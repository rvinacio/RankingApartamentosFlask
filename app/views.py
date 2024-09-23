from flask import render_template, request, jsonify
from app import app
from app.utils import (
    get_ranking_data, handle_toggle_favorite, save_comment, 
    get_favorites, get_comments, get_notes, delete_comment, 
    remover_apartamentos_do_ranking_e_atualizar
)

# Rota para exibir o ranking
@app.route('/')
def mostrar_ranking():
    dados_ranqueados, dados_desconsiderados = get_ranking_data()
    return render_template('ranking.html', dados_ranqueados=dados_ranqueados, dados_desconsiderados=dados_desconsiderados)

# Rota para exibir a página de desconsiderados
@app.route('/desconsiderados')
def mostrar_desconsiderados():
    _, dados_desconsiderados = get_ranking_data()  # Pega só os dados desconsiderados
    return render_template('desconsiderados.html', dados_ranqueados=dados_desconsiderados)

# Rota para favoritar ou desfavoritar
@app.route('/toggle_favorite', methods=['POST'])
def toggle_favorite():
    data = request.get_json()
    fonte = data.get('link')
    return handle_toggle_favorite(fonte)

# Rota para salvar ou editar comentários
@app.route('/save_notes', methods=['POST'])
def save_notes():
    data = request.get_json()
    fonte = data.get('fonte')  # Use 'fonte' que contém o link do apartamento
    comentario = data.get('comentario')

    if comentario.strip() == "":  # Se o comentário for vazio, deletar o registro
        return delete_comment(fonte)
    
    return save_comment(fonte, comentario)

# Rota para buscar anotações existentes
@app.route('/get_notes', methods=['GET'])
def get_notes_route():
    fonte = request.args.get('fonte')  # Pega o link do apartamento como string
    if not fonte:
        return jsonify({'status': 'error', 'message': 'Fonte não fornecida'}), 400
    
    return get_notes(fonte)

# Rota para obter os favoritos
@app.route('/get_favorites', methods=['GET'])
def get_favorites_route():
    return get_favorites()

# Rota para obter os comentários
@app.route('/get_comments', methods=['GET'])
def get_comments_route():
    return get_comments()

# Rota para remover o apartamento e recalcular o ranking
@app.route('/remover_imovel', methods=['POST'])
def remover_imovel():
    data = request.get_json()
    print("Dados recebidos do JS:", data)  # Imprime todos os dados recebidos
    fonte_list = data.get('codigo')  # fonte_list agora contém uma lista de códigos
    if not fonte_list:
        return jsonify({'status': 'error', 'message': 'Lista de fontes não fornecida'}), 400
    
     # Imprime a lista de fontes recebida
    print("Lista de fontes recebida:", fonte_list)
    
    return remover_apartamentos_do_ranking_e_atualizar(fonte_list)