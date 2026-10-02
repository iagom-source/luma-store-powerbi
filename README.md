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

De cada R$ 100 vendidos, o frete subsidiado e a comissão do marketplace passaram a levar **R$ 4,9 a mais**. O canal Marketplace tem margem de 24,8%, contra cerca de 37% no site e no app.

Por categoria, a história fica mais sutil:
- **Todas as categorias perderam de 4,5 a 6,4 p.p. de margem.**
- **Móveis responde por 38% da margem que não entrou** porque é a maior categoria (41% da receita), não porque caiu mais.
- **Os itens baratos pagam o frete mais caro:** Decoração gasta R$ 4,4 de frete a cada R$ 100 vendidos, quase o dobro de Móveis (R$ 2,5).

## Páginas

| Página | Medida | O que mostra |
|---|---|---|
| Capa | `HTML Capa` | Fundo animado (WebP embutido), manchete, 3 KPIs dinâmicos e botões de navegação |
| Diagnóstico | `HTML Diagnostico` + `_CSS Diagnostico` | KPIs com verso (giram no hover e mostram definição + contexto), gráfico mensal com anotações de Black Friday, mosaicos de "cada R$ 100" (2023 × 2025), canais e ações |
| Categorias | `HTML Categorias` + `_CSS Categorias` | Barras com marcador (margem atual × tracinho da margem de 2023), frete subsidiado a cada R$ 100 e faixa de conclusão |

Os textos das páginas (manchetes, destaques, ações) são calculados pelo DAX, não digitados. As páginas são ligadas por botões desenhados no HTML, com botões nativos transparentes por cima.

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

### Truques que funcionaram

- **Escala proporcional:** com tamanhos em pixel, o texto fica minúsculo quando o visual é grande. A página define `--u: min(100vw / 1280, 100vh / 720)` e escreve tudo como `calc(var(--u) * N)`, então escala inteira como uma imagem.
- **Gráfico sem texto distorcido:** o SVG estica só as formas (`preserveAspectRatio='none'`, viewBox 1000×1000). Eixos, rótulos e tooltip ficam em HTML posicionado em %.
- **Card com verso nítido:** um card que *fica* girado em 3D sai borrado no Chrome. Por isso o card gira 0° → 90° → 0° e troca de face no meio, terminando sem rotação.
- **Listas:** o HTML Content tem estilo próprio para `<li>`, então o tamanho da fonte vai no próprio `<li>`, com `!important`.
- **CSS em medida separada:** ajustes visuais mexem só em `_CSS …`, sem reenviar a página inteira.

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

O `midia_para_pbi.py` precisa do FFmpeg. Ele aceita `--crop` para recortar o quadro e avisa quando o WebP passa de ~1,5 MB. Com `--still`, ele extrai um quadro parado em JPEG, usado nas faixas de abertura do Diagnóstico e das Categorias.

## Estrutura

```
dados/        CSVs (vendas, produtos, clientes, mídia em base64)
midia/        WebP do fundo da capa e fotos das faixas de abertura
pbi/          Projeto Power BI (PBIP + TMDL)
scripts/      Gerador da base, conversor de mídia, Power Query e DAX das páginas
```

## Ferramentas

Power BI Desktop · DAX · Power Query · HTML Content · Claude Code + Power BI Modeling MCP · Python · FFmpeg · Pippit AI (vídeo de fundo)
