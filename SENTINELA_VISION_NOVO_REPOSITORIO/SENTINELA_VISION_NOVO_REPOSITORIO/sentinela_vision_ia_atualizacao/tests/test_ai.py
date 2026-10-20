from fastapi.testclient import TestClient
from app.main import app

def test_ai_status(monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    with TestClient(app) as client:
        result=client.get('/api/ai/status')
        assert result.status_code==200
        assert result.json()['diagnosis_ai'] is False
        assert result.json()['reconstruction_3d'] is False

def test_ai_requires_credentials(monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    with TestClient(app) as client:
        eq=client.post('/api/equipment',json={'name':'Motor AI teste','kind':'motor'}).json()
        r=client.post('/api/ai/diagnosis',json={'equipment_id':eq['id'],'part':'Rolamentos','symptoms':['vibration']})
        assert r.status_code==503

def test_vision_rejects_invalid_format():
    with TestClient(app) as client:
        r=client.post('/api/ai/vision',files={'file':('bad.txt',b'abc','text/plain')})
        assert r.status_code==415
