Documento Técnico para a Aplicação em Streamlit para o Testes Técnico de Plataformas de Produto

1. Este documento técnico descreve o funcionamento de uma aplicação Streamlit 
que consulta instâncias AWS de uma API e exibe dados filtrados sobre as instâncias, como vCPU, Memória, sistema operacional suportado (Linux ou Windows), 
e outras informações úteis. 
O usuário pode interagir com a aplicação 
localmente, utilizando filtros de entrada para buscar instâncias específicas e visualizar detalhes de cada uma.

2. A aplicação requer a instalação das seguintes bibliotecas para funcionar corretamente:

* Streamlit: Para criar a interface da web interativa.
* Requests: Para fazer requisições HTTP e obter dados da API.
* Pandas: Para manipulação e filtragem dos dados.

Instalação das dependências:
pip install streamlit requests pandas

3. Carregamento de Dados da API
    
A função load_api_data() faz uma requisição HTTP para obter os dados de instâncias AWS de uma API pública e 
retorna os dados em formato JSON. Se houver um erro durante a requisição, uma mensagem de erro é exibida ao usuário:
<img width="578" alt="image" src="https://github.com/user-attachments/assets/a93a3daa-0760-4343-88d3-f81b1243b63d">

4. O usuário pode filtrar as instâncias de acordo com:
<img width="831" alt="image" src="https://github.com/user-attachments/assets/eda2fe45-bbee-4946-958b-09b70689aea1">



Região: Seleção de diferentes regiões AWS.
vCPU: Quantidade de vCPUs desejadas (entre 1 e 96).
Memória (GiB): Memória RAM em GiB (0.5 até 768 GiB).
Tipo de Instância: Entrada de texto para buscar tipos específicos de instâncias (mínimo 3 caracteres).

5.Tabela Filtrada
Após aplicar os filtros, uma tabela é exibida mostrando as instâncias que atendem aos critérios fornecidos. A tabela contém colunas para:

Tipo de Instância
vCPU
Memória
Economia sobre On-Demand
Suporte a Linux
Suporte a Windows

6. Passo Execute a Aplicação
No terminal, navegue até o diretório onde o script está salvo e execute o seguinte comando para iniciar a aplicação:
pip install streamlit requests pandas
streamlit run teste_bank_inter_v1.py

Após iniciar a aplicação, o Streamlit irá fornecer um link local, como:
Local URL: http://localhost:8501

. Funcionamento
Após a execução, a aplicação permite:

Filtrar instâncias AWS por região, vCPU, memória e tipo de instância.
Visualizar uma tabela com os detalhes das instâncias filtradas.
Selecionar uma instância específica para obter mais informações detalhadas.
Exibir uma imagem SVG no topo da página.
7. Possíveis Erros
Erro ao carregar a imagem: Verifique se o arquivo banco-inter-logo.svg está no mesmo diretório que o script.
Erro ao carregar dados da API: Se a API estiver fora do ar ou se houver problemas com a conexão, o erro será exibido.
8. Melhorias Futura
Adicionar novos filtros, como preço e desempenho das instâncias.
Adicionar cache de dados para otimizar a performance.

Fluxo da aplicação 

<img width="1392" alt="image" src="https://github.com/user-attachments/assets/4a93e77f-7f25-44a9-9fa2-bca9d2b7ca7c">


