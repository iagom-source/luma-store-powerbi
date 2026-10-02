"""
Gera a base fictícia da LUMA Store (e-commerce de casa & decoração), 2023-2025.

História embutida nos dados ("O custo do frete grátis"):
  - Em 01/03/2024 a LUMA lança frete grátis para pedidos >= R$ 199.
  - O volume de pedidos sobe, mas o frete passa a sair do bolso da empresa.
  - O Marketplace cresce rápido, cobra comissão de 16% e tem o dobro de devoluções.
  - Resultado: a receita cresce, mas a margem de contribuição encolhe.

Saída (CSV UTF-8, separador ",", decimal "."):
  dados/dProduto.csv, dados/dCliente.csv, dados/fVendas.csv
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)
OUT = Path(__file__).resolve().parent.parent / "dados"
OUT.mkdir(exist_ok=True)

INICIO, FIM = date(2023, 1, 1), date(2025, 12, 31)
LANC_FRETE_GRATIS = date(2024, 3, 1)
FRETE_MINIMO = 199.0

# ---------------------------------------------------------------- Produtos
CATEGORIAS = {
    # categoria: (faixa de preço, margem bruta típica, peso de venda, marcas)
    "Móveis":       ((390, 2400), 0.38, 0.12, ["Casa Viva", "Madeirar"]),
    "Decoração":    ((39, 290),   0.58, 0.26, ["Atelier Sul", "Ponto Raro"]),
    "Cama & Banho": ((59, 420),   0.52, 0.20, ["Algodão Bom", "Sono Leve"]),
    "Cozinha":      ((29, 520),   0.45, 0.22, ["Panela Feliz", "Mesa Posta"]),
    "Iluminação":   ((69, 890),   0.50, 0.12, ["Luz & Cia", "Atelier Sul"]),
    "Jardim":       ((25, 380),   0.48, 0.08, ["Verde Casa", "Ponto Raro"]),
}
NOMES = {
    "Móveis": ["Rack Nórdico", "Mesa Lateral Oslo", "Poltrona Bossa", "Aparador Ripado",
               "Cadeira Eames Off-white", "Estante Modular", "Banqueta Alta Pinus", "Escrivaninha Compacta"],
    "Decoração": ["Vaso Cerâmica Areia", "Quadro Abstrato 60x90", "Espelho Redondo 70cm", "Cesto Fibra Natural",
                  "Vela Aromática Cedro", "Almofada Linho", "Tapete Sisal 1,5m", "Bandeja Espelhada",
                  "Escultura Mãos", "Relógio de Parede Minimal"],
    "Cama & Banho": ["Jogo de Lençol 300 fios", "Edredom Queen Pluma", "Toalha Banhão Algodão Egípcio",
                     "Kit Travesseiros Nasa", "Manta Tricot", "Roupão Waffle", "Tapete de Banho Bolinhas"],
    "Cozinha": ["Jogo de Panelas Cerâmica", "Faqueiro Inox 24pç", "Aparelho de Jantar 20pç", "Cafeteira Prensa Francesa",
                "Tábua de Corte Teca", "Jogo de Taças Cristal", "Pote Hermético Kit 5", "Air Fryer 4L"],
    "Iluminação": ["Luminária de Piso Arco", "Pendente Cúpula Rattan", "Abajur Cerâmica", "Fita LED 5m Smart",
                   "Arandela Industrial", "Lâmpada Filamento Vintage"],
    "Jardim": ["Vaso Autoirrigável", "Kit Jardinagem 5pç", "Cachepot Cimento", "Horta Vertical",
               "Regador Metal", "Ombrelone 2m"],
}

produtos = []
pid = 1
for cat, (faixa, margem, _, marcas) in CATEGORIAS.items():
    for nome in NOMES[cat]:
        preco = round(random.uniform(*faixa), 2)
        preco = round(preco - (preco % 1) + 0.90, 2)  # preços terminados em ,90
        custo = round(preco * (1 - random.uniform(margem - 0.08, margem + 0.08)), 2)
        produtos.append({
            "ID_Produto": f"P{pid:03d}", "Produto": nome, "Categoria": cat,
            "Marca": random.choice(marcas), "Preco_Lista": preco, "Custo_Unit": custo,
        })
        pid += 1

peso_prod = []
for p in produtos:
    peso_cat = CATEGORIAS[p["Categoria"]][2] / len(NOMES[p["Categoria"]])
    peso_prod.append(peso_cat * random.uniform(0.5, 1.6))

# ---------------------------------------------------------------- Clientes
UFS = [  # UF, região, peso, frete médio (custo p/ empresa)
    ("SP", "Sudeste", 30, 18), ("RJ", "Sudeste", 11, 22), ("MG", "Sudeste", 10, 24), ("ES", "Sudeste", 2, 26),
    ("PR", "Sul", 6, 25), ("SC", "Sul", 4, 27), ("RS", "Sul", 6, 29),
    ("BA", "Nordeste", 5, 36), ("PE", "Nordeste", 4, 38), ("CE", "Nordeste", 3, 40), ("RN", "Nordeste", 1, 42),
    ("GO", "Centro-Oeste", 3, 31), ("DF", "Centro-Oeste", 3, 30), ("MT", "Centro-Oeste", 1, 38),
    ("PA", "Norte", 2, 48), ("AM", "Norte", 1, 55),
]
FRETE_UF = {u[0]: u[3] for u in UFS}
FAIXAS = ["18-24", "25-34", "35-44", "45-54", "55+"]

clientes = []
for i in range(1, 18001):
    uf = random.choices(UFS, weights=[u[2] for u in UFS])[0]
    cad = INICIO - timedelta(days=400) + timedelta(days=int(random.betavariate(1.4, 1.1) * 1500))
    clientes.append({
        "ID_Cliente": f"C{i:05d}", "UF": uf[0], "Regiao": uf[1],
        "Faixa_Etaria": random.choices(FAIXAS, weights=[10, 32, 28, 18, 12])[0],
        "Data_Cadastro": min(cad, FIM).isoformat(),
    })

# ---------------------------------------------------------------- Vendas
SAZON = {1: 0.85, 2: 0.80, 3: 0.92, 4: 0.95, 5: 1.12, 6: 0.98,
         7: 0.95, 8: 1.00, 9: 0.97, 10: 1.05, 11: 1.65, 12: 1.45}
BASE_DIA = 38  # pedidos/dia em jan/2023


def canal_para(d: date) -> str:
    # Marketplace ganha espaço ao longo do tempo
    t = (d - INICIO).days / (FIM - INICIO).days
    pm = 0.18 + 0.22 * t
    return random.choices(["Site", "App", "Marketplace"], weights=[0.55 - pm / 2, 0.45 - pm / 2, pm])[0]


linhas = []
pedido = 0
d = INICIO
while d <= FIM:
    t_anos = (d - INICIO).days / 365
    efeito_frete = 1.18 if d >= LANC_FRETE_GRATIS else 1.0
    bf = 2.6 if (d.month == 11 and 22 <= d.day <= 30) else 1.0
    lam = BASE_DIA * (1.14 ** t_anos) * SAZON[d.month] * efeito_frete * bf * (1.08 if d.weekday() < 5 else 0.9)
    n_ped = max(0, int(random.gauss(lam, lam ** 0.5)))

    for _ in range(n_ped):
        pedido += 1
        cli = random.choice(clientes)
        canal = canal_para(d)
        n_itens = random.choices([1, 2, 3, 4], weights=[62, 25, 9, 4])[0]
        itens = random.choices(produtos, weights=peso_prod, k=n_itens)

        promo = 0.0
        if d.month == 11 and d.day >= 20:
            promo = random.choice([0.10, 0.15, 0.20, 0.25])
        elif random.random() < 0.22:
            promo = random.choice([0.05, 0.10, 0.15])

        brutos = []
        for p in itens:
            qtd = random.choices([1, 2, 3], weights=[80, 15, 5])[0]
            preco = round(p["Preco_Lista"] * (1 + 0.045 * t_anos), 2)  # reajuste anual
            brutos.append((p, qtd, preco))
        total_ped = sum(q * pr * (1 - promo) for _, q, pr in brutos)

        frete_custo_ped = FRETE_UF[cli["UF"]] * random.uniform(0.8, 1.3) * (1 + 0.25 * (n_itens - 1))
        if any(p["Categoria"] == "Móveis" for p, _, _ in brutos):
            frete_custo_ped *= 2.4
        frete_gratis = d >= LANC_FRETE_GRATIS and total_ped >= FRETE_MINIMO and canal != "Marketplace"
        frete_cobrado_ped = 0.0 if frete_gratis else frete_custo_ped * random.uniform(0.85, 1.05)
        if canal == "Marketplace":  # marketplace subsidia parte do frete
            frete_cobrado_ped = frete_custo_ped * 0.9

        taxa_dev = {"Site": 0.045, "App": 0.04, "Marketplace": 0.11}[canal]
        prazo = max(1, int(random.gauss(5 + FRETE_UF[cli["UF"]] / 8, 2)))

        for idx, (p, qtd, preco) in enumerate(brutos, start=1):
            bruto = round(qtd * preco, 2)
            desc_val = round(bruto * promo, 2)
            liq = round(bruto - desc_val, 2)
            share = liq / total_ped if total_ped else 1 / n_itens
            r = random.random()
            status = "Cancelado" if r < 0.025 else ("Devolvido" if r < 0.025 + taxa_dev else "Entregue")
            linhas.append({
                "ID_Pedido": f"PD{pedido:07d}", "Item": idx, "Data_Pedido": d.isoformat(),
                "ID_Cliente": cli["ID_Cliente"], "ID_Produto": p["ID_Produto"], "Canal": canal,
                "Qtd": qtd, "Preco_Unit": preco, "Desconto_Pct": promo,
                "Receita_Bruta": bruto, "Desconto_Valor": desc_val, "Receita_Liquida": liq,
                "CMV": round(qtd * p["Custo_Unit"] * (1 + 0.05 * t_anos), 2),
                "Frete_Cobrado": round(frete_cobrado_ped * share, 2),
                "Frete_Custo": round(frete_custo_ped * share, 2),
                "Comissao_Marketplace": round(liq * 0.16, 2) if canal == "Marketplace" else 0.0,
                "Frete_Gratis": "Sim" if frete_gratis else "Não",
                "Status": status, "Prazo_Entrega_Dias": prazo,
            })
    d += timedelta(days=1)


def salvar(nome, rows):
    with open(OUT / nome, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{nome}: {len(rows):,} linhas")


salvar("dProduto.csv", produtos)
salvar("dCliente.csv", clientes)
salvar("fVendas.csv", linhas)
