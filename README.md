# Projeto MAPI - Monitoramento e Fog Computing 📡🐍

O **Projeto MAPI (Python)** atua como a camada de **Fog Computing (Computação em Névoa)** e virtualização de sensores da solução MAPI. Este middleware é responsável por extrair, normalizar e processar dados ambientais de diversas fontes oficiais, transformando-os em fluxos de dados inteligentes via MQTT.

## 📋 O que é o projeto?

O projeto funciona como uma malha de **Sensores Virtuais**. Em vez de depender apenas de hardware físico caro, o sistema "virtualiza" estações de monitoramento governamentais (ANA e APAC), coletando seus dados em tempo real e aplicando lógica de borda para detectar anomalias antes mesmo dos dados chegarem à nuvem.

## 🏗️ Arquitetura

O sistema utiliza uma arquitetura modular baseada em **Agentes e Controladores**, projetada para alta resiliência e concorrência:

1.  **Coletores (Collectors):** Módulos especializados em "scraping" ou consumo de APIs REST. Cada órgão (ANA, APAC) possui seu próprio coletor que conhece as nuances da extração de dados brutos.
2.  **Sensores Virtuais (VirtualSensors):** A inteligência central. Cada sensor virtual representa um ponto de monitoramento geográfico. Ele decide quando aumentar a frequência de coleta baseado nos dados recebidos (Lógica de Fog).
3.  **Gerenciador de Mensagens (MQTT Manager):** Responsável por formatar os dados processados em JSON e publicá-los em tópicos MQTT para consumo da API Spring Boot.
4.  **Orquestrador (Main):** Gerencia o ciclo de vida de múltiplos sensores virtuais rodando em threads paralelas, permitindo o monitoramento simultâneo de várias bacias hidrográficas e cidades.

## 📂 Estrutura do Projeto

```text
src/
├── collectors/      # Agentes de extração (ANA, APAC, CEMADEN)
├── controllers/     # Lógica do VirtualSensor e gerenciamento de anomalias
├── services/        # Serviços de infraestrutura (MQTT, Auth OAuth2 para ANA)
├── utils/           # Funções auxiliares de processamento de texto e dados
└── main.py          # Ponto de entrada e orquestração de threads
```

## ⚙️ Como o projeto funciona?

1.  **Coleta Inteligente:** O sistema inicia múltiplos `VirtualSensors` em threads separadas. Cada um busca dados de fontes como o WebService da ANA ou o portal da APAC.
2.  **Lógica de Fog Computing:** Se um sensor detecta uma anomalia (ex: nível de rio subindo rápido ou chuva forte), ele entra em "Modo Crítico" e aumenta automaticamente sua frequência de polling (ex: de 10 minutos para 30 segundos).
3.  **Processamento de Borda:** Os dados são limpos e normalizados localmente, simulando o comportamento de um dispositivo IoT físico (incluindo status de bateria e telemetria).
4.  **Publicação MQTT:** O resultado é enviado para um Broker MQTT. A API central (Java) escuta esses tópicos e persiste os dados para o dashboard.

## 🚀 Tecnologias Utilizadas

- **Python 3.12+**
- **MQTT (Paho-MQTT)**
- **BeautifulSoup4** (Scraping de dados governamentais)
- **Requests** (Consumo de APIs)
- **Threading** (Concorrência para múltiplos sensores)
- **OAuth2** (Autenticação para serviços oficiais)

---
**Camada de inteligência distribuída para prevenção de desastres.**
