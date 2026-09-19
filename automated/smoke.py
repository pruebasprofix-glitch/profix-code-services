"""Public sample only; no marketplace order or payment is created."""
import json
from audits import audit
result=audit('pages',{'urls':['https://example.com']})
assert result['results'][0]['status'] in (200,206), 'Public sample did not return a page'
assert result['results'][0]['metadata']['title'], 'Public sample had no parsed title'
print(json.dumps({'sample':'https://example.com','status':result['results'][0]['status'],'title':result['results'][0]['metadata']['title']}))
