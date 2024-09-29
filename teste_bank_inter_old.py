import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import aiofiles
import requests

# Inicializando a aplicação FastAPI
app = FastAPI()

# Caminho absoluto para a pasta 'static'
static_dir = os.path.join(os.path.dirname(__file__), "static")

# Montar a pasta 'static' para servir arquivos estáticos como CSS ou JS
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Servir o arquivo HTML principal ('index.html')
@app.get("/", response_class=HTMLResponse)
async def serve_html():
    # Certifique-se de que o caminho aponta para o 'index.html' dentro da pasta 'static'
    async with aiofiles.open(os.path.join(static_dir, "index.html"), mode="r") as f:
        content = await f.read()
    return HTMLResponse(content=content)

# Endpoint de exemplo para pegar dados de uma API externa (opcional)
@app.get("/spot_instances")
def get_spot_instances():
    url = "https://spot-bid-advisor.s3.amazonaws.com/spot-advisor-data.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": f"Erro ao acessar a API. Status Code: {response.status_code}"}

    data = response.json()
    
    try:
        return {"instance_types": data["instance_types"]}
    except KeyError as e:
        return {"error": f"Erro ao acessar os dados: {e}"}

# Endpoint para filtrar as instâncias (opcional)
@app.get("/spot_instances/filter")
def filter_spot_instances(region: str = None, cpu: int = None, memory: int = None, instance_type: str = None):
    url = "https://spot-bid-advisor.s3.amazonaws.com/spot-advisor-data.json"
    response = requests.get(url)
    data = response.json()

    try:
        instance_data = data["instance_types"]

        # Filtrar as instâncias com base nos parâmetros fornecidos
        filtered_instances = {}
        for inst_type, inst_info in instance_data.items():
            if region and inst_info['region'] != region:
                continue
            if cpu and not (cpu * 0.8 <= inst_info['vCPU'] <= cpu * 1.2):
                continue
            if memory and inst_info['MemoryGiB'] < memory:
                continue
            if instance_type and instance_type != inst_type:
                continue
            filtered_instances[inst_type] = inst_info

        return {"instance_types": filtered_instances}
    except KeyError as e:
        return {"error": f"Erro ao acessar os dados: {e}"}
