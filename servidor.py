import socket
import json
import threading
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# Configurações do Servidor
HOST = '0.0.0.0'  # Localhost
PORT = 65432        # Porta para escutar

# --- LÓGICA DE MULTITHREADING (A tua lógica original) ---
global_num_threads = 4

def update_bar(thread_id, progress, total):
    """Atualiza a barra de progresso no terminal do SERVIDOR."""
    bar_length = 30
    filled = int(bar_length * (progress / total))
    bar = "#" * filled + "-" * (bar_length - filled)
    
    # Move o cursor para a linha correta da thread
    move_up = global_num_threads - thread_id + 1
    print(f"\033[{move_up}A", end="")
    print(f"Thread {thread_id:02d} |{bar}| {progress}/{total}   ")
    print(f"\033[{move_up}B", end="")

def moving_average_chunk(data_slice, window, thread_id):
    """Função que cada thread executa para processar sua parte."""
    result = []
    total = len(data_slice) - window + 1
    
    for i in range(total):
        janela = data_slice[i:i+window]
        media = np.mean(janela)
        result.append(media)
        
        # Simula trabalho pesado para vermos a barra a mexer
        update_bar(thread_id, i+1, total)
        time.sleep(0.1) # Aumentei um pouco para ficar mais visual na apresentação
        
    return result

def processar_dados(dados, window=3, num_threads=4):
    """Gerencia a divisão do trabalho e o ThreadPool."""
    global global_num_threads
    global_num_threads = num_threads
    
    chunk_size = len(dados) // num_threads
    slices = []
    
    # Divide os dados em pedaços (chunks)
    for i in range(num_threads):
        start = i * chunk_size
        # Precisamos de um pouco mais de dados (window) para as bordas
        end = start + chunk_size + window if i < num_threads - 1 else len(dados) + window
        # Nota: O slicing simples pode perder bordas, mas para fins didáticos:
        slices.append(dados[start:min(end, len(dados))])

    print(f"\n=== INICIANDO PROCESSAMENTO PARALELO ({num_threads} Threads) ===\n")
    # Prepara espaço visual para as barras
    for t in range(1, num_threads + 1):
        print(f"Thread {t:02d} |------------------------------| 0/0")
    print()

    # Executa as threads
    results_ordered = [None] * num_threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i, slice_data in enumerate(slices):
            # Envia thread_id = i+1
            futures.append(executor.submit(moving_average_chunk, slice_data, window, i+1))
        
        # Coleta resultados
        final_result = []
        for f in futures:
            final_result.extend(f.result())
            
    print("\n=== PROCESSAMENTO CONCLUÍDO ===")
    return final_result

# --- LÓGICA DE REDE (SOCKETS) ---

def iniciar_servidor():
    # Cria o socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor Multithread ouvindo em {HOST}:{PORT}...")
        print("Aguardando conexão do cliente...")

        conn, addr = s.accept() # Bloqueia até um cliente conectar
        with conn:
            print(f"Conectado por: {addr}")
            
            # 1. Recebe os dados do cliente
            data = conn.recv(4096)
            if not data: return
            
            # Decodifica o JSON recebido
            request = json.loads(data.decode('utf-8'))
            temperaturas = request['dados']
            
            print(f"Recebidos {len(temperaturas)} registros de temperatura.")
            
            # 2. Processa usando Multithreading
            resultado = processar_dados(temperaturas)
            
            # 3. Envia a resposta de volta
            response = json.dumps({'resultado': resultado})
            conn.sendall(response.encode('utf-8'))
            print("Resposta enviada ao cliente.")

if __name__ == "__main__":
    iniciar_servidor()