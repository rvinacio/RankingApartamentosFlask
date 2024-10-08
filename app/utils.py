import os
from google.cloud import bigquery
from flask import jsonify
from google.auth import default

def get_bigquery_client():
    # Verifica se estÃ¡ rodando no Google App Engine (GAE_ENV serÃ¡ definido no App Engine)
    if os.getenv('GAE_ENV', '').startswith('standard'):
        # No App Engine, use as credenciais padrão automaticamente
        client = bigquery.Client()
    else:
        # Se estiver localmente, use o arquivo de credenciais definido pelo .env
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            client = bigquery.Client()
        else:
            raise EnvironmentError('GOOGLE_APPLICATION_CREDENTIALS não foi encontrada no ambiente.')
    
    return client

# Inicializa o cliente BigQuery com base no ambiente
client = get_bigquery_client()


# Função para buscar dados do ranking e desconsiderados
def get_ranking_data():
    query_ranqueados = """
        SELECT * FROM `rafael-data.ranking_apartamentos_flask.ranking_apartamentos`
        ORDER BY `Pontuacao_Total` DESC
    """
    query_desconsiderados = """
        SELECT * FROM `rafael-data.ranking_apartamentos_flask.ranking_apartamentos_desconsiderados`
    """
    
    dados_ranqueados = client.query(query_ranqueados).result()
    dados_desconsiderados = client.query(query_desconsiderados).result()
    
    dados_ranqueados = [dict(row) for row in dados_ranqueados]
    dados_desconsiderados = [dict(row) for row in dados_desconsiderados]
    
    return dados_ranqueados, dados_desconsiderados

