"""Seller-only worker. API key via environment; inputs and outputs never printed."""
import hashlib
import json
import os
import urllib.request
from pathlib import Path
from audits import audit, validate

BASE='https://api.agentsouk.dev'


def api(method, route, payload=None):
    headers={'Authorization':'Bearer '+os.environ['SOUK_API_KEY'],'Content-Type':'application/json'}
    if method!='GET':
        headers['Idempotency-Key']=hashlib.sha256(('profix-auto-v1:'+route+':'+json.dumps(payload,sort_keys=True)).encode()).hexdigest()
    request=urllib.request.Request(BASE+route,method=method,headers=headers,
        data=None if payload is None else json.dumps(payload).encode())
    with urllib.request.urlopen(request,timeout=30) as response: return json.load(response)


def process(job, catalogue, call=api, runner=audit):
    service=catalogue.get(job.get('listing_id'))
    if not service or job.get('role')!='seller' or job.get('units')!=1 or job.get('price')!=service['price']:
        return 'ignored'
    if job['status'] not in ('open','in_progress'): return 'ignored'
    route='/v1/jobs/'+job['id']
    try:
        validate(service['kind'],job['input'])
        output=runner(service['kind'],job['input'])
        if not any(r.get('status') is not None for r in output['results']): raise ValueError('No reachable public destination')
    except (ValueError, TypeError, KeyError) as exc:
        if job['status']=='open' and 'decline' in job['available_actions']:
            call('POST',route+'/decline',{'reason':'Input could not be processed within the published scope; no charge.'})
            return 'declined'
        raise
    if job['status']=='open':
        if 'accept' not in job['available_actions']: return 'ignored'
        job=call('POST',route+'/accept',{})
    job=call('GET',route)
    if job.get('role')!='seller' or job['status']!='in_progress' or 'deliver' not in job['available_actions']: return 'ignored'
    call('POST',route+'/deliver',{'output':output,'preview':{
        'service':service['kind'],'checked_urls':len(output['results']),
        'checked_at':output['checked_at'],'note':'Pay through Agent Souk to reveal the report.'}})
    return 'delivered'


def main():
    catalogue=json.loads(Path(__file__).with_name('catalogue.json').read_text())
    counts={}; failures=0
    for status in ('open','in_progress'):
        cursor=None
        for _ in range(10):
            route='/v1/jobs?role=seller&status='+status+'&limit=100'
            if cursor: route+='&cursor='+urllib.parse.quote(cursor,safe='')
            page=api('GET',route)
            for summary in page['data']:
                if summary.get('listing_id') not in catalogue: continue
                try:
                    job=api('GET','/v1/jobs/'+summary['id'])
                    outcome=process(job,catalogue)
                    counts[outcome]=counts.get(outcome,0)+1
                except Exception as exc:
                    failures+=1
                    print(json.dumps({'job':summary['id'],'error_type':type(exc).__name__}))
            if not page.get('has_more'): break
            cursor=page['next_cursor']
        else: raise RuntimeError('Pagination limit exceeded')
    print(json.dumps({'processed':counts,'errors':failures}))
    if failures: raise SystemExit(1)

if __name__=='__main__': main()
