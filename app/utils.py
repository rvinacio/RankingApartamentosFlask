import pandas as pd

# função para pegar o caminho base do csv
def get_caminho_base_csv():
    env = 1  # <<<  env 1 = local // env 2 = produção
    if env == 1:
        return '/Users/rafaelinacio/projects/ranking_alugar_casa/data/'
    else:
        return '/home/rvinacio/aluguel/data/'

# definição do caminho dos arquivos
def get_caminho_csv(param):
    caminho_ambiente = get_caminho_base_csv()
    caminho_ranking = f'{caminho_ambiente}ranking_apartamentos.csv'
    caminho_desconsiderados = f'{caminho_ambiente}apartamentos_desconsiderados.csv'
    if param == 'ranking':
        return caminho_ranking
    else:
        return caminho_desconsiderados


# # função para ler os arquivos csv
# def ler_csv():
#     df_ranking = pd.read_csv(get_caminho_csv('ranking'))
#     df_desconsiderados = pd.read_csv(get_caminho_csv('desconsiderados'))
#     df_ranking_filtered = df_ranking[~df_ranking['Código']].isin(df_desconsiderados['Código'])
#     df_ranking_sorted = df_ranking_filtered.sort_values(by="Pontuação Total", ascending=False)
#     return df_ranking_sorted, df_desconsiderados

# Função para ler os arquivos CSV
def ler_csv():
    # Lê os CSVs
    df_ranking = pd.read_csv(get_caminho_csv('ranking'))
    df_desconsiderados = pd.read_csv(get_caminho_csv('desconsiderados'))
    
    # Retira espaço em branco do nome das colunas
    df_ranking.columns = df_ranking.columns.str.strip()
    df_desconsiderados.columns = df_desconsiderados.columns.str.strip()

    # Filtra os itens que estão no desconsiderados
    df_ranking_filtered = df_ranking[~df_ranking['Código'].isin(df_desconsiderados['Código'])]
    
    # Ordena o DataFrame filtrado pela 'Pontuação Total' em ordem decrescente
    df_ranking_sorted = df_ranking_filtered.sort_values(by="Pontuação Total", ascending=False)
    
    return df_ranking_sorted, df_desconsiderados

# fluxo para retirar imóveis do ranking
def remover_imovel(codigos):
    # Converte códigos para inteiros (se eles são armazenados como inteiros no CSV)
    codigos_int = [int(codigo) for codigo in codigos]

    df_ranqueados = pd.read_csv(get_caminho_csv('ranking'))
    df_desconsiderados = pd.read_csv(get_caminho_csv('desconsiderados'))

    # Identifica os imóveis a serem removidos usando a lista de inteiros
    imoveis_removidos = df_ranqueados[df_ranqueados['Código'].isin(codigos_int)]

    # Remove os imóveis do DataFrame de ranqueados
    df_ranqueados = df_ranqueados[~df_ranqueados['Código'].isin(codigos_int)]
    df_ranqueados.sort_values(by='Pontuação Total', ascending=False, inplace=True)
    df_ranqueados['Rank'] = range(1, len(df_ranqueados) + 1)

    # Adiciona os imóveis removidos ao DataFrame de desconsiderados
    df_desconsiderados = pd.concat([df_desconsiderados, imoveis_removidos])

    # Salva os CSVs atualizados
    df_ranqueados.to_csv(get_caminho_csv('ranking'), index=False)
    df_desconsiderados.to_csv(get_caminho_csv('desconsiderados'), index=False)



# Fluxo para reinserir imóveis no ranking
def reconsiderar_imovel(ids):
    # Converte ids para inteiros, se estiverem como strings
    ids_int = [int(id) for id in ids]
    
    # Carrega o CSV de desconsiderados
    df_desconsiderados = pd.read_csv(get_caminho_csv('desconsiderados'))

    # Encontra os imóveis a serem reconsiderados
    imoveis_reconsiderados = df_desconsiderados[df_desconsiderados['Código'].isin(ids_int)]

    # Remove os imóveis reconsiderados do DataFrame de desconsiderados
    df_desconsiderados = df_desconsiderados[~df_desconsiderados['Código'].isin(ids_int)]
    # Salva o CSV atualizado de desconsiderados
    df_desconsiderados.to_csv(get_caminho_csv('desconsiderados'), index=False)

    # Carrega o CSV de ranqueados
    df_ranqueados = pd.read_csv(get_caminho_csv('ranking'))

    # Adiciona os imóveis reconsiderados ao DataFrame de ranqueados
    df_ranqueados = pd.concat([df_ranqueados, imoveis_reconsiderados], ignore_index=True)
    # Re-classifica o rank
    df_ranqueados.sort_values(by='Pontuação Total', ascending=False, inplace=True)
    df_ranqueados['Rank'] = range(1, len(df_ranqueados) + 1)

    # Salva o CSV atualizado de ranqueados
    df_ranqueados.to_csv(get_caminho_csv('ranking'), index=False)


