import socket
import asyncio
import websockets
import base64
import os

# 🔹 Configuración TCP
HOST = "0.0.0.0"  # Escuchar en todas las interfaces
PORT = 5000

# 🔹 Configuración Deepgram
DEEPGRAM_API_KEY = "e207917d9a5bdf8afec7de52e9d016a3809a3a6a"  # pon aquí tu API key
DEEPGRAM_URL = "wss://api.deepgram.com/v1/listen?punctuate=true&language=es"

# Buffer de audio recibido
audio_buffer = bytearray()

async def send_to_deepgram(audio_chunk):
    # Convertimos el chunk a base64
    data_b64 = base64.b64encode(audio_chunk).decode("utf-8")
    
    headers = [("Authorization", f"Token {DEEPGRAM_API_KEY}")]
    
    async with websockets.connect(DEEPGRAM_URL, extra_headers=headers) as ws:
        # Enviamos el audio
        await ws.send(data_b64)
        
        # Recibimos la transcripción
        async for message in ws:
            print("📝 Deepgram:", message)
            break  # sacamos la primera respuesta

def receive_audio_tcp():
    global audio_buffer
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"🎧 Servidor TCP escuchando en {HOST}:{PORT}")
        conn, addr = s.accept()
        print("✅ Conexión establecida con", addr)
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                audio_buffer += data

async def main():
    loop = asyncio.get_event_loop()
    # Recibir audio en un hilo separado para no bloquear asyncio
    await loop.run_in_executor(None, receive_audio_tcp)
    
    # Cuando termine de recibir, enviamos a Deepgram
    if audio_buffer:
        print("📦 Datos recibidos:", len(audio_buffer), "bytes")
        await send_to_deepgram(audio_buffer)

if __name__ == "__main__":
    asyncio.run(main())

