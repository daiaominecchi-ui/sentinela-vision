# Sentinela Vision — integração híbrida de IA

## Recursos
- **Diagnóstico por regras**: funciona localmente, sem IA externa.
- **Diagnóstico com IA**: endpoint `POST /api/ai/diagnosis`; usa modelo externo somente quando `OPENAI_API_KEY` está configurada.
- **Visão computacional**: `POST /api/ai/vision` interpreta JPG, PNG e WEBP com modelo externo. Não extrai automaticamente plantas PDF.
- **Reconstrução 3D**: **não implementada**. O visualizador atual mostra geometrias esquemáticas e arquivos GLB enviados pelo usuário; isso não equivale a reconstrução por IA.

## Instalação (Codespaces, na pasta deste README)
```bash
python -m pip install -r requirements.txt
python -m pytest -q
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Abra a porta 8000 no navegador. Se estiver num Codespace, mantenha a porta **privada** durante testes com dados reais.

## Habilitar as duas IAs
Crie uma chave de API com acesso ao modelo multimodal compatível e configure-a em **Codespaces Secrets** como `OPENAI_API_KEY` (não cole no frontend nem faça commit). Reinicie o servidor. Opcional: `OPENAI_MODEL` (padrão `gpt-4o-mini`). Uso sujeito a cobrança, limites e disponibilidade do provedor. O status aparece na interface.

## Limitações para produção
É um protótipo técnico, não certificado. Antes de oferecer comercialmente, implementar autenticação/autorização, segregação de clientes, gestão de consentimento e retenção de arquivos, limites de uso, logs auditáveis, observabilidade, fila de tarefas e banco gerenciado; validar saídas da IA com profissionais e manuais do fabricante. Não enviar fotografias confidenciais sem autorização. Nunca executar manutenção com base apenas na resposta da IA.

## Reconstrução 3D futura
Integrar um provedor de fotogrametria ou reconstrução multimodal, processamento assíncrono e armazenamento de GLB; validar escala e dimensões contra plantas e medições reais. Não há garantia de CAD preciso a partir de foto única.
