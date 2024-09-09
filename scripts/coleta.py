import csv
import requests
from bs4 import BeautifulSoup

# Carregar arquivo CSV
csv_file = '/mnt/data/apartamentos.csv'

# Links para pesquisa
links = [
    "https://www.quintoandar.com.br/imovel/894601086/alugar/apartamento-2-quartos-santa-ifigenia-sao-paulo",
    "https://www.quintoandar.com.br/imovel/894590276/alugar/apartamento-3-quartos-bela-vista-sao-paulo",
    "https://www.quintoandar.com.br/imovel/892877492/alugar/apartamento-3-quartos-bela-vista-sao-paulo"
]

# Função para coletar dados de um link
def coletar_dados(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Coletar informações do imóvel (ajustar com base na estrutura do site)
    nome_endereco = soup.find("h1", {"class": "address-title"}).get_text(strip=True)
    bairro = soup.find("span", {"class": "neighborhood"}).get_text(strip=True)
    preco_aluguel = soup.find("span", {"class": "rental-price"}).get_text(strip=True)
    condominio = soup.find("span", {"class": "condominium-fee"}).get_text(strip=True)
    iptu = soup.find("span", {"class": "iptu-price"}).get_text(strip=True)
    quartos = soup.find("span", {"class": "bedroom-count"}).get_text(strip=True)
    banheiros = soup.find("span", {"class": "bathroom-count"}).get_text(strip=True)
    vagas = soup.find("span", {"class": "parking-space-count"}).get_text(strip=True)
    area = soup.find("span", {"class": "area-size"}).get_text(strip=True)
    facilidades = ", ".join([f.get_text(strip=True) for f in soup.find_all("span", {"class": "facility-name"})])
    nome_imobiliaria = "QuintoAndar"  # Ajustar para coletar nome da imobiliária caso necessário
    site = link
    
    # Calcular o valor total mensal
    valor_total_mensal = float(preco_aluguel.replace("R$", "").replace(",", "")) + \
                         float(condominio.replace("R$", "").replace(",", "")) + \
                         float(iptu.replace("R$", "").replace(",", ""))
    
    # Retornar os dados coletados
    return {
        "nome_endereco": nome_endereco,
        "bairro": bairro,
        "preco_aluguel": preco_aluguel,
        "condominio": condominio,
        "iptu": iptu,
        "quartos": quartos,
        "banheiros": banheiros,
        "vagas": vagas,
        "area": area,
        "facilidades": facilidades,
        "nome_imobiliaria": nome_imobiliaria,
        "site": site,
        "valor_total_mensal": valor_total_mensal
    }

# Função para inserir dados no CSV
def inserir_no_csv(dados):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Inserir linha no CSV
        writer.writerow([
            dados['nome_endereco'],
            dados['bairro'],
            dados['preco_aluguel'],
            dados['condominio'],
            dados['iptu'],
            dados['quartos'],
            dados['banheiros'],
            dados['vagas'],
            dados['area'],
            dados['facilidades'],
            dados['nome_imobiliaria'],
            dados['site'],
            dados['valor_total_mensal']
        ])

# Coletar e exibir os dados para todos os links
for link in links:
    dados_imovel = coletar_dados(link)
    print(f"Dados coletados do link: {link}")
    for chave, valor in dados_imovel.items():
        print(f"{chave}: {valor}")
    
    # Solicitar confirmação para inserir no CSV
    confirmacao = input("Deseja inserir os dados deste imóvel no CSV? (sim/não): ").strip().lower()
    if confirmacao == "sim":
        inserir_no_csv(dados_imovel)
        print(f"Dados do imóvel inseridos no CSV com sucesso.")
    else:
        print(f"Dados do imóvel não foram inseridos no CSV.")