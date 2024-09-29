import streamlit as st
import pandas as pd
import requests

# Função para carregar os dados do arquivo instancias.txt
def load_instance_data(file_path):
    df = pd.read_csv(file_path, delimiter="\t")
    df.columns = df.columns.str.strip()  # Remove espaços nas colunas
    return df

# Função para buscar os dados da API (JSON com instâncias spot)
def fetch_spot_data():
    url = "https://spot-bid-advisor.s3.amazonaws.com/spot-advisor-data.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro ao acessar a API: {response.status_code}")
        return {}

# Função para formatar os dados em uma tabela com as colunas solicitadas
def format_data_for_display(data, instance_data):
    formatted_data = []
    for instance_type, value in data.items():
        # Buscando informações da instância no arquivo instancias.txt
        instance_info = instance_data[instance_data['Nome da instância'] == instance_type]
        if not instance_info.empty:
            row = instance_info.iloc[0]  # Pega a primeira linha correspondente
            formatted_data.append({
                "Instance Type": instance_type,
                "vCPU (cores)": row['vCPU'],
                "Memory GiB": row['Memória'],
                "Savings over On-Demand": value.get('SavingsOverOnDemand', 'N/A'),
                "Frequency of Interruption": value.get('InterruptionFrequency', 'N/A'),
                "Hourly Rate": row['Taxa horária sob demanda'],
                "Network Performance": row['Performance das redes']
            })
    return pd.DataFrame(formatted_data)

# Função para filtrar os dados com base na região, CPU, memória, etc.
def filter_spot_data(data, region, cpu, memory, instance_type, os_choice):
    filtered_data = {}
    for key, value in data.items():
        if region and value.get('region') != region:
            continue
        if cpu and value.get('vCPU', 0) < cpu:
            continue
        if memory and value.get('MemoryGiB', 0) < memory:
            continue
        if instance_type and key != instance_type:
            continue
        if os_choice and value.get('OS', 'Linux') != os_choice:
            continue
        filtered_data[key] = value
    return filtered_data

# Função para encontrar a instância mais barata
def find_cheapest_instance(data):
    cheapest_instance = None
    highest_savings = -1
    for key, value in data.items():
        savings = value.get('SavingsOverOnDemand', 0)
        if savings > highest_savings:
            highest_savings = savings
            cheapest_instance = (key, value)
    return cheapest_instance

# Função para encontrar a instância mais cara
def find_most_expensive_instance(instance_data):
    # Ordena as instâncias pela taxa horária (Taxa horária sob demanda)
    most_expensive_instance = instance_data.sort_values(by="Taxa horária sob demanda", ascending=False).iloc[0]
    return most_expensive_instance

# Carregar dados de instâncias do arquivo instancias.txt
instance_data = load_instance_data('instancias.txt')

# Configurar a interface
st.title("Filtrar Instâncias Spot")

# Fetch data from the API
data = fetch_spot_data()

# Verificar se a chave "instance_types" existe
if "instance_types" in data:
    # Dropdown de Regiões
    regions_list = [
        'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'us-gov-east-1', 'us-gov-west-1', 
        'ca-central-1', 'sa-east-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 
        'eu-south-1', 'eu-south-2', 'eu-central-1', 'ap-south-1', 'ap-south-2', 'ap-southeast-1', 
        'ap-southeast-2', 'ap-southeast-4', 'ap-northeast-1', 'ap-northeast-3', 'ap-northeast-2', 
        'ap-east-1', 'me-south-1', 'me-central-1', 'il-central-1', 'af-south-1'
    ]
    selected_region = st.selectbox("Selecione a Região", [""] + regions_list)
    
    # Input para CPU e Memória
    cpu_input = st.number_input("CPU", min_value=1, value=1)
    memory_input = st.number_input("Memória (GiB)", min_value=1, value=1)

    # Dropdown para Tipos de Instância
    instance_types = sorted(list(data["instance_types"].keys()))
    selected_instance_type = st.selectbox("Selecione o Tipo de Instância", [""] + instance_types)

    # Dropdown para Sistema Operacional
    os_choice = st.selectbox("Selecione o Sistema Operacional (OS)", ["", "Linux", "Windows"])

    # Botão para filtrar
    if st.button("Filtrar Instâncias"):
        filtered_data = filter_spot_data(data["instance_types"], selected_region, cpu_input, memory_input, selected_instance_type, os_choice)
        if filtered_data:
            df = format_data_for_display(filtered_data, instance_data)
            st.table(df)
        else:
            st.write("Nenhuma instância encontrada.")

    # Botão para encontrar a instância mais barata
    if st.button("Encontrar Instância Mais Barata"):
        cheapest_instance = find_cheapest_instance(data["instance_types"])
        if cheapest_instance:
            inst_type, inst_data = cheapest_instance
            df = format_data_for_display({inst_type: inst_data}, instance_data)
            st.write(f"A instância com maior economia é {inst_type}, com uma economia de {inst_data.get('SavingsOverOnDemand', 'N/A')}%.")
            st.table(df)

    # Botão para encontrar a instância mais cara
    if st.button("Encontrar Instância Mais Cara"):
        most_expensive_instance = find_most_expensive_instance(instance_data)
        st.write(f"A instância mais cara é {most_expensive_instance['Nome da instância']}, com uma taxa horária de {most_expensive_instance['Taxa horária sob demanda']}.")
        st.table(most_expensive_instance)
else:
    st.error("Chave 'instance_types' não encontrada nos dados da API.")
