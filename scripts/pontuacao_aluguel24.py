
import pandas as pd
from IPython.display import display



# Carregar os dados dos apartamentos a partir de um arquivo CSV ou Excel
df_apartamentos = pd.read_csv('User/rafaelinacio/projects/ranking_alugar_casa/scripts/apartamentos.csv')

# Exibindo o DataFrame original
display(df_apartamentos)

#%%

# Importando a biblioteca geopy para buscar coordenadas de um bairro
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapi")

# Função para buscar coordenadas de um bairro
def buscar_coordenadas(bairro):
    location = geolocator.geocode(bairro + ", São Paulo, Brazil")
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

df_apartamentos['LatLong Imovel'] = df_apartamentos['Bairro'].apply(buscar_coordenadas)


# # Exibindo o DataFrame com as coordenadas
# display(df_apartamentos)


# Importando a biblioteca geopy para calcular a distância entre dois pontos 
from geopy.distance import geodesic

def calcular_distancia_robusta(linha):
    coords_trabalho = (-23.6842, -46.6802)
    localizacao = linha['LatLong Imovel']

    if pd.notnull(localizacao):
        return geodesic(localizacao, coords_trabalho).km
    else:
        return None
    
df_apartamentos['Distância Interlagos (km)'] = df_apartamentos.apply(calcular_distancia_robusta, axis=1)

# Exibindo o DataFrame com as distâncias
# display(df_apartamentos)



# Função para calcular a pontuação com as regras
def calcular_pontuacao_atualizada(apartamento):
    # Critério 1: Preço Total (30%)
    if apartamento["Valor Total Mensal (R$)"] < 4500:
        pontos_preco = 10 + ((4500 - apartamento["Valor Total Mensal (R$)"]) // 100) * 10
    elif apartamento["Valor Total Mensal (R$)"] > 4500:
        pontos_preco = -((apartamento["Valor Total Mensal (R$)"] - 4500) // 200) * 10
    else:
        pontos_preco = 0

    # Critério 2: Distância até Interlagos (20%)
    if apartamento["Distância Interlagos (km)"] < 15:
        pontos_distancia = 5 + ((15 - apartamento["Distância Interlagos (km)"]) // 2) * 5
    else:
        pontos_distancia = -(apartamento["Distância Interlagos (km)"] - 15) // 2 * 5

    # Critério 3: Número de Quartos (parte de 10%)
    pontos_quartos = (apartamento["Quartos"] - 2) * 5 if apartamento["Quartos"] > 2 else 0

    # Critério 4: Banheiros (parte de 10%)
    pontos_banheiros = (apartamento["Banheiros"] - 2) * 3 if apartamento["Banheiros"] > 2 else 0

    # Critério 5: Vagas (parte de 8%)
    pontos_vagas = apartamento["Vagas"] * 2 if apartamento["Vagas"] > 0 else 0

    # Critério 6: Área do Apartamento (10%)
    if apartamento["Área (m²)"] >= 75:
        pontos_area = 1 + ((apartamento["Área (m²)"] - 75) // 10) * 2
    else:
        pontos_area = -1 - ((75 - apartamento["Área (m²)"]) // 10) * 2

    # Critério 7: Facilidades (5%)
    num_facilidades = len(apartamento["Facilidades"].split(", "))
    pontos_facilidades = 2 * num_facilidades

    # Critério 8: Fonte (7%)
    pontos_fonte = 10 if "quintoandar" in apartamento["Imobiliária"].lower() else 0
    
    # Calculando a pontuação total (aplicando os pesos)
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
        "Pontos Preço": pontos_preco,
        "Pontos Distância": pontos_distancia,
        "Pontos Quartos": pontos_quartos,
        "Pontos Banheiros": pontos_banheiros,
        "Pontos Vagas": pontos_vagas,
        "Pontos Área": pontos_area,
        "Pontos Facilidades": pontos_facilidades,
        "Pontos Fonte": pontos_fonte,
        "Pontuação Total": pontuacao_total
    }



# Aplicando a função de pontuação atualizada para cada apartamento
df_pontuacao = df_apartamentos.apply(calcular_pontuacao_atualizada, axis=1, result_type="expand")

# Combinando a planilha original com a de pontuação
df_apartamentos_pontuacao = pd.concat([df_pontuacao, df_apartamentos], axis=1)

# Ordenando a planilha pela pontuação total (maior para menor) e colocando a coluna "Pontuação Total" no início
df_apartamentos_pontuacao = df_apartamentos_pontuacao.sort_values(by="Pontuação Total", ascending=False).reset_index(drop=True)
df_apartamentos_pontuacao = df_apartamentos_pontuacao[["Pontuação Total"] + [col for col in df_apartamentos_pontuacao.columns if col != "Pontuação Total"]]

# Exibindo as primeiras linhas do DataFrame com as pontuações
#df_apartamentos_pontuacao.head()


# Salvando a planilha atualizada
df_apartamentos_pontuacao.to_csv('lista_de_imoveis_pontuados.csv', index=False)


ranking_apartamentos = df_apartamentos_pontuacao.sort_values(by='Pontuação Total', ascending=False)[['Pontuação Total','Nome/Endereço', 'Valor Total Mensal (R$)', 'Bairro','Fonte (site)','Código']]

# Adicionando a coluna de rank
ranking_apartamentos['Rank'] = range(1, len(ranking_apartamentos) + 1)

ranking_apartamentos.to_csv('/Users/rafaelinacio/projects/ranking_alugar_casa/data/ranking_apartamentos.csv', index=False)



