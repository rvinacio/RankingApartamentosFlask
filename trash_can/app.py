import pandas as pd
from flask import Flask, render_template_string

# Crie o app Flask
app = Flask(__name__)

# Função para ler o arquivo CSV e preparar os dados
def ler_csv():
    df = pd.read_csv('files/ranking_apartamentos.csv')
    # Ordena os dados por pontuação total
    df_sorted = df.sort_values(by="Pontuação Total", ascending=False)
    return df_sorted

# Template HTML para exibir o ranking
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ranking de Imóveis</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
        }
        h1 {
            text-align: center;
            margin-top: 20px;
            color: #343a40;
        }
        table {
            margin: 20px auto;
            border-collapse: collapse;
            width: 90%;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 12px;
            text-align: center;
        }
        th {
            background-color: #343a40;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #ddd;
        }
    </style>
    <!-- Adicionar DataTables CSS -->
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.css">
</head>
<body>
    <h1>Ranking de Imóveis</h1>
    <table id="tabela_imoveis" class="display">
        <thead>
            <tr>
                <th>Rank</th>
                <th>Nome/Endereço</th>
                <th>Bairro</th>
                <th>Valor Total (R$)</th>
                <th>Pontuação Total</th>
            </tr>
        </thead>
        <tbody>
            {% for index, row in dados.iterrows() %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ row['Nome/Endereço'] }}</td>
                <td>{{ row['Bairro'] }}</td>
                <td>{{ row['Valor Total Mensal (R$)'] }}</td>
                <td>{{ row['Pontuação Total'] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <!-- Adicionar jQuery e DataTables JavaScript -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.js"></script>
    
    <!-- Inicializar DataTables -->
    <script>
        $(document).ready( function () {
            $('#tabela_imoveis').DataTable();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def mostrar_ranking():
    # Lê os dados do CSV
    dados = ler_csv()
    # Renderiza o HTML com os dados
    return render_template_string(html_template, dados=dados)

if __name__ == '__main__':
    app.run(debug=True)