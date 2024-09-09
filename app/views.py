from flask import render_template, request, jsonify
from app import app
from app.utils import *


@app.route('/')
def mostrar_ranking():
    # Lê os dados do CSV
    dados_ranqueados, dados_desconsiderados = ler_csv()  # Desempacota ambos os DataFrames retornados
    
    # Formatar a coluna "Valor Total Mensal (R$)" como moeda BRL para ambos os conjuntos de dados
    dados_ranqueados['Valor Total Mensal (R$)'] = dados_ranqueados['Valor Total Mensal (R$)'].apply(
        lambda x: f'R${x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))
    dados_desconsiderados['Valor Total Mensal (R$)'] = dados_desconsiderados['Valor Total Mensal (R$)'].apply(
        lambda x: f'R${x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))

    # Renderiza o HTML com os dados
    return render_template('ranking.html', dados_ranqueados=dados_ranqueados, dados_desconsiderados=dados_desconsiderados)

@app.route('/remover_imovel', methods=['POST'])
def remover():
    codigos = request.json['codigo']
    remover_imovel(codigos)
    return jsonify({'success': True, 'message': 'Imóveis removidos com sucesso'})


@app.route('/reconsiderar_imovel', methods=['POST'])
def reconsiderar():
    codigo = request.json['codigo']
    reconsiderar_imovel(codigo)
    return jsonify({'success': True, 'message': 'Imóvel reconsiderado com sucesso'})