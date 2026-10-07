# 🤖 GitHub Actions - Guia Rápido

## O que é GitHub Actions?

É uma ferramenta de automação do GitHub que permite executar scripts automaticamente quando certos eventos acontecem no repositório.

## Como funciona o workflow deste projeto?

O ficheiro `.github/workflows/check-streams.yml` define um workflow que:

### 1. **Quando executa?**
- **Automaticamente**: Todos os dias às 00:00 UTC (via cron)
- **Manualmente**: Podes clicar em "Run workflow" na interface do GitHub

### 2. **O que faz?**
```
1. Descarrega o código do repositório
2. Instala Python 3.10
3. Instala as dependências (requests)
4. Executa o script check_streams.py
5. Guarda o relatório JSON como artifact
6. Cria um resumo na página da run
```

### 3. **Como ver os resultados?**

#### Via Interface Web:
1. Vai ao repositório no GitHub
2. Clica no separador **"Actions"** no topo
3. Seleciona o workflow **"Check Streams"** na esquerda
4. Vê a lista de runs (execuções)
5. Clica numa run para ver detalhes
6. Na secção "Artifacts", podes descarregar o relatório JSON

#### Via Notificações:
- O GitHub envia notificações quando workflows falham
- Podes configurar notificações por email

## Como executar manualmente?

1. Vai ao separador **"Actions"**
2. Seleciona **"Check Streams"**
3. Clica em **"Run workflow"**
4. Seleciona a branch (geralmente `main`)
5. Clica em **"Run workflow"** novamente

## Personalizar horário?

Edita o ficheiro `.github/workflows/check-streams.yml`:

```yaml
on:
  schedule:
    - cron: '0 12 * * *'  # Executar às 12:00 UTC todos os dias
```

Formato cron: `minuto hora dia-mês mês dia-semana`

Exemplos:
- `'0 0 * * *'` - Todos os dias à meia-noite
- `'0 */6 * * *'` - A cada 6 horas
- `'0 9 * * 1'` - Todas as segundas às 9:00
- `'0 9,21 * * *'` - Todos os dias às 9:00 e 21:00

## Vantagens

✅ **Automático** - Não precisas de executar manualmente
✅ **Histórico** - Guarda relatórios das últimas 30 execuções
✅ **Gratuito** - Para repositórios públicos e privados (com limites)
✅ **Notificações** - Avisa quando algo falha
✅ **Multi-plataforma** - Executa em servidores do GitHub (Linux, macOS, Windows)

## Limitações

- **2000 minutos/mês** para repositórios privados gratuitos
- **Ilimitado** para repositórios públicos
- Cada run deste workflow demora ~2-3 minutos

## Desativar?

Para desativar o workflow:

1. Vai ao separador **"Actions"**
2. Seleciona **"Check Streams"**
3. Clica nos **"..."** (três pontos)
4. Seleciona **"Disable workflow"**

Ou comenta a linha do cron no ficheiro:
```yaml
# schedule:
#   - cron: '0 0 * * *'
```
