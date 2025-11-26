
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor

global_num_threads = 4

def init_display(num_threads):
    print("\n=== PROCESSAMENTO INICIADO ===\n")
    for t in range(1, num_threads + 1):
        print(f"Thread {t:02d} |------------------------------| 0/0")
    print()

def update_bar(thread_id, progress, total):
    bar_length = 30
    filled = int(bar_length * (progress / total))
    bar = "#" * filled + "-" * (bar_length - filled)

    move_up = global_num_threads - thread_id + 1
    print(f"\033[{move_up}A", end="")

    print(f"Thread {thread_id:02d} |{bar}| {progress}/{total}   ")

    print(f"\033[{move_up}B", end="")

def moving_average_chunk(data_slice, window, thread_id):
    result = []
    total = len(data_slice) - window + 1

    for i in range(total):
        janela = data_slice[i:i+window]
        media = np.mean(janela)
        result.append(media)

        update_bar(thread_id, i+1, total)
        time.sleep(0.05)

    return result

def moving_average_multithread(data, window=3, num_threads=4):
    global global_num_threads
    global_num_threads = num_threads

    chunk_size = len(data) // num_threads

    slices = []
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size + window
        slices.append(data[start:end])

    init_display(num_threads)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for thread_id, slice_data in enumerate(slices, start=1):
            futures.append(executor.submit(moving_average_chunk, slice_data, window, thread_id))

        final = []
        for f in futures:
            final.extend(f.result())

    print("\n=== PROCESSAMENTO CONCLUIDO ===\n")
    return final

if __name__ == "__main__":
    temperaturas = [18, 19, 21, 24, 27, 29, 30, 31, 32, 33, 34, 34,
                    33, 32, 30, 29, 27, 26, 24, 23, 22, 21, 20, 19]

    print("Temperaturas do dia (24h):")
    print(temperaturas)

    print("\nCalculando Média Móvel (janela = 3 horas)...")

    resultado = moving_average_multithread(temperaturas, window=3, num_threads=4)

    print("\n=== RESULTADOS DA MÉDIA MÓVEL ===\n")

    print("Temperaturas originais (24 horas):")
    print(temperaturas)

    print("\nPrimeiras previsões da média móvel (janela de 3 horas):")
    for i, valor in enumerate(resultado[:5], start=1):
        a = temperaturas[i-1]
        b = temperaturas[i]
        c = temperaturas[i+1]
        print(f"Hora {i:02d} → ({a} + {b} + {c}) / 3 = {valor:.2f}°C")

    print(f"\nTotal de previsões geradas: {len(resultado)}")