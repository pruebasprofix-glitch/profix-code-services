import copy
import unittest
from unittest.mock import patch
from audits import target, audit, validate
from worker import process


def response(url, body=True):
    return {'url':url,'status':200,'final_url':url,'redirects':[], 'headers':{},'truncated':False,
            'body':'<title>Demo</title><meta name="description" content="Example"><h1>Welcome</h1>'}


class Audits(unittest.TestCase):
    def test_private_destinations_rejected(self):
        for address in ['127.0.0.1','10.0.0.1','169.254.169.254','::1','192.168.1.2','100.64.0.1']:
            with self.subTest(address=address), patch('socket.getaddrinfo',return_value=[(2,1,6,'',(address,443))]):
                with self.assertRaises(ValueError): target('https://example.com')
    def test_mixed_dns_rejected(self):
        with patch('socket.getaddrinfo',return_value=[(2,1,6,'',('8.8.8.8',443)),(2,1,6,'',('127.0.0.1',443))]):
            with self.assertRaises(ValueError):target('https://example.com')
    def test_bad_schemes_credentials_ports(self):
        for url in ['file:///etc/passwd','http://example.com','https://user:pass@example.com','https://example.com:8080','https://example.com/\r\nx:bad']:
            with self.subTest(url=url), self.assertRaises(ValueError):target(url)
    def test_page_metadata_and_no_body_leak(self):
        r=audit('pages',{'urls':['https://example.com']},response)['results'][0]
        self.assertEqual(r['metadata']['title'],'Demo');self.assertEqual(r['metadata']['h1_count'],1);self.assertNotIn('body',r)
    def test_input_limits(self):
        with self.assertRaises(ValueError):validate('pages',{'urls':['https://example.com']*6})
        with self.assertRaises(ValueError):validate('pages',{'urls':[]})
        with self.assertRaises(ValueError):validate('pages',{'urls':['https://example.com'],'code':'anything'})
    def test_redirect_service_fetches_no_body(self):
        calls=[]
        def fetcher(url,body=True):calls.append(body);return response(url,body)
        audit('redirects',{'urls':['https://example.com']},fetcher)
        self.assertEqual(calls,[False])
    def test_sitemap_sample_and_namespace(self):
        def fetcher(url,body=True):
            r=response(url,body)
            if 'xml' in url:r['body']='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>https://example.com/'+str(i)+'</loc></url>' for i in range(25))+'</urlset>'
            return r
        r=audit('sitemap',{'sitemap_url':'https://example.com/sitemap.xml'},fetcher)
        self.assertEqual(r['urls_in_sitemap'],25);self.assertEqual(len(r['results']),20)
    def test_entities_rejected(self):
        def fetcher(url):return {**response(url),'body':'<!DOCTYPE foo [<!ENTITY e SYSTEM "file:///etc/passwd">]><urlset/>'}
        with self.assertRaises(ValueError):audit('sitemap',{'sitemap_url':'https://example.com'},fetcher)
    def test_network_failure_is_observation(self):
        def fail(*a,**k):raise TimeoutError()
        self.assertEqual(audit('pages',{'urls':['https://example.com']},fail)['results'][0]['error'],'TimeoutError')


class Worker(unittest.TestCase):
    def setUp(self):
        self.catalogue={'lst_test':{'price':5000000,'kind':'pages'}}
        self.job={'id':'job_test','listing_id':'lst_test','role':'seller','units':1,'price':5000000,'status':'open','input':{'urls':['https://example.com']},'available_actions':['accept','decline']}
        self.calls=[]
    def call(self,method,path,payload=None):
        self.calls.append((method,path,payload))
        return {**self.job,'status':'in_progress','available_actions':['deliver']}
    def runner(self,kind,data):return audit(kind,data,response)
    def test_accept_deliver_and_preview_separate(self):
        self.assertEqual(process(self.job,self.catalogue,self.call,self.runner),'delivered')
        self.assertEqual([x[0] for x in self.calls],['POST','GET','POST'])
        payload=self.calls[-1][2];self.assertIn('results',payload['output']);self.assertNotIn('results',payload['preview'])
    def test_do_not_accept_other_jobs_or_wrong_price(self):
        for field,value in [('role','buyer'),('listing_id','unknown'),('price',1),('units',2),('status','completed')]:
            j={**self.job,field:value};self.assertEqual(process(j,self.catalogue,self.call,self.runner),'ignored')
        self.assertEqual(self.calls,[])
    def test_invalid_input_declined_before_accept(self):
        self.job['input']={'urls':[]}
        self.assertEqual(process(self.job,self.catalogue,self.call,self.runner),'declined')
        self.assertTrue(self.calls[0][1].endswith('/decline'))
    def test_unreachable_not_sold(self):
        def runner(*a):return {'results':[{'status':None}]}
        self.assertEqual(process(self.job,self.catalogue,self.call,runner),'declined')
    def test_changed_state_not_delivered(self):
        def call(*args):return {**self.job,'status':'cancelled','available_actions':[]}
        self.assertEqual(process(self.job,self.catalogue,call,self.runner),'ignored')

if __name__=='__main__':unittest.main()
