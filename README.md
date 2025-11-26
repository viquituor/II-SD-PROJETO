# Média Móvel Multithread: Análise de Temperaturas

Este projeto implementa um cálculo de **Média Móvel Simples (SMA)** utilizando processamento paralelo (multithreading) em Python. O algoritmo simula o processamento de leituras de temperatura ao longo de um ciclo de 24 horas, demonstrando conceitos de concorrência e visualização de progresso em tempo real no terminal.

## 📋 Sobre o Projeto

O objetivo principal é demonstrar como dividir uma tarefa de processamento de dados (séries temporais) em "chunks" (fragmentos) independentes que são processados simultaneamente por múltiplas threads.

O script:

1. Gera um conjunto de dados de 24 temperaturas (uma por hora).
2. Aplica uma janela deslizante de 3 horas para calcular a média móvel.
3. Divide o processamento entre 4 threads reais.
4. Exibe o progresso de cada thread individualmente com barras de carregamento dinâmicas.

## 🚀 Funcionalidades

* **Processamento Concorrente:** Utiliza `concurrent.futures.ThreadPoolExecutor` para gerir as threads.
* **Visualização em Tempo Real:** Implementação de barras de progresso via códigos de escape ANSI, permitindo a atualização de linhas específicas no terminal sem limpar o ecrã.
* **Segmentação de Dados:** Lógica de "slicing" inteligente que preserva a integridade da janela de média móvel nas bordas dos fragmentos de dados.
* **Bibliotecas:** Uso do `NumPy` para cálculos vetoriais eficientes.

## 🛠️ Requisitos

* Python 3.x
* Biblioteca `numpy`

## 📦 Instalação e Execução

1. **Instalar as dependências:**

   ```bash
   pip install numpy
   ```
