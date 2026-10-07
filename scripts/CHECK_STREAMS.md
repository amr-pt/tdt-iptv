# 📡 Verificação de Streams

Script para verificar periodicamente a disponibilidade dos streams IPTV na lista.

## 🚀 Como Utilizar

### Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

### Executar verificação

```bash
python check_streams.py
```

O script irá:
1. Ler o ficheiro `../playlists/tdt.m3u`
2. Verificar cada stream em paralelo (até 10 simultâneos)
3. Gerar um relatório no terminal
4. Guardar um relatório detalhado em JSON em `../output/stream_status_report.json`

## 📊 Relatório

O relatório inclui:
- **Total de canais**: Quantidade total de canais na lista
- **A funcionar**: Canais com streams acessíveis
- **Placeholders**: Canais sem stream definido (marcados com #)
- **A não funcionar**: Canais com streams inacessíveis
- **Percentual funcional**: % de canais com streams a funcionar

## 🔐 Suporte a Headers

O script suporta automaticamente headers definidos via `#EXTVLCOPT` no ficheiro M3U:

```
#EXTINF:-1 group-title="Portugal" tvg-id="SIC.pt",🇵🇹 SIC
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0
#EXTVLCOPT:http-origin=https://sic.pt
#EXTVLCOPT:http-referrer=https://sic.pt/
https://sic.live.impresa.pt/sic1080p.m3u8
```

Headers suportados:
- `http-user-agent` → `User-Agent`
- `http-origin` → `Origin`
- `http-referrer` → `Referer`

### Exemplo de saída

```
============================================================
📊 RELATÓRIO DE STREAMS
============================================================
Total de canais: 50
✅ A funcionar: 35 (70.0%)
⚪ Placeholders: 10
❌ A não funcionar: 5
============================================================
```

## 🔧 Personalização

### Alterar timeout

Para canais que demoram a responder, edite o script:

```python
check_stream(channel, timeout=15)  # Aumentar para 15 segundos
```

### Alterar número de threads

Para verificar mais canais em paralelo:

```python
with ThreadPoolExecutor(max_workers=20) as executor:  # Aumentar para 20
```

## 📅 Automatização

### Via GitHub Actions (recomendado)

Crie um ficheiro `.github/workflows/check-streams.yml`:

```yaml
name: Check Streams

on:
  schedule:
    - cron: '0 0 * * *'  # Diariamente à meia-noite
  workflow_dispatch:     # Permite execução manual

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Check streams
        run: python check_streams.py
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: stream-report
          path: stream_status_report.json
```

### Via cron (Linux)

Adicione ao crontab:

```bash
# Executar diariamente às 00:00
0 0 * * * cd /path/to/tdt-iptv && /usr/bin/python3 check_streams.py >> logs/check_streams.log 2>&1
```

### Via agendamento (Windows)

Usar o Agendador de Tarefas para executar o script periodicamente.

## 📝 Interpretação dos Estados

- **working**: Stream acessível (HTTP 200, 206, 301, 302)
- **placeholder**: Canal sem stream definido (#)
- **not_working**: Stream retornou erro HTTP
- **timeout**: Pedido excedeu o tempo limite
- **error**: Erro de ligação ou DNS

## ⚠️ Limitações

- Alguns streams podem requerer User-Agent específico ou headers adicionais
- Streams com geo-blocking podem não funcionar dependendo da localização
- A verificação não garante que o stream contenha conteúdo válido, apenas que o URL é acessível
- Verificações frequentes podem ser bloqueadas por alguns servidores

## 🔍 Método de Verificação

O script usa uma abordagem de dois passos:

1. **HEAD request** (mais rápido) - Tenta primeiro um pedido HEAD
2. **GET request** (fallback) - Se o HEAD falhar, tenta um GET com streaming

Isto é necessário porque alguns servidores (como Euronews) não suportam bem requests HEAD. O GET com streaming apenas lê os primeiros 1KB para verificar que o stream é válido, sem descarregar o conteúdo completo.

## 🔄 Atualização da Lista

Após identificar canais a não funcionar:
1. Procure novos URLs em fontes como [M3UPT](https://github.com/LITUATUI/M3UPT) ou [Free-TV/IPTV](https://github.com/Free-TV/IPTV)
2. Atualize o ficheiro `../playlists/tdt.m3u`
3. Execute novamente a verificação
