# Ranking Apartamentos Flask

## Sobre o Projeto
O projeto "Ranking Apartamentos Flask" surgiu da necessidade pessoal de facilitar o processo de escolha e visita de apartamentos para aluguel. Desenvolvido em Python, ele utiliza a inteligência do ChatGPT para extrair informações de anúncios de apartamentos, organizando-os em uma planilha. Um script Python posteriormente analisa esses dados com base em critérios pré-definidos e pesos atribuídos para cada um, gerando um ranking dos apartamentos mais atraentes para visitação.

## Estrutura do Projeto

Abaixo está a estrutura de diretórios do projeto "RankingApartamentosFlask":
```
/meu_projeto
/
|-- static/
|   |-- css/
|   |   |-- style.css
|   |-- js/
|   |   |-- ranking.js
|
|-- templates/
|   |-- index.html
|   |-- ranking.html
|   |-- layout.html
|
|-- scripts/
|   |-- data_processing.py
|   |-- db_integration.py
|
|-- app/
|   |-- __init__.py
|   |-- views.py
|   |-- utils.py
|
|-- README.md
|-- requirements.txt
|-- run.py
```

### Funcionalidades

1. **Ranking Automático**: O sistema ranqueia automaticamente os apartamentos de acordo com os critérios estabelecidos, exibindo-os em uma tabela dinâmica.

2. **Anotações e Favoritos**: Usuários podem marcar apartamentos como favoritos e adicionar anotações, permitindo a comparação de diferentes imóveis de maneira personalizada.

3. **Remoção de Apartamentos**: Agora, há um botão de **"Remover"** que permite desconsiderar apartamentos indesejados. Os apartamentos removidos são armazenados em uma tabela separada, permitindo sua reintegração no ranking futuramente.

4. **Reconsideração de Apartamentos**: Os usuários também podem reconsiderar apartamentos previamente desconsiderados, trazendo-os de volta ao ranking com suas pontuações originais.

5. **Botão de Menu**: Um novo botão de menu foi adicionado para facilitar o acesso à página de apartamentos desconsiderados e outras opções futuras.

6. **Integração com Banco de Dados (BigQuery)**: Anteriormente, o projeto utilizava arquivos CSV para armazenar e processar os dados dos apartamentos. Agora, toda a estrutura foi migrada para um banco de dados no **BigQuery**, garantindo maior escalabilidade e desempenho.

## Tecnologias Utilizadas
- **Python**: Para lógica de backend e processamento de dados.
- **Flask**: Para criação da interface web.
- **HTML/CSS/JavaScript**: Para design e interatividade da página web.
- **Jupyter Notebook**: Utilizado para desenvolvimento e testes de protótipos do código.

## Gamificação e Sistema de Pontuação

O projeto implementa um sistema de pontuação avançado para classificar apartamentos com base em vários critérios essenciais na tomada de decisões de aluguel. Utilizando técnicas de gamificação, cada apartamento recebe pontos por critérios como preço, quantidade de quartos, banheiros e proximidade com o local de trabalho.

O cálculo de distância é realizado através da geolocalização, convertendo endereços em coordenadas de latitude e longitude usando a biblioteca `geopy`, e em seguida, calculando a distância real. Essa abordagem permite uma avaliação precisa e dinâmica dos imóveis, facilitando a decisão de qual apartamento visitar primeiro.

## Processamento de Dados

O tratamento de dados foi alterado para integrar diretamente com o BigQuery. Toda a manipulação de dados (inclusão, remoção e reclassificação dos apartamentos) é feita diretamente no banco de dados, substituindo o uso de arquivos CSV.

### Estrutura de Dados

O projeto utiliza várias tabelas no banco de dados BigQuery:

- **ranking_apartamentos**: Tabela principal que armazena todos os apartamentos ativos no ranking.
- **ranking_apartamentos_desconsiderados**: Tabela que armazena temporariamente os apartamentos removidos do ranking.
- **lista_de_imoveis_pontuados**: Tabela que contém os apartamentos pontuados, mostrando a classificação detalhada com base em vários critérios (preço, distância, número de quartos, banheiros, etc.).
- **favoritos**: Tabela que armazena os apartamentos marcados como favoritos pelos usuários.
- **comentarios**: Tabela que armazena as anotações feitas pelos usuários sobre cada apartamento.


### Como Usar
Para executar o projeto "Ranking Apartamentos Flask" localmente, siga os passos abaixo:

