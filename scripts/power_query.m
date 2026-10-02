// ============================================================
// LUMA Store — consultas Power Query (cole cada uma numa
// "Consulta Nula" > Editor Avançado, com o nome indicado)
// Os CSVs usam ponto como decimal, por isso a cultura "en-US".
// PastaDados = parâmetro do Power Query com a pasta dos CSVs (termina com \).
// ============================================================

// ---------- Consulta: dProduto ----------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "dProduto.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cabecalho, {
        {"ID_Produto", type text}, {"Produto", type text}, {"Categoria", type text}, {"Marca", type text},
        {"Preco_Lista", type number}, {"Custo_Unit", type number}
    }, "en-US")
in
    Tipos

// ---------- Consulta: dCliente ----------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "dCliente.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cabecalho, {
        {"ID_Cliente", type text}, {"UF", type text}, {"Regiao", type text},
        {"Faixa_Etaria", type text}, {"Data_Cadastro", type date}
    }, "en-US")
in
    Tipos

// ---------- Consulta: fVendas ----------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "fVendas.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cabecalho, {
        {"ID_Pedido", type text}, {"Item", Int64.Type}, {"Data_Pedido", type date},
        {"ID_Cliente", type text}, {"ID_Produto", type text}, {"Canal", type text},
        {"Qtd", Int64.Type}, {"Preco_Unit", type number}, {"Desconto_Pct", type number},
        {"Receita_Bruta", type number}, {"Desconto_Valor", type number}, {"Receita_Liquida", type number},
        {"CMV", type number}, {"Frete_Cobrado", type number}, {"Frete_Custo", type number},
        {"Comissao_Marketplace", type number}, {"Frete_Gratis", type text}, {"Status", type text},
        {"Prazo_Entrega_Dias", Int64.Type}
    }, "en-US")
in
    Tipos
