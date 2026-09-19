"""Bounded public HTTPS observations; never execute customer code or JavaScript."""
import http.client
import ipaddress
import socket
import ssl
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlsplit, urljoin
import xml.etree.ElementTree as ET

MAX_BYTES = 262144


def target(url):
    if not isinstance(url, str) or len(url) > 2048 or any(ord(c) < 33 for c in url):
        raise ValueError('Expected an HTTPS URL without whitespace')
    p = urlsplit(url)
    if p.scheme != 'https' or not p.hostname or p.username or p.password or p.port not in (None, 443):
        raise ValueError('Only public HTTPS URLs on port 443 are supported')
    host = p.hostname.encode('idna').decode('ascii')
    addresses = list(dict.fromkeys(x[4][0] for x in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)))
    if not addresses or any(not ipaddress.ip_address(a).is_global for a in addresses):
        raise ValueError('Private or non-public destinations are not supported')
    return host, addresses[0], p.path or '/', p.query


class PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self, host, address):
        super().__init__(host, timeout=8, context=ssl.create_default_context())
        self.address = address

    def connect(self):
        raw = socket.create_connection((self.address, 443), timeout=self.timeout)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except BaseException:
            raw.close()
            raise


def fetch(url, body=True):
    start = time.monotonic()
    chain = []
    current = url
    for _ in range(6):
        host, address, path, query = target(current)
        connection = PinnedHTTPS(host, address)
        try:
            connection.request('GET', path + ('?' + query if query else ''), headers={
                'User-Agent': 'ProfixSiteCheck/1.0 (+https://github.com/pruebasprofix-glitch/profix-code-services)',
                'Accept-Encoding': 'identity'})
            response = connection.getresponse()
            headers = {k.lower(): v for k, v in response.getheaders()}
            chain.append({'url': current, 'status': response.status})
            if response.status in (301, 302, 303, 307, 308) and headers.get('location'):
                current = urljoin(current, headers['location'])
                continue
            raw = response.read(MAX_BYTES + 1) if body else b''
            return {'url': url, 'final_url': current, 'status': response.status,
                    'redirects': chain, 'elapsed_ms': round((time.monotonic()-start)*1000),
                    'headers': {k: headers[k] for k in ['content-type','strict-transport-security',
                        'content-security-policy','x-content-type-options','referrer-policy','x-robots-tag'] if k in headers},
                    'truncated': len(raw) > MAX_BYTES, 'body': raw[:MAX_BYTES].decode('utf-8', errors='replace')}
        finally:
            connection.close()
    raise ValueError('More than five redirects')


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(); self.title = ''; self.in_title = False; self.description = None; self.canonical = None; self.h1 = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title': self.in_title = True
        if tag == 'h1': self.h1 += 1
        if tag == 'meta' and a.get('name','').lower() == 'description': self.description = a.get('content','')
        if tag == 'link' and 'canonical' in a.get('rel','').lower().split(): self.canonical = a.get('href')
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.title += data


def validate(kind, data):
    if not isinstance(data, dict): raise ValueError('Input must be an object')
    key = 'sitemap_url' if kind == 'sitemap' else 'urls'
    if set(data) != {key}: raise ValueError('Unexpected or missing input fields')
    urls = [data[key]] if kind == 'sitemap' else data[key]
    limit = 5 if kind == 'pages' else 20
    if not isinstance(urls, list) or not 1 <= len(urls) <= limit: raise ValueError(f'Provide 1-{limit} URLs')
    for url in urls:
        if not isinstance(url,str) or len(url)>2048: raise ValueError('Invalid URL')
        p=urlsplit(url)
        if p.scheme!='https' or not p.hostname or p.username or p.password or p.port not in (None,443): raise ValueError('Public HTTPS URLs only')
    return urls


def audit(kind, data, fetcher=fetch):
    urls = validate(kind, data)
    meta = {}
    if kind == 'sitemap':
        source = fetcher(urls[0])
        if source['status'] != 200 or source['truncated']: raise ValueError('Sitemap must return HTTP 200 and fit within 256 KiB')
        body = source['body']
        if '<!DOCTYPE' in body.upper() or '<!ENTITY' in body.upper(): raise ValueError('XML entities are not supported')
        try:
            root = ET.fromstring(body)
        except ET.ParseError as exc:
            raise ValueError('Invalid sitemap XML') from exc
        if root.tag.rsplit('}',1)[-1] != 'urlset': raise ValueError('Send a urlset sitemap, not a sitemap index')
        urls = [e.text.strip() for e in root.iter() if e.tag.rsplit('}',1)[-1]=='loc' and e.text]
        meta = {'sitemap_url':data['sitemap_url'], 'urls_in_sitemap':len(urls), 'sample_limit':20}
        urls = urls[:20]
        if not urls: raise ValueError('Sitemap contains no URLs')
    results = []
    for url in urls:
        try:
            result = fetcher(url, body=kind=='pages')
            body = result.pop('body', '')
            if kind == 'pages':
                parser=Metadata();parser.feed(body)
                result['metadata']={'title':parser.title.strip()[:500], 'description':(parser.description or '')[:1000],
                                    'canonical':(parser.canonical or '')[:2048], 'h1_count':parser.h1}
            results.append(result)
        except Exception as exc:
            results.append({'url':url,'error':type(exc).__name__, 'status':None})
    return {'service':kind,'checked_at':datetime.now(timezone.utc).isoformat(), **meta,
            'results':results,'limitations':['Single observation from one server, not uptime monitoring.',
                'No JavaScript rendering, authentication, vulnerability scan or SEO ranking guarantee.',
                'Public HTTPS only. Up to 5 redirects and 256 KiB per page. Results may differ by region.',
                'Missing headers or metadata are observations, not proof of a vulnerability.']}
