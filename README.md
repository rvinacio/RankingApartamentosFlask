# Ranking Underline Alugar Casa

## Sobre o Projeto
O projeto "Ranking Apartamentos Flas" surgiu da necessidade pessoal de facilitar o processo de escolha e visita de apartamentos para aluguel. Desenvolvido em Python, ele utiliza a inteligência do ChatGPT para extrair informações de anúncios de apartamentos, organizando-os em uma planilha. Um script Python posteriormente analisa esses dados com base em critérios pré-definidos e pesos atribuídos para cada um, gerando um ranking dos apartamentos mais atraentes para visitação.

## Estrutura do Projeto

Abaixo está a estrutura de diretórios do projeto "RankingApartamentosFlask":

/meu_projeto
│
├── /app
│   ├── /static
│   │   ├── /css
│   │   ├── /js
│   │   └── /img
│   │
│   ├── /templates
│   │   └── index.html
│   │
│   ├── init.py
│   ├── views.py
│   ├── models.py
│   └── forms.py
│
├── /data
│   └── output.csv
│
├── config.py
├── run.py
└── requirements.txt


## Funcionalidades
- **Extração Automatizada de Dados**: Utiliza ChatGPT para extrair dados de anúncios de imóveis online.
- **Avaliação por Critérios**: Aplica pesos a diferentes critérios como preço, número de quartos, banheiros e distância até o trabalho.
- **Geração de Ranking**: Cria um ranking dinâmico dos apartamentos para ajudar na decisão de qual visitar primeiro.
- **Interface Web**: Apresenta o ranking em uma página web desenvolvida com Flask, HTML, CSS e Javascript.

## Tecnologias Utilizadas
- **Python**: Para lógica de backend e processamento de dados.
- **Flask**: Para criação da interface web.
- **HTML/CSS/JavaScript**: Para design e interatividade da página web.
- **Jupyter Notebook**: Utilizado para desenvolvimento e testes de protótipos do código.

## Gamificação e Sistema de Pontuação

O projeto implementa um sistema de pontuação avançado para classificar apartamentos com base em vários critérios essenciais na tomada de decisões de aluguel. Utilizando técnicas de gamificação, cada apartamento recebe pontos por critérios como preço, quantidade de quartos, banheiros e proximidade com o local de trabalho.

O cálculo de distância é realizado através da geolocalização, convertendo endereços em coordenadas de latitude e longitude usando a biblioteca `geopy`, e em seguida, calculando a distância real. Essa abordagem permite uma avaliação precisa e dinâmica dos imóveis, facilitando a decisão de qual apartamento visitar primeiro.

## Como Usar
Para executar o projeto localmente, siga os passos abaixo:
1. Clone o repositório para sua máquina local.
2. Instale as dependências necessárias (listar as dependências ou incluir comando para instalar).
3. Execute o script para iniciar a extração de dados e geração do ranking.
4. Inicie o servidor Flask para visualizar o ranking na interface web.

## Melhorias Futuras

O projeto tem grande potencial para evolução, com várias áreas de melhorias identificadas:

- **Automatização do Processo de Extração de Dados**: Atualmente, a extração de dados é semi-automática e dependente da interação com o ChatGPT. A implementação de um sistema de web scraping diretamente em Python poderia automatizar completamente esse processo, tornando-o mais eficiente e menos propenso a erros.
- **Melhoria na Interface de Usuário**: A interface web, embora funcional, pode ser melhorada para oferecer uma experiência de usuário mais rica e interativa.
- **Otimização de Performance**: Com a adição de mais imóveis e critérios, o sistema poderia ser otimizado para garantir que a geração do ranking seja realizada de maneira rápida e eficiente.
- **Integração com Banco de Dados**: Atualmente, o projeto utiliza arquivos CSV para armazenamento de dados devido ao seu escopo limitado. No entanto, uma integração com um banco de dados como PostgreSQL ou MongoDB poderia ser considerada para melhorar a gestão de dados e suportar um volume maior de informações de forma mais eficaz.

## Contato
Seu Nome - seu_email@example.com
Projeto Link: [GitHub Repository](URL_do_repositório)