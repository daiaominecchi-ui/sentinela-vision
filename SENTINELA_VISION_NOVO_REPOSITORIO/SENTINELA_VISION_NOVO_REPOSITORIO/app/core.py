from __future__ import annotations
import json, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)
DB = DATA / 'sentinela.sqlite3'

MACHINES = {
 'motor': {'name':'Motor de indução', 'parts':['Rolamentos','Eixo','Estator','Ventilação','Carcaça']},
 'pump': {'name':'Bomba centrífuga', 'parts':['Rotor','Selo mecânico','Rolamentos','Sucção','Carcaça']},
 'conveyor': {'name':'Esteira transportadora', 'parts':['Correia','Roletes','Motorredutor','Tensionador','Estrutura']},
 'compressor': {'name':'Compressor', 'parts':['Motor','Válvulas','Lubrificação','Filtro','Reservatório']},
}
SYMPTOMS = {
 'vibration': {'label':'Vibração excessiva','causes':['Desalinhamento','Desbalanceamento','Folga mecânica'], 'checks':['Verificar histórico de vibração','Inspecionar fixações com equipamento bloqueado']},
 'heat': {'label':'Temperatura elevada','causes':['Sobrecarga','Ventilação insuficiente','Atrito anormal'], 'checks':['Comparar corrente e temperatura','Verificar obstruções de ventilação após bloqueio']},
 'noise': {'label':'Ruído anormal','causes':['Desgaste mecânico','Lubrificação inadequada','Peças soltas'], 'checks':['Registrar tipo e localização do ruído','Consultar plano de lubrificação do fabricante']},
 'leak': {'label':'Vazamento','causes':['Vedação deteriorada','Conexão frouxa','Pressão inadequada'], 'checks':['Identificar fluido e região afetada','Isolar fontes de energia e pressão antes da inspeção']},
 'low_output': {'label':'Baixo desempenho','causes':['Carga acima do previsto','Obstrução','Falha de acionamento'], 'checks':['Comparar ponto de operação com especificação','Analisar telemetria e alarmes existentes']},
}

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute('''CREATE TABLE IF NOT EXISTS equipment (id TEXT PRIMARY KEY, name TEXT NOT NULL, kind TEXT NOT NULL, created TEXT NOT NULL)''')
        con.execute('''CREATE TABLE IF NOT EXISTS inspections (id TEXT PRIMARY KEY, equipment_id TEXT NOT NULL, part TEXT NOT NULL, symptoms TEXT NOT NULL, notes TEXT NOT NULL, diagnosis TEXT NOT NULL, created TEXT NOT NULL)''')
        con.execute('''CREATE TABLE IF NOT EXISTS uploads (id TEXT PRIMARY KEY, equipment_id TEXT NOT NULL, name TEXT NOT NULL, mime TEXT NOT NULL, stored_name TEXT NOT NULL, created TEXT NOT NULL)''')

def stamp(): return datetime.now(timezone.utc).isoformat()
def ident(): return uuid.uuid4().hex

def diagnose(kind, part, symptoms):
    if kind not in MACHINES: raise ValueError('Tipo de equipamento desconhecido')
    if part not in MACHINES[kind]['parts']: raise ValueError('Componente desconhecido')
    if not symptoms or any(s not in SYMPTOMS for s in symptoms): raise ValueError('Sintomas inválidos')
    causes, checks = [], []
    for symptom in symptoms:
        causes.extend(SYMPTOMS[symptom]['causes'])
        checks.extend(SYMPTOMS[symptom]['checks'])
    return {'status':'hipóteses preliminares', 'causes':list(dict.fromkeys(causes)), 'checks':list(dict.fromkeys(checks)), 'confidence':'não calculada — sem dados reais validados', 'warning':'Não executar intervenções com equipamento energizado. Confirmar com profissional habilitado, procedimentos de bloqueio e manual do fabricante.'}
