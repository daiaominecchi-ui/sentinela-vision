# SENTINELA VISION — Base de produto web (v0.1)

Plataforma web de inspeção industrial com visualizador 3D, cadastro de máquinas, anexos de fotografias/PDF/GLB, hipóteses de falhas por regras, histórico persistente e relatórios PDF.

**Estado:** base funcional de demonstração e desenvolvimento, **não produto comercial pronto/certificado**.

## Execução no GitHub Codespaces ou PC

```bash
python -m venv .venv
source .venv/bin/activate  # no Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Abra a porta **8000** no Codespaces ou `http://localhost:8000` no PC. O frontend carrega Three.js via CDN, exigindo internet no navegador.

Testes:

```bash
python -m pytest -q
```

## Funcionalidades disponíveis

- Quatro tipos de máquinas com geometria 3D **esquemática** e rotação/zoom.
- Upload de fotos (PNG/JPG/WEBP), plantas PDF e arquivos 3D GLB até 15 MB.
- Visualização de modelos GLB enviados pelo usuário.
- Cadastro de equipamentos e inspeções persistidos em SQLite.
- Hipóteses e recomendações genéricas baseadas em regras explicáveis.
- Histórico e PDF de inspeção.
- API OpenAPI em `/docs`.

## O que **não** está implementado

- Reconstrução automática de fotos/PDF para geometria 3D.
- Leitura semântica de plantas técnicas por IA.
- Identificação automática confiável de modelo e componentes internos.
- Diagnóstico validado de máquinas reais e integração com sensores.
- Contas, controle de acesso, armazenamento em nuvem, faturamento e operações multiusuário.

## Arquitetura e produção

FastAPI + frontend Three.js + SQLite local. Antes de comercializar, implementar autenticação, permissões por organização, PostgreSQL, armazenamento de objetos, antivírus para uploads, filas de processamento, limites por usuário, observabilidade, políticas de privacidade/LGPD, testes E2E, auditoria, backups e avaliações de segurança. Para reconstrução 3D, integrar um pipeline de fotogrametria ou provedor 3D com processamento em GPU, calibração de escala e controle de incerteza. Nenhuma reconstrução é simulada como se fosse real.

**Segurança:** não utilizar hipóteses deste software para executar manutenção sem avaliação de profissional habilitado e procedimentos de bloqueio e segurança adequados.
