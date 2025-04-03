import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

def get_gpu_data():
    url = "https://7353-181-191-163-189.ngrok-free.app"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        return resposta.json()
    except requests.RequestException as e:
        return {"erro": "Não foi possível obter os dados da GPU"}

@app.websocket("/ws/gpu")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        gpu_data = get_gpu_data()
        await websocket.send_json(gpu_data)
        await asyncio.sleep(60)  

@app.get("/")
async def get():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Monitor de GPU</title>
    </head>
    <body>
        <h1>Dados da GPU</h1>
        <pre id="gpuData">Carregando dados...</pre>
        
        <script>
            let socket = new WebSocket("wss://backend-monitoramento-gpu.onrender.com/ws/gpu");
            socket.onmessage = function(event) {
                const gpuData = JSON.parse(event.data);
                document.getElementById('gpuData').textContent = JSON.stringify(gpuData, null, 2);
            };
            socket.onopen = function() {
                console.log("Conexão WebSocket aberta.");
            };
            socket.onerror = function(error) {
                console.error("Erro WebSocket:", error);
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