# Função para favoritar ou desfavoritar um apartamento
def handle_toggle_favorite(fonte):
    if not fonte:
        return jsonify({'status': 'error', 'message': 'Nenhum link foi fornecido.'}), 400

    try:
        query_check = f"SELECT COUNT(*) as total FROM `rafael-data.ranking_apartamentos_flask.favoritos` WHERE Fonte = '{fonte}'"
        results = client.query(query_check).result()
        total_favorites = [row['total'] for row in results][0]

        if total_favorites > 0:
            query_remove = f"DELETE FROM `rafael-data.ranking_apartamentos_flask.favoritos` WHERE Fonte = '{fonte}'"
            client.query(query_remove)
            return jsonify({'status': 'success', 'message': 'Apartamento desfavoritado com sucesso.'}), 200
        else:
            query_add = f"INSERT INTO `rafael-data.ranking_apartamentos_flask.favoritos` (Fonte) VALUES ('{fonte}')"
            client.query(query_add)
            return jsonify({'status': 'success', 'message': 'Apartamento favoritado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Função para salvar ou editar comentários
def save_comment(fonte, comentario):
    if not fonte:
        return jsonify({'status': 'error', 'message': 'Fonte ausente'}), 400

    try:
        # Verifica se já existe um comentário para o apartamento
        query_check = """
            SELECT * FROM `rafael-data.ranking_apartamentos_flask.comentarios`
            WHERE Fonte = @fonte
        """
        query_params_check = [
            bigquery.ScalarQueryParameter("fonte", "STRING", fonte)  # Fonte = link do apartamento
        ]
        job_config_check = bigquery.QueryJobConfig(query_parameters=query_params_check)
        results = client.query(query_check, job_config=job_config_check).result()

        if list(results):
            # Atualiza o comentário se já existir
            query_update = """
                UPDATE `rafael-data.ranking_apartamentos_flask.comentarios`
                SET Comentarios = @comentario
                WHERE Fonte = @fonte
            """
            query_params_update = [
                bigquery.ScalarQueryParameter("comentario", "STRING", comentario),
                bigquery.ScalarQueryParameter("fonte", "STRING", fonte)
            ]
            job_config_update = bigquery.QueryJobConfig(query_parameters=query_params_update)
            client.query(query_update, job_config=job_config_update)
        else:
            # Adiciona o comentário se não existir
            query_add = """
                INSERT INTO `rafael-data.ranking_apartamentos_flask.comentarios` (Fonte, Comentarios)
                VALUES (@fonte, @comentario)
            """
            query_params_add = [
                bigquery.ScalarQueryParameter("fonte", "STRING", fonte),
                bigquery.ScalarQueryParameter("comentario", "STRING", comentario)
            ]
            job_config_add = bigquery.QueryJobConfig(query_parameters=query_params_add)
            client.query(query_add, job_config=job_config_add)

        return jsonify({'status': 'success', 'message': 'Comentário salvo com sucesso'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Função para deletar um comentário
def delete_comment(fonte):
    if not fonte:
        return jsonify({'status': 'error', 'message': 'Fonte ausente'}), 400

    try:
        # Deleta o comentário associado ao link (Fonte)
        query_delete = """
            DELETE FROM `rafael-data.ranking_apartamentos_flask.comentarios`
            WHERE Fonte = @fonte
        """
        query_params_delete = [
            bigquery.ScalarQueryParameter("fonte", "STRING", fonte)
        ]
        job_config_delete = bigquery.QueryJobConfig(query_parameters=query_params_delete)
        client.query(query_delete, job_config=job_config_delete)

        return jsonify({'status': 'success', 'message': 'Comentário removido com sucesso'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Função para obter os favoritos
def get_favorites():
    try:
        query = "SELECT Fonte FROM `rafael-data.ranking_apartamentos_flask.favoritos`"
        results = client.query(query).result()

        favorites = [row['Fonte'] for row in results]
        return jsonify(favorites), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Função para buscar anotações de um apartamento
def get_notes(fonte):
    try:
        # Busca o comentário na tabela de comentários pelo link (Fonte)
        query = """
            SELECT Comentarios FROM `rafael-data.ranking_apartamentos_flask.comentarios`
            WHERE Fonte = @fonte
        """
        query_params = [
            bigquery.ScalarQueryParameter("fonte", "STRING", fonte)
        ]
        job_config = bigquery.QueryJobConfig(query_parameters=query_params)

        result = client.query(query, job_config=job_config).result()

        # Verifica se existe algum resultado
        comentario = None
        for row in result:
            comentario = row['Comentarios']

        # Se o comentário for encontrado, retorna o comentário como string no JSON
        if comentario:
            return jsonify({'comentario': comentario}), 200
        else:
            return jsonify({'comentario': ''}), 200

    except Exception as e:
        # Se ocorrer algum erro, retorna a mensagem de erro
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

def atualizar_ranking_apartamentos(fonte_list):
    try:
        # Log para acompanhar a lista de fontes a serem removidas
        print(f"Recriando a tabela 'ranking_apartamentos', excluindo os itens com as fontes: {fonte_list}")
        
        # Query para recriar a tabela 'ranking_apartamentos' excluindo os apartamentos com fontes na 'fonte_list'
        query_recreate = """
            CREATE OR REPLACE TABLE `rafael-data.ranking_apartamentos_flask.ranking_apartamentos` AS
            SELECT 
                Codigo,
                Nome_Endereco,
                Bairro,
                Valor_Total_Mensal,
                Fonte,
                Pontuacao_Total,
                ROW_NUMBER() OVER (ORDER BY Pontuacao_Total DESC) AS rank
            FROM `rafael-data.ranking_apartamentos_flask.ranking_apartamentos`
            WHERE Fonte NOT IN UNNEST(@fonte_list)
            ORDER BY Pontuacao_Total DESC
        """
        
        # Passando a lista de fontes como parâmetro para excluir
        query_params = [
            bigquery.ArrayQueryParameter("fonte_list", "STRING", fonte_list)
        ]
        
        job_config = bigquery.QueryJobConfig(query_parameters=query_params)
        
        # Executar a query para recriar a tabela
        client.query(query_recreate, job_config=job_config).result()
        
        print(f"Tabela 'ranking_apartamentos' recriada com sucesso, excluindo os itens especificados.")
        return True

    except Exception as e:
        print(f"Erro ao recriar a tabela 'ranking_apartamentos': {str(e)}")
        return False
    

def desconsiderar_apartamento(fonte_list):
    try:
        # Verificar se os apartamentos já estão na tabela 'ranking_apartamentos_desconsiderados'
        query_check = """
            SELECT Fonte FROM `rafael-data.ranking_apartamentos_flask.ranking_apartamentos_desconsiderados`
            WHERE Fonte IN UNNEST(@fonte_list)
        """
        
        query_params_check = [
            bigquery.ArrayQueryParameter("fonte_list", "STRING", fonte_list)
        ]
        
        job_config_check = bigquery.QueryJobConfig(query_parameters=query_params_check)
        existing_desconsiderados = client.query(query_check, job_config=job_config_check).to_dataframe()
        
        # Filtrar os apartamentos que ainda não estão na tabela 'ranking_apartamentos_desconsiderados'
        fontes_novas = [fonte for fonte in fonte_list if fonte not in existing_desconsiderados['Fonte'].tolist()]
        
        if fontes_novas:
            # Inserir apartamentos que não estão na tabela 'ranking_apartamentos_desconsiderados'
            query_insert = """
                INSERT INTO `rafael-data.ranking_apartamentos_flask.ranking_apartamentos_desconsiderados`
                (Codigo, Nome_Endereco, Bairro, Valor_Total_Mensal, Fonte, Pontuacao_Total, rank)
                SELECT Codigo, Nome_Endereco, Bairro, Valor_Total_Mensal, Fonte, Pontuacao_Total, rank
                FROM `rafael-data.ranking_apartamentos_flask.lista_de_imoveis_pontuados`
                WHERE Fonte IN UNNEST(@fonte_list)
            """
            query_params_insert = [
                bigquery.ArrayQueryParameter("fonte_list", "STRING", fontes_novas)
            ]
            job_config_insert = bigquery.QueryJobConfig(query_parameters=query_params_insert)
            client.query(query_insert, job_config=job_config_insert).result()

            print(f"Apartamentos desconsiderados inseridos com sucesso.")
            return True
        else:
            print(f"Nenhum novo apartamento para desconsiderar.")
            return False

    except Exception as e:
        print(f"Erro ao desconsiderar apartamentos: {str(e)}")
        return False
