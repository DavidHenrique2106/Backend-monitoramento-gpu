import requests

def get_gpu_data():
    url = "https://7353-181-191-163-189.ngrok-free.app/data.json"  
    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.ConnectionError:
        return {"erro": "Não foi possível conectar ao Open Hardware Monitor"}
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro ao obter os dados da GPU: {str(e)}"}
