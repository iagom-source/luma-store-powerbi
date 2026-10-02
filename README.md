# LUMA Store · O custo do frete grátis

Dashboard em Power BI com páginas em **HTML/CSS/SVG geradas por medidas DAX** e uma capa com **fundo de vídeo animado** e KPIs calculados ao vivo.

> Dados fictícios: a LUMA Store é um e-commerce de casa e decoração inventado para este estudo.

## A história

Em março/2024 a LUMA passou a oferecer frete grátis em pedidos a partir de R$ 199. As vendas subiram, mas a margem caiu:

| Ano | Receita líquida | Margem de contribuição |
|---|---|---|
| 2023 | R$ 11,70 Mi | 38,5% |
| 2024 | R$ 15,70 Mi | 34,1% |
| 2025 | R$ 19,33 Mi | 32,9% |

De cada R$ 100 vendidos, o frete subsidiado e a comissão do marketplace passaram a levar **R$ 4,9 a mais**. A categoria Móveis concentra 1/3 do frete subsidiado, e o canal Marketplace tem margem de 24,8%, contra cerca de 37% no site e no app.

## Páginas

| Página | Medida | O que mostra |
|---|---|---|
| Capa | `HTML Capa` | Fundo animado (WebP embutido), manchete e 3 KPIs dinâmicos |
| Diagnóstico | `HTML Diagnostico` | KPIs ano contra ano, gráfico mensal em SVG com tooltip em CSS, canais, composição de cada R$ 100 e ação recomendada |

## Como funciona

```
CSV (dados fictícios) → Power Query → modelo estrela → medidas DAX → HTML/CSS/SVG → visual HTML Content
```

- **Modelo:** `fVendas` (101 mil itens de pedido, 2023–2025), com as dimensões `dProduto`, `dCliente` e `dCalendario`. As medidas ficam em `_Medidas`, organizadas em pastas.
- **Formato PBIP/TMDL:** o modelo é texto versionável, editado com o Claude Code via [Power BI Modeling MCP](https://github.com/microsoft/powerbi-modeling-mcp).

### O que o visual HTML Content aceita (e o que não aceita)

Testado no Power BI Desktop:

| Recurso | Funciona? |
|---|---|
| CSS, `@keyframes`, `:hover` | ✅ |
| SVG inline, inclusive `<animate>` | ✅ |
| Imagem embutida (`data:image/...;base64`) em `<img>` ou fundo CSS, inclusive GIF/WebP animado | ✅ |
| `<video>` | ❌ removido |
| Imagens por URL externa (GitHub, CDN) | ❌ bloqueado |
| JavaScript | ❌ não executa |

Por isso, o fundo da capa é um **WebP animado embutido no próprio modelo**. Ele é convertido em base64 e fatiado em partes de 30 mil caracteres na tabela `dMidia`, porque o Power BI corta textos longos numa única célula. A medida `_URL Fundo Capa` junta as partes com `CONCATENATEX`.

## Como rodar

1. Clone o repositório e abra `pbi/LumaStore.pbip` no Power BI Desktop. Os recursos de PBIP e TMDL precisam estar habilitados.
2. Em *Transformar dados → Editar parâmetros*, aponte **`PastaDados`** para a pasta `dados\` do seu clone (com `\` no final).
3. Clique em **Atualizar**.
4. Instale o visual **HTML Content** pelo AppSource, caso ele não carregue.

### Regenerar os dados ou trocar o fundo

```bash
python scripts/gerar_base.py
python scripts/midia_para_pbi.py midia/seu_video.mp4 capa --inicio 0 --duracao 3.6 --pingpong --fps 10 --qualidade 32
```

O `midia_para_pbi.py` precisa do FFmpeg. Ele aceita `--crop` para recortar o quadro e avisa quando o WebP passa de ~1,5 MB.

## Estrutura

```
dados/        CSVs (vendas, produtos, clientes, mídia em base64)
midia/        WebP final do fundo da capa
pbi/          Projeto Power BI (PBIP + TMDL)
scripts/      Gerador da base, conversor de mídia, Power Query e DAX das páginas
```

## Ferramentas

Power BI Desktop · DAX · Power Query · HTML Content · Claude Code + Power BI Modeling MCP · Python · FFmpeg · Pippit AI (vídeo de fundo)
