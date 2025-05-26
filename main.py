from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import base64
import cv2
import numpy as np
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        import json
        frame_data = json.loads(data)

        if frame_data["type"] == "frame":
            img_data = base64.b64decode(frame_data["data"].split(',')[1])
            img = Image.open(io.BytesIO(img_data)).convert("RGB")
            np_img = np.array(img)

            # Processamento de exemplo: desenho de retângulo
            cv_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
            cv2.rectangle(cv_img, (50, 50), (200, 200), (0, 255, 0), 3)
            _, jpeg = cv2.imencode('.jpg', cv_img)
            b64_img = base64.b64encode(jpeg.tobytes()).decode('utf-8')

            # Envia imagem processada e texto
            await websocket.send_text(json.dumps({"type": "image", "data": f"data:image/jpeg;base64,{b64_img}"}))
            await websocket.send_text(json.dumps({"type": "text", "data": "Vire à direita"}))
