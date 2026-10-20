from fastapi.testclient import TestClient
from app.main import app
from app.core import diagnose

def test_diagnosis():
    d=diagnose('motor','Rolamentos',['vibration','heat'])
    assert 'Desalinhamento' in d['causes']

def test_catalog_and_flow():
    with TestClient(app) as client:
        assert client.get('/api/catalog').status_code==200
        eq=client.post('/api/equipment',json={'name':'Motor teste','kind':'motor'})
        assert eq.status_code==201
        i=client.post('/api/inspections',json={'equipment_id':eq.json()['id'],'part':'Rolamentos','symptoms':['vibration'],'notes':'Ruído e vibração'})
        assert i.status_code==201
        pdf=client.get('/api/inspections/'+i.json()['id']+'/pdf')
        assert pdf.status_code==200 and pdf.content.startswith(b'%PDF')

def test_invalid_kind():
    with TestClient(app) as client:
        assert client.post('/api/equipment',json={'name':'Teste','kind':'inexistente'}).status_code==422

def test_reconstruction_honesty():
    with TestClient(app) as client:
        assert client.get('/api/reconstruction/status').json()['available'] is False
