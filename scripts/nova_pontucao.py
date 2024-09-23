# %%
import pandas as pd
from google.cloud import bigquery
import os
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from dotenv import load_dotenv


# %%
# import google.auth

# # Verifica a conta de serviço atual
# credentials, project = google.auth.default()
# print(f"Usando a conta de serviço: {credentials.service_account_email}")
# print(f"Projeto: {project}")

# %%
# Inicializar o cliente BigQuery usando as credenciais do arquivo .env
client = bigquery.Client()

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter o caminho do arquivo CSV a partir das variáveis de ambiente
csv_path = os.getenv('CSV_FILE_PATH')

df_apartamentos = pd.read_csv(csv_path)

# Limpar e verificar dados (strip para colunas e dados)
df_apartamentos.columns = df_apartamentos.columns.str.strip()
df_apartamentos = df_apartamentos.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Renomear as colunas do CSV para corresponder às colunas do BigQuery
df_apartamentos = df_apartamentos.rename(columns={
    "Código": "Codigo",
    "Nome/Endereço": "Nome_Endereco",
    "Bairro": "Bairro",
    "Valor Total Mensal (R$)": "Valor_Total_Mensal",
    "Preço do Aluguel (R$)": "Preco_Aluguel",
    "Condomínio (R$)": "Condominio",
    "IPTU (R$)": "IPTU",
    "Quartos": "Quartos",
    "Banheiros": "Banheiros",
    "Vagas": "Vagas",
    "Área (m²)": "Area",
    "Facilidades": "Facilidades",
    "Imobiliária": "Imobiliaria",
    "Fonte (site)": "Fonte"
})

# %%
# Verificar se o apartamento já existe no BigQuery pela coluna 'Fonte' na tabela 'apartamentos'
query_apartamentos = """
SELECT Fonte FROM `rafael-data.ranking_apartamentos_flask.apartamentos`
"""
existing_apartments = client.query(query_apartamentos).to_dataframe()

# Verificar se os registros da tabela 'lista_de_imoveis_pontuados' já foram pontuados
query_lista_pontuados = """
SELECT Fonte FROM `rafael-data.ranking_apartamentos_flask.lista_de_imoveis_pontuados`
"""
existing_pontuados = client.query(query_lista_pontuados).to_dataframe()

# Filtrar os apartamentos que não estão na tabela 'apartamentos'
new_apartments = df_apartamentos[~df_apartamentos['Fonte'].isin(existing_apartments['Fonte'])]

# Filtrar os apartamentos que ainda não foram pontuados na tabela 'lista_de_imoveis_pontuados'
new_apartments = new_apartments[~new_apartments['Fonte'].isin(existing_pontuados['Fonte'])]

# Verifique se há novos apartamentos para processar
if not new_apartments.empty:
    # Carregar os novos apartamentos na tabela 'apartamentos' do BigQuery
    job = client.load_table_from_dataframe(new_apartments, 'rafael-data.ranking_apartamentos_flask.apartamentos')
    job.result()  # Espera o job de carregamento terminar

    # Ler a tabela atualizada 'apartamentos' do BigQuery de volta como DataFrame
    df_apartamentos_bq = client.query("SELECT * FROM `rafael-data.ranking_apartamentos_flask.apartamentos`").to_dataframe()

#     # Mostrar o DataFrame atualizado
#     print(df_apartamentos_bq.head())
# else:
#     print("Nenhum novo apartamento para processar.")

# %%
# Configurações de colunas com base no BigQuery
nome_coluna_codigo = 'Codigo'
nome_coluna_nome_endereco = 'Nome_Endereco'
nome_coluna_bairro = 'Bairro'
nome_coluna_valor_total_mensal = 'Valor_Total_Mensal'
nome_coluna_preco_aluguel = 'Preco_Aluguel'
nome_coluna_condominio = 'Condominio'
nome_coluna_iptu = 'IPTU'
nome_coluna_quartos = 'Quartos'
nome_coluna_banheiros = 'Banheiros'
nome_coluna_vagas = 'Vagas'
nome_coluna_area = 'Area'
nome_coluna_facilidades = 'Facilidades'
nome_coluna_imobiliaria = 'Imobiliaria'
nome_coluna_fonte = 'Fonte'  # Nome da coluna no BigQuery que armazena o link do site do apartamento
nome_coluna_latlong = 'LatLong'
nome_coluna_distancia_interlagos = 'Distancia_Interlagos'

# %%
geolocator = Nominatim(user_agent="geoapi")

# Função para buscar coordenadas de um bairro
def buscar_coordenadas(bairro):
    location = geolocator.geocode(bairro + ", São Paulo, Brazil")
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Aplicando coordenadas no DataFrame
df_apartamentos[nome_coluna_latlong] = df_apartamentos[nome_coluna_bairro].apply(buscar_coordenadas)

# %%
# Função para calcular a distância entre o apartamento e o trabalho (Interlagos)
def calcular_distancia_robusta(linha):
    coords_trabalho = (-23.6842, -46.6802)
    localizacao = linha[nome_coluna_latlong]

    if pd.notnull(localizacao):
        return geodesic(localizacao, coords_trabalho).km
    else:
        return None

