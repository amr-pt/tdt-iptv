# 📺 Canais IPTV Públicos

Uma lista organizada de canais IPTV portugueses e internacionais, com foco nos canais de televisão digital terrestre (TDT) de Portugal.

## ⚠️ Aviso Importante

**Este projeto NÃO faz streaming de canais de televisão.** Todos os URLs presentes nas listas M3U são endereços públicos encontrados na internet que apontam para streams oficiais ou disponíveis publicamente.

Este repositório funciona apenas como uma **agregação e organização** de ligações públicas, facilitando o acesso a conteúdos de televisão aberta.

## 🎯 Objetivo

A ideia desta lista é ter uma coleção de canais portugueses o mais próxima possível da oferta TDT (Televisão Digital Terrestre) de Portugal, aproveitando também para incluir alguns canais de interesse de outros países.

## 📋 Conteúdo

- **Lista M3U**: Ficheiro M3U com canais portugueses e internacionais
- **Canais TDT Portugal**: Canais generalistas, notícias, regionais e especializados
- **Canais Internacionais**: Seleção de canais de outros países (Espanha, França, etc.)
- **EPG e Logos**: Referências incluídas no ficheiro M3U
- **Scripts**: Ferramentas de verificação e automação (ver pasta `scripts/`)

## 🗂️ Estrutura

```
playlists/
└── tdt.m3u       # Lista de canais TDT portugueses e internacionais
scripts/
└── check_streams.py  # Script de verificação de streams
output/
└── stream_status_report.json  # Relatório de verificação
```

## 📡 Como Utilizar

1. **VLC Media Player**
   - Abrir VLC → Media → Open Network Stream
   - Colar o URL do ficheiro M3U ou abrir o ficheiro localmente

2. **Kodi**
   - Instalar PVR IPTV Simple Client
   - Configurar com o caminho para o ficheiro M3U

3. **Sparkle TV - IPTV Player** (Recomendado para Android) 📱
   - Descarregar [Sparkle TV](https://play.google.com/store/apps/details?id=com.sparkle.tv) na Google Play Store
   - Abrir a aplicação → Adicionar playlist
   - Selecionar "URL" ou "Ficheiro Local"
   - Colar o URL do ficheiro M3U ou selecionar o ficheiro M3U descarregado
   - Interface intuitiva com suporte a EPG, favoritos e categorias

4. **Outros Leitores**
   - Qualquer leitor que suporte listas M3U/M3U8

## 🔗 Fontes

Os canais, logos e informações de EPG desta lista são agregados de fontes públicas, incluindo:

- [LITUATUI/M3UPT](https://github.com/LITUATUI/M3UPT) - Lista de canais portugueses
- [Free-TV/IPTV](https://github.com/Free-TV/IPTV) - Base de dados de canais IPTV gratuitos
- [TDT Channels](https://www.tdtchannels.com) - Listas de canais TDT de vários países

## 📝 Contribuir

Contribuições são bem-vindas! Se encontrar ligações que não funcionam ou quiser adicionar novos canais públicos, sinta-se à vontade para:

1. Abrir uma issue
2. Submeter um pull request
3. Sugerir melhorias

### Verificar Disponibilidade de Streams

Antes de reportar canais a não funcionar, pode usar o script de verificação para confirmar o estado dos streams:

```bash
# Instalar dependências
pip install -r scripts/requirements.txt

# Executar verificação
python scripts/check_streams.py
```

Para mais detalhes, consulte [scripts/CHECK_STREAMS.md](scripts/CHECK_STREAMS.md) e [scripts/GITHUB_ACTIONS.md](scripts/GITHUB_ACTIONS.md).

## ⚖️ Licença e Responsabilidade

- Este projeto não aloja, não transmite e não distribui conteúdo protegido por direitos de autor
- Todas as ligações apontam para streams públicos disponíveis na internet
- Os utilizadores são responsáveis pelo uso que fazem desta informação
- Respeite sempre os direitos de autor e os termos de serviço dos fornecedores de conteúdo

## 🌟 Agradecimentos

Um agradecimento especial aos projetos [M3UPT](https://github.com/LITUATUI/M3UPT), [Free-TV/IPTV](https://github.com/Free-TV/IPTV) e [TDT Channels](https://www.tdtchannels.com) pela disponibilização pública de listas e recursos.

---

**Nota**: Este é um projeto pessoal sem fins comerciais, destinado a simplificar o acesso a canais de televisão aberta disponíveis publicamente.
