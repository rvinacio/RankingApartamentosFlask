# Ranking Apartamentos Flask

## Sobre o Projeto
O "Ranking Apartamentos Flask" é um projeto desenvolvido com o intuito de compartilhar conhecimentos práticos sobre desenvolvimento web com Flask e Python, e o uso de plataformas de nuvem como o Google Cloud Platform, especificamente App Engine e BigQuery. Este projeto não só demonstra a aplicação de Python e Flask na criação de páginas web, mas também oferece insights sobre como estruturar e hospedar aplicações na nuvem, manipular dados com BigQuery, e mais.

Esse projeto surgiu da necessidade pessoal de facilitar o processo de escolha e visita de apartamentos para aluguel. Desenvolvido em Python, ele utiliza a inteligência do ChatGPT para extrair informações de anúncios de apartamentos, organizando-os em uma planilha. Um script Python posteriormente analisa esses dados com base em critérios pré-definidos e pesos atribuídos para cada um, gerando um ranking dos apartamentos mais atraentes para visitação.

## Objetivos de Aprendizado
O projeto foi criado para servir como um recurso educativo abrangendo vários aspectos de desenvolvimento e operações de TI, incluindo:

1. **Desenvolvimento Web com Flask**: Demonstração prática de como configurar e executar uma aplicação web usando o microframework Flask.
2. **Hospedagem com Google App Engine**: Instruções detalhadas sobre como configurar e desdobrar uma aplicação em Flask no ambiente de nuvem do App Engine (em breve).
3. **Integração com BigQuery**: Uso do BigQuery como back-end para armazenamento e consulta de dados, demonstrando como integrar tecnologias de nuvem com aplicações web (em breve).
4. **Scripts Python para Processamento de Dados**: Exploração do uso de scripts Python para manipulação e análise de dados, crucial para operações de back-end.
5. **Segurança com IAM do Google Cloud**: Explicação sobre o Identity and Access Management (IAM), demonstrando como configurar e gerenciar acessos no Google Cloud (em breve).
6. **Operações de Terminal**: Utilização do terminal para operações de versionamento com Git, deploy com gcloud, e teste local de aplicações.

## Estrutura do Projeto

Abaixo está a estrutura de diretórios do projeto "Ranking Apartamentos Flask":
```
RankingApartamentosFlask/
│
├── app/
│   ├── __init__.py          # Inicialização do app Flask
│   ├── views.py             # Arquivo com as rotas do app
│   ├── utils.py             # Funções auxiliares (e.g. manipulação de dados)
│   ├── static/              # Arquivos estáticos como CSS e JS
│   │   ├── style.css        # Arquivo de estilos CSS
│   │   ├── ranking.js       # Arquivo JavaScript
│   │   └── jquery.min.js    # Biblioteca jQuery local
│   ├── templates/           # Templates HTML do app
│   │   ├── layout.html      # Layout base para as páginas
│   │   ├── ranking.html     # Página principal de ranking
│   │   └── desconsiderados.html # Página de imóveis desconsiderados
│
├── scripts/                 # Scripts auxiliares para manipulação de dados e rodar jobs
│   └── nova_pontuacao.py    # Script para calcular pontuações de imóveis
│
├── requirements.txt         # Dependências do projeto (Flask, BigQuery, etc.)
├── app.yaml                 # Configuração do App Engine (Google Cloud)
├── .gcloudignore            # Arquivo para ignorar no deploy do GCP
├── .gitignore               # Arquivo para ignorar no Git
├── run.py                   # Arquivo principal para rodar o servidor Flask
├── README.md                # Documentação do projeto

```

### Funcionalidades

1. **Ranking Automático**: O sistema ranqueia automaticamente os apartamentos de acordo com os critérios estabelecidos, exibindo-os em uma tabela dinâmica.

2. **Anotações e Favoritos**: Usuários podem marcar apartamentos como favoritos e adicionar anotações, permitindo a comparação de diferentes imóveis de maneira personalizada.

3. **Remoção de Apartamentos**: Agora, há um botão de **"Remover"** que permite desconsiderar apartamentos indesejados. Os apartamentos removidos são armazenados em uma tabela separada, permitindo sua reintegração no ranking futuramente.

4. **Reconsideração de Apartamentos**: Os usuários também podem reconsiderar apartamentos previamente desconsiderados, trazendo-os de volta ao ranking com suas pontuações originais.

5. **Botão de Menu**: Um novo botão de menu foi adicionado para facilitar o acesso à página de apartamentos desconsiderados e outras opções futuras.

6. **Integração com Banco de Dados (BigQuery)**: Anteriormente, o projeto utilizava arquivos CSV para armazenar e processar os dados dos apartamentos. Agora, toda a estrutura foi migrada para um banco de dados no **BigQuery**, garantindo maior escalabilidade e desempenho.

## Tecnologias Utilizadas
- **Python, Flask**: Para toda a lógica de back-end e interação com o banco de dados.
- **HTML, CSS, JavaScript**: Para construção da interface do usuário.
- **Google App Engine, BigQuery**: Para hospedagem e gerenciamento de dados.
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

### Acesso aos Dados
Atualmente, o projeto requer acesso ao BigQuery para operar completamente, pois depende de dados armazenados nesse serviço. No futuro próximo, planejamos implementar melhorias que simplificarão este processo. Estamos explorando alternativas como o uso do Datastore do Google App Engine, que permitirão executar o projeto sem necessidade de configurações complexas de acesso ao BigQuery. Isso tornará mais fácil para qualquer pessoa executar o projeto localmente sem preocupações adicionais de configuração de acesso a dados.

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

### Conclusão
Este projeto é um esforço prático para fornecer uma base sólida de conhecimento que pode ser expandida e adaptada. Ele serve como um excelente ponto de partida para quem deseja aprofundar-se em desenvolvimento web, manipulação de dados, e mais. Em breve, planejo acrescentar aqui detalhes da configuração da hospedagem no App Engine, Google Cloud Storage e IAM. 


## Contato
Rafael Inacio - rvinacio@gmail.com
Projeto Link: [GitHub Repository](https://github.com/rvinacio/RankingApartamentosFlask)

