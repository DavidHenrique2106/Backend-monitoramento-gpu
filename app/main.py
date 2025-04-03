import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from app.services import get_gpu_data

app = FastAPI()

@app.websocket("/ws/gpu")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Cliente conectado ao WebSocket.")
    
    while True:
        gpu_data = get_gpu_data()
        await websocket.send_json(gpu_data)
        await asyncio.sleep(5)

@app.get("/")
async def get():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Monitor de GPU</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
            pre { background: #f4f4f4; padding: 10px; border-radius: 5px; text-align: left; }
        </style>
    </head>
    <body>
        <h1>Monitor de GPU em Tempo Real</h1>
        <pre id="gpuData">Conectando...</pre>
        
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

            socket.onclose = function() {
                console.log("Conexão WebSocket fechada. Tentando reconectar...");
                setTimeout(() => {
                    location.reload(); 
                }, 5000);
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