1. **Clone o Repositório**:
   Abra o terminal e digite o seguinte comando para clonar o repositório para sua máquina local:
   ```bash
   git clone https://github.com/rvinacio/RankingApartamentosFlask.git
   cd RankingApartamentosFlask
   ```

2. **Instale as Dependências**:
   Certifique-se de que você está no diretório do projeto e execute o seguinte comando para instalar as dependências listadas no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o Script**:
   Execute o script `run.py` para iniciar a aplicação. Esse script configura e inicia o servidor Flask:
   ```bash
   python run.py
   ```

   Isso iniciará o servidor Flask e normalmente o servidor ficará acessível via navegador em `http://localhost:5000` ou outro endereço dependendo das configurações do Flask.

### Comandos Extras
- Certifique-se de ter o Python instalado em sua máquina.
- Se estiver usando um ambiente virtual, ative-o antes de instalar as dependências e executar o script.

## Melhorias Futuras

O projeto tem grande potencial para evolução, com áreas de melhorias identificadas:

- **Automatização do Processo de Extração de Dados**: Atualmente, a extração de dados é semi-automática e dependente da interação com o ChatGPT. A implementação de um sistema de web scraping diretamente em Python poderia automatizar completamente esse processo, tornando-o mais eficiente e menos propenso a erros.
- **Página de Apartamentos Desconsiderados**: Um dos próximos passos do projeto é desenvolver uma página dedicada aos apartamentos desconsiderados, permitindo aos usuários gerenciar melhor quais imóveis querem reconsiderar.
- **Implementação de Sistema de Notificações**: A adição de um sistema de notificações que avise os usuários sobre mudanças no status dos apartamentos (como variações de preço ou novas disponibilidades) seria um diferencial para a plataforma, melhorando a experiência do usuário.
- **Melhoria na Interface Responsiva**: Pretende-se aprimorar ainda mais a interface do usuário para garantir que a aplicação seja totalmente funcional e responsiva em dispositivos móveis, proporcionando uma navegação mais fluida e intuitiva em diferentes resoluções.
- **Integração com APIs Imobiliárias**: Futuramente, a integração com APIs de grandes plataformas de imóveis permitirá a sincronização em tempo real de informações, otimizando a atualização de dados de apartamentos no sistema.
- **Melhorias no Sistema de Autenticação**: A aplicação deverá incluir uma autenticação segura para que os usuários possam salvar e acessar suas preferências, incluindo os apartamentos favoritados e desconsiderados, em diferentes dispositivos.
- **Uso do BigQuery como Data Warehouse**: O banco de dados utilizado atualmente é o **BigQuery**, que, apesar de ser um **Data Warehouse**, foi escolhido pela facilidade e rapidez na curva de aprendizado. Embora o BigQuery não seja o ideal para operações que envolvem atualizações frequentes de linhas, como exigido pelo App Engine, ele resolveu o problema inicial devido ao seu conhecimento prévio. Para melhorias futuras, um banco de dados específico para o **App Engine**, mais otimizado para atualizações frequentes e operações de leitura/escrita, poderá ser implementado, melhorando a performance da aplicação.
- **Pipeline de Dados com Python**: O pipeline de dados atual é feito utilizando **Python** e executado via **Jupyter Notebooks**. Embora ele atenda às necessidades iniciais do projeto, há espaço para melhorias em termos de performance e estruturação. Um pipeline mais robusto poderia ser desenvolvido, aumentando a eficiência e escalabilidade do processo de tratamento de dados.
- **Modelagem de Dados**: Como parte das melhorias planejadas, será desenvolvida uma modelagem de dados formal, incluindo o modelo físico ou conceitual das tabelas, para que seja possível recriar as tabelas de forma idêntica ao que foi feito no projeto. Atualmente, como solução provisória, as informações sobre o formato das tabelas podem ser encontradas no arquivo **nova_pontuacao.ipynb** (localizado na pasta **scripts** no GitHub), que trata os dados e realiza a conexão com o banco de dados para carregar as tabelas. Esse notebook contém os `INSERTs`, `DELETEs` e o esquema das tabelas. Embora este não seja o método mais apropriado para documentar a estrutura dos dados, ele fornece uma visão das colunas e do esquema utilizado até que a modelagem completa seja disponibilizada.

## Contato
Rafael Inacio - rvinacio@gmail.com
Projeto Link: [GitHub Repository](https://github.com/rvinacio/RankingApartamentosFlask)

