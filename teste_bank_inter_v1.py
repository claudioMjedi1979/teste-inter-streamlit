import streamlit as st
import requests
import pandas as pd
import streamlit as st

# Função para carregar dados da API
def load_api_data():
    url = "https://spot-bid-advisor.s3.amazonaws.com/spot-advisor-data.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao carregar dados da API.")
        return {}

# Função para verificar suporte ao sistema operacional (baseado em "emr")
def get_os_support(emr_value):
    if emr_value:
        return {"Linux": "Yes", "Windows": "No"}  # EMR geralmente roda em Linux
    else:
        return {"Linux": "No", "Windows": "Yes"}  # Presumimos suporte ao Windows se não for Linux

# Carregar os dados da API
json_data = load_api_data()

# Verificar se os dados foram carregados corretamente
if json_data:
    instance_types = json_data.get('instance_types', {})
    ranges = json_data.get('ranges', [])
    global_rate = json_data.get('global_rate', 'N/A')
    # Carregar a imagem SVG do mesmo diretório onde está o script
    st.image("banco-inter-logo.svg", use_column_width=False, width=200)
    st.title("Demonstração de Instâncias AWS - Teste Técnico")

    # Seletor de região
    region = st.selectbox("Selecione a região", options=["us-east-1", "us-west-1", "eu-west-1"])

    # Filtros de CPU, Memória e Tipo de Instância
    vCPU = st.slider("Insira o valor de vCPU", min_value=1, max_value=96, value=2)
    memory = st.slider("Insira o valor de Memória (GiB)", min_value=0.5, max_value=768.0, step=0.5, value=4.0)
    instance_type_input = st.text_input("Digite o tipo de instância (mínimo 3 caracteres)")

    if len(instance_type_input) < 3:
        st.warning("Por favor, insira ao menos 3 caracteres para o tipo de instância.")

    # Criar DataFrame a partir dos dados
    df = pd.DataFrame([
        {
            'Instance Type': instance,
            'vCPU': details['cores'],
            'Memory GiB': details['ram_gb'],
            'Savings over On-Demand': details.get('savings_over_on_demand', 'N/A'),
            'Frequency of Interruption': details.get('frequency', global_rate),
            'Update Date': details.get('update_date', 'N/A'),
            'Linux': 'Yes' if details.get('emr', False) else 'No',  # Suporte para Linux
            'Windows': 'No' if details.get('emr', False) else 'Yes'  # Suporte para Windows
        }
        for instance, details in instance_types.items()
    ])

    # Filtrar DataFrame com os critérios de CPU, Memória e tipo de instância
    df_filtered = df[
        (df['vCPU'] >= vCPU) &
        (df['Memory GiB'] >= memory) &
        (df['Instance Type'].str.contains(instance_type_input, case=False, na=False))
    ]

    # Ordenar DataFrame
    df_filtered = df_filtered.sort_values(by='Savings over On-Demand', ascending=False)

    # Exibir a lista filtrada com as colunas Linux e Windows
    st.subheader("Instâncias Filtradas (Ordenadas por Savings)")
    st.dataframe(df_filtered)

    # Drill-down: Selecionar uma instância para ver detalhes
    if not df_filtered.empty:
        instance_selected = st.selectbox("Selecione uma instância para ver detalhes", df_filtered['Instance Type'])
        instance_details = instance_types.get(instance_selected, {})

        st.subheader(f"Detalhes da Instância: {instance_selected}")
        st.write(f"vCPU: {instance_details.get('cores', 'N/A')}")
        st.write(f"Memória: {instance_details.get('ram_gb', 'N/A')} GiB")
        st.write(f"Savings over On-Demand: {instance_details.get('savings_over_on_demand', 'N/A')}")
        st.write(f"Frequência de Interrupção: {instance_details.get('frequency', global_rate)}")
        st.write(f"Update Date: {instance_details.get('update_date', 'N/A')}")
        st.write(f"Suporte ao Linux: {'Yes' if instance_details.get('emr', False) else 'No'}")
        st.write(f"Suporte ao Windows: {'No' if instance_details.get('emr', False) else 'Yes'}")

else:
    st.error("Não foi possível carregar os dados da API.")