df_apartamentos[nome_coluna_distancia_interlagos] = df_apartamentos.apply(calcular_distancia_robusta, axis=1)

# %%
# Função para calcular pontuações no DataFrame
def calcular_pontuacoes(df):
    df['Pontuacao_Total'] = (df['Pontos_Preco'] + df['Pontos_Distancia'] +
                             df['Pontos_Quartos'] + df['Pontos_Banheiros'] +
                             df['Pontos_Vagas'] + df['Pontos_Area'] +
                             df['Pontos_Facilidades'] + df['Pontos_Fonte'])
    return df

# Função para calcular a pontuação atualizada para cada apartamento
def calcular_pontuacao_atualizada(apartamento):
    # Critério 1: Preço Total (30%)
    if apartamento[nome_coluna_valor_total_mensal] < 4500:
        pontos_preco = 10 + ((4500 - apartamento[nome_coluna_valor_total_mensal]) // 100) * 10
    elif apartamento[nome_coluna_valor_total_mensal] > 4500:
        pontos_preco = -((apartamento[nome_coluna_valor_total_mensal] - 4500) // 200) * 10
    else:
        pontos_preco = 0

    # Critério 2: Distância até Interlagos (20%)
    if apartamento[nome_coluna_distancia_interlagos] < 15:
        pontos_distancia = 5 + ((15 - apartamento[nome_coluna_distancia_interlagos]) // 2) * 5
    else:
        pontos_distancia = -(apartamento[nome_coluna_distancia_interlagos] - 15) // 2 * 5

    # Critério 3: Número de Quartos (parte de 10%)
    pontos_quartos = (apartamento[nome_coluna_quartos] - 2) * 5 if apartamento[nome_coluna_quartos] > 2 else 0

    # Critério 4: Banheiros (parte de 10%)
    pontos_banheiros = (apartamento[nome_coluna_banheiros] - 2) * 3 if apartamento[nome_coluna_banheiros] > 2 else 0

    # Critério 5: Vagas (parte de 8%)
    pontos_vagas = apartamento[nome_coluna_vagas] * 2 if apartamento[nome_coluna_vagas] > 0 else 0

    # Critério 6: Área do Apartamento (10%)
    if apartamento[nome_coluna_area] >= 75:
        pontos_area = 1 + ((apartamento[nome_coluna_area] - 75) // 10) * 2
    else:
        pontos_area = -1 - ((75 - apartamento[nome_coluna_area]) // 10) * 2

    # Critério 7: Facilidades (5%)
    num_facilidades = len(apartamento[nome_coluna_facilidades].split(", "))
    pontos_facilidades = 2 * num_facilidades

    # Critério 8: Fonte (7%)
    apartamento[nome_coluna_imobiliaria] = apartamento[nome_coluna_imobiliaria].lower()
    pontos_fonte = 15 if "quintoandar" in apartamento[nome_coluna_imobiliaria].lower() else 0

    # Calculando a pontuação total
    pontuacao_total = (
        (pontos_preco * 0.3) +
        (pontos_distancia * 0.2) +
        (pontos_quartos * 0.1) +
        (pontos_banheiros * 0.1) +
        (pontos_vagas * 0.08) +
        (pontos_area * 0.1) +
        (pontos_facilidades * 0.05) +
        (pontos_fonte * 0.07)
    )

    return {
        "Pontos_Preco": pontos_preco,
        "Pontos_Distancia": pontos_distancia,
        "Pontos_Quartos": pontos_quartos,
        "Pontos_Banheiros": pontos_banheiros,
        "Pontos_Vagas": pontos_vagas,
        "Pontos_Area": pontos_area,
        "Pontos_Facilidades": pontos_facilidades,
        "Pontos_Fonte": pontos_fonte,
        "Pontuacao_Total": pontuacao_total
    }

# Aplicar a função calcular_pontuacao_atualizada no DataFrame
def aplicar_pontuacao(df):
    pontuacoes = df.apply(calcular_pontuacao_atualizada, axis=1)
    pontuacoes_df = pd.DataFrame(pontuacoes.tolist(), index=df.index)  # Converter para DataFrame
    return pd.concat([df, pontuacoes_df], axis=1)  # Concatenar o DataFrame original com as pontuações

# Aplicar as pontuações ao DataFrame
df_apartamentos = aplicar_pontuacao(df_apartamentos)

# Agora, calcular a pontuação total com a função calcular_pontuacoes
df_pontuado = calcular_pontuacoes(df_apartamentos)

# Exibir o DataFrame final (caso necessário)
# display(df_pontuado)

# %%
# Variável para identificar a tabela 'lista_de_imoveis_pontuados'
lista_de_imoveis_table_id = 'rafael-data.ranking_apartamentos_flask.lista_de_imoveis_pontuados'

# Preencher NaN e converter tipos
df_pontuado.fillna({
    'Pontuacao_Total': 0,
    'Pontos_Preco': 0,
    'Pontos_Distancia': 0,
    'Pontos_Quartos': 0,
    'Pontos_Banheiros': 0,
    'Pontos_Vagas': 0,
    'Pontos_Area': 0,
    'Pontos_Facilidades': 0,
    'Pontos_Fonte': 0
}, inplace=True)

df_pontuado = df_pontuado.astype({
    'Pontuacao_Total': 'float',
    'Pontos_Preco': 'float',
    'Pontos_Distancia': 'float',
    'Pontos_Quartos': 'float',
    'Pontos_Banheiros': 'float',
    'Pontos_Vagas': 'float',
    'Pontos_Area': 'float',
    'Pontos_Facilidades': 'float',
    'Pontos_Fonte': 'float',
    'Codigo': 'int',
    'Quartos': 'int',
    'Banheiros': 'int',
    'Vagas': 'int',
    'Area': 'float'
})

# Variável para contar o número de linhas inseridas
linhas_inseridas = 0

# Loop para inserir os novos apartamentos na tabela 'lista_de_imoveis_pontuados'
for index, row in df_pontuado.iterrows():
    insert_query = f"""
    INSERT INTO `{lista_de_imoveis_table_id}` (
        Pontuacao_Total, Pontos_Preco, Pontos_Distancia, Pontos_Quartos, 
        Pontos_Banheiros, Pontos_Vagas, Pontos_Area, Pontos_Facilidades, 
        Pontos_Fonte, Codigo, Nome_Endereco, Bairro, Valor_Total_Mensal, 
        Preco_Aluguel, Condominio, IPTU, Quartos, Banheiros, Vagas, Area, 
        Facilidades, Imobiliaria, Fonte, LatLong, Distancia_Interlagos
    )
    VALUES (
        {row['Pontuacao_Total']}, {row['Pontos_Preco']}, {row['Pontos_Distancia']}, 
        {row['Pontos_Quartos']}, {row['Pontos_Banheiros']}, {row['Pontos_Vagas']}, 
        {row['Pontos_Area']}, {row['Pontos_Facilidades']}, {row['Pontos_Fonte']}, 
        {row['Codigo']}, '{row['Nome_Endereco']}', '{row['Bairro']}', 
        {row['Valor_Total_Mensal']}, {row['Preco_Aluguel']}, {row['Condominio']}, 
        {row['IPTU']}, {row['Quartos']}, {row['Banheiros']}, {row['Vagas']}, 
        {row['Area']}, '{row['Facilidades']}', '{row['Imobiliaria']}', 
        '{row['Fonte']}', '{row['LatLong']}', {row['Distancia_Interlagos']}
    )
    """
    client.query(insert_query)
    linhas_inseridas += 1

# Imprimir o total de linhas inseridas
print(f"Total de {linhas_inseridas} apartamentos inseridos na tabela 'lista_de_imoveis_pontuados'.")

# %%
# Definir o nome da tabela 'ranking_apartamentos'
table_id = 'rafael-data.ranking_apartamentos_flask.ranking_apartamentos'

# Apagar a tabela se ela já existir para recriá-la
client.delete_table(table_id, not_found_ok=True)
print(f"Tabela {table_id} excluída, se existia.")

# Definir o schema da tabela incluindo a nova coluna RANK
schema = [
    bigquery.SchemaField(nome_coluna_codigo, "INT64"),
    bigquery.SchemaField(nome_coluna_nome_endereco, "STRING"),
    bigquery.SchemaField(nome_coluna_bairro, "STRING"),
    bigquery.SchemaField(nome_coluna_valor_total_mensal, "FLOAT64"),
    bigquery.SchemaField(nome_coluna_fonte, "STRING"),
    bigquery.SchemaField("Pontuacao_Total", "FLOAT64"),
    bigquery.SchemaField("rank", "INT64")  # Nova coluna de rank
]

# Recriar a tabela com o novo schema
table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)
print(f"Tabela {table_id} recriada.")

# Ordenar o DataFrame por 'Pontuacao_Total' de forma decrescente
df_pontuado = df_pontuado.sort_values(by='Pontuacao_Total', ascending=False)

# Calcular e adicionar a coluna de ranking ao DataFrame
df_pontuado['rank'] = df_pontuado['Pontuacao_Total'].rank(method='first', ascending=False).astype(int)

# Inserir os dados na tabela recriada
rows_to_insert = [
    {
        nome_coluna_codigo: row[nome_coluna_codigo],
        nome_coluna_nome_endereco: row[nome_coluna_nome_endereco],
        nome_coluna_bairro: row[nome_coluna_bairro],
        nome_coluna_valor_total_mensal: row[nome_coluna_valor_total_mensal],
        nome_coluna_fonte: row[nome_coluna_fonte],
        'Pontuacao_Total': row['Pontuacao_Total'],
        'rank': row['rank']
    }
    for index, row in df_pontuado.iterrows()
]

# Inserir os dados no BigQuery
errors = client.insert_rows_json(table_id, rows_to_insert)

# Verificar se houve erros
if errors == []:
    print(f"Total de apartamentos inseridos: {len(rows_to_insert)}")
    print("Dados inseridos com sucesso!")
else:
    print(f"Erros encontrados ao inserir os dados: {errors}")


