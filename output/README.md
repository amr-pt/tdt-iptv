# 📊 Output

Esta pasta contém os relatórios gerados pelo script de verificação de streams.

## 📄 Conteúdo

- **stream_status_report.json** - Relatório detalhado da última verificação de streams

## 📋 Estrutura do Relatório

```json
{
  "timestamp": "2024-10-07T12:33:00",
  "summary": {
    "total": 55,
    "working": 55,
    "placeholder": 0,
    "not_working": 0,
    "percentage_working": 100.0
  },
  "channels": [
    {
      "name": "🇵🇹 RTP 1",
      "url": "https://...",
      "status": "working",
      "http_status": 200,
      "method": "HEAD"
    }
  ]
}
```

## ⚠️ Nota

Esta pasta está no `.gitignore`, ou seja, os relatórios não são submetidos para o repositório.
