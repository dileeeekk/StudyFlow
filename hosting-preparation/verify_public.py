import urllib.request, urllib.error, json, secrets
from pathlib import Path
base='https://dileeeekk.pythonanywhere.com/api/'
def request(path, body=None, token=None):
    headers={'Content-Type':'application/json'}
    if token: headers['Authorization']='Bearer '+token
    req=urllib.request.Request(base+path, data=json.dumps(body).encode() if body is not None else None,headers=headers)
    try:
        with urllib.request.urlopen(req,timeout=30) as res: return res.status,json.load(res)
    except urllib.error.HTTPError as e: return e.code,json.load(e)
assert request('health/')==(200,{'status':'ok'})
assert request('auth/me/')[0]==401
data={'email':'cloud-test-'+secrets.token_hex(6)+'@example.com','password':secrets.token_urlsafe(24),'full_name':'Cloud verification','university':'Test University','terms_accepted':True}
code,pair=request('auth/register/',data);assert code==201,code
assert request('auth/me/',token=pair['access'])[0]==200
code,login=request('auth/login/',{k:data[k] for k in ('email','password')});assert code==200
code,rotated=request('auth/refresh/',{'refresh':login['refresh']});assert code==200
assert request('auth/refresh/',{'refresh':login['refresh']})[0]==401
assert request('auth/logout/',{'refresh':rotated['refresh']})[0]==200
assert request('auth/refresh/',{'refresh':rotated['refresh']})[0]==401
assert request('auth/logout/',{'refresh':pair['refresh']})[0]==200
report={'server':base,'health':200,'registration':201,'login':200,'profile':200,'refresh_rotation':'passed','logout_revocation':'passed','test_account':data['email']}
Path(__file__).with_name('public-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Public HTTPS verification passed: registration, login, profile, JWT rotation and logout. No tokens logged.')
