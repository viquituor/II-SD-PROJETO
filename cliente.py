import socket
import json

# Configurações (devem bater com o servidor)
HOST = '192.168.1.14'
PORT = 65432

# Dados para teste (24 horas)
temperaturas_dia = [18, 19, 21, 24, 27, 29, 30, 31, 32, 33, 34, 34,
                    33, 32, 30, 29, 27, 26, 24, 23, 22, 21, 20, 19]

def enviar_tarefa():
    print(f"Conectando ao servidor {HOST}:{PORT}...")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            
            # Prepara os dados em formato JSON
            mensagem = {
                'dados': temperaturas_dia,
                'acao': 'calcular_media_movel'
            }
            data_json = json.dumps(mensagem)
            
            print("Enviando dados de temperatura...")
            s.sendall(data_json.encode('utf-8'))
            
            # Aguarda a resposta (bloqueante)
            print("Aguardando processamento do servidor...")
            data = s.recv(4096)
            
            resposta = json.loads(data.decode('utf-8'))
            resultados = resposta['resultado']
            
            print("\n=== RESPOSTA DO SERVIDOR ===")
            print(f"Recebidas {len(resultados)} previsões suavizadas:\n")
            
            # Formatação bonita para exibir
            for i, val in enumerate(resultados[:5]): # Mostra só os 5 primeiros
                print(f"Janela {i+1}: {val:.2f}°C")
            print("...")
            
    except ConnectionRefusedError:
        print("ERRO: Não foi possível conectar. O servidor está rodando?")

if __name__ == "__main__":
    enviar_tarefa()