# Servidor Multithread de Predição de Temperaturas

Este projeto consiste num sistema distribuído Cliente-Servidor desenvolvido para a disciplina de Sistemas Distribuídos. O objetivo é demonstrar o processamento paralelo de cálculos de predição (Média Móvel) utilizando sockets e múltiplas threads.

## 📋 Sobre o Projeto

Tema do Trabalho: 4.5 Cálculos de predição (2ª Semana)

Alunos: Igor César da Silva e Paulo Victor

Data: Dezembro/2025

## O Problema

O sistema simula um cenário onde um cliente (ex: uma estação meteorológica) envia um conjunto de dados brutos de temperatura para um servidor central. O servidor deve processar esses dados rapidamente para gerar uma previsão de tendência suavizada.

## A Solução

Implementámos um servidor que utiliza o padrão ThreadPool para dividir o cálculo da Média Móvel Simples (SMA) em várias threads. Isso permite que diferentes segmentos dos dados sejam processados simultaneamente.

## 🚀 Arquitetura

O sistema é dividido em dois scripts Python:

### **servidor_mt.py (O Servidor)**

*Fica à escuta na porta TCP 65432.

*Recebe um payload JSON contendo a lista de temperaturas.

*Multithreading: Divide os dados em "chunks" e atribui cada parte a uma thread real.

*Visualização: Exibe barras de progresso concorrentes no terminal para demonstrar o paralelismo.

*Retorna o resultado processado ao cliente.

### **cliente.py (O Cliente)**

*Contém os dados de teste (24h de medições).

*Conecta-se ao servidor via Socket TCP.

*Envia a requisição e aguarda a resposta (bloqueante).

*Exibe os dados de previsão formatados.

## 🛠️ Requisitos

Python 3.x instalado.

Biblioteca NumPy para cálculos vetoriais.

Para instalar a dependência:

pip install numpy

## 📦 Como Executar

Como é uma aplicação Cliente-Servidor, é necessário abrir dois terminais (prompts de comando) separados.

1. **Iniciar o Servidor**

*No primeiro terminal, execute o servidor. Ele ficará em loop aguardando conexões.

```bash
python servidor_mt.py
```

*Saída esperada: Servidor Multithread ouvindo em 127.0.0.1:65432...

1. **Executar o Cliente**

*No segundo terminal, execute o cliente para enviar os dados.

```bash
python cliente.py
```

1. **Verificar o Resultado**

*No terminal do Servidor: Verá 4 barras de progresso a encherem simultaneamente (simulando o trabalho das threads).

*No terminal do Cliente: Receberá a resposta JSON e verá as médias calculadas:

```bash
=== RESPOSTA DO SERVIDOR ===
Recebidas 22 previsões suavizadas:

Janela 1: 19.33°C
Janela 2: 21.33°C
...
```

## ⚙️ Configuração de Rede (Opcional)

O código vem configurado para rodar em localhost (mesma máquina). Para testar em dois computadores diferentes na mesma rede Wi-Fi:

No Servidor (servidor_mt.py): Mude HOST = '127.0.0.1' para HOST = '0.0.0.0'.

Descubra o IP do Servidor: Execute ipconfig (Windows) ou ifconfig (Linux/Mac).

No Cliente (cliente.py): Mude HOST para o IP do computador do servidor (ex: '192.168.1.15').

Desenvolvido para fins académicos.
