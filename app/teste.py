import json
import requests

resp = requests.get('http://127.0.0.1:8000/anuncio/').json()


sla = json.dumps(resp)
sl = json.loads(sla)
print(type(sl))
for x in sl:
    if x['usuario'] == 'joaoandre':
        print(x['bairro'])
    


