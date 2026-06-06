# MAPI Edge - Coletores e Sensores Virtuais (Fog Computing) 📡🌊

O **MAPI Edge** é o componente de borda do ecossistema MAPI, desenvolvido para monitoramento hidrometeorológico resiliente através de **Fog Computing (Computação em Névoa)**.

Este módulo virtualiza estações de monitoramento físicas das agências **ANA** e **APAC**, aplicando inteligência local para otimização de banda e detecção de anomalias antes do envio dos dados via MQTT.

## 🌐 Ecossistema MAPI

Este projeto é o **produtor de dados primários** do ecossistema. Ele opera de forma integrada com os demais módulos:

```text
  [ MAPI Edge ] (Python / MQTT) 📡 <-- (Este Serviço)
        │   (Pulsações Telemétricas e Inteligência de Borda)
        ▼
  [  MAPI API  ] (Java 21 / Spring Boot / TimescaleDB) 🌊🚀
        │ ▲
        │ │ (Dados em Tempo Real via HTTP POST / Resposta com Probabilidade e Risco)
        ▼ │
  [  MAPI AI  ] (Python / FastAPI / XGBoost & LSTM) 🧠
        │
        │ (Consumo da REST API e Exibição Geoespacial)
        ▼
  [ MAPI Front ] (React 19 / MapLibre GL) 💻✨
```

### Dependências no Ecossistema:
- **MAPI API (Backend):** O Edge atua como um Publisher focado no Broker MQTT orquestrado pela API Central.
- **MAPI AI (Inteligência):** Os payloads gerados aqui são a matéria-prima usada para o treinamento histórico e inferências.
- **MAPI Front (Dashboard):** Dados de telemetria processados na borda são exibidos na interface geoespacial.

## 🛠️ Tecnologias Escolhidas

| Categoria | Tecnologia | Justificativa Técnica |
| :--- | :--- | :--- |
| **Linguagem** | Python 3.12+ | Agilidade para scraping e manipulação numérica. |
| **Mensageria** | Paho-MQTT | Protocolo leve ideal para conectividade instável. |
| **Extração de Dados** | BeautifulSoup4 & Requests | Robustez para scraping (APAC) e WebServices REST (ANA). |
| **Processamento** | XMLtoDict & NumPy | Conversão de XML e processamento matemático de matrizes. |
| **Gestão de Config** | Python-Dotenv | Isolamento seguro de variáveis de ambiente. |

## ✨ Funcionalidades Principais

- **Virtualização de Sensores:** Emula dispositivos físicos, incluindo simulação de drenos e ciclos de recarga solar.
- **Fog Intelligence:** Frequência Adaptativa (aumenta taxa de coleta em anomalias) e Processamento na Borda.
- **Resiliência e Autopreservação:** Modo de economia de energia e "Recarga Solar".
- **Suporte Multi-fonte:** CEMADEN, Meteorologia 24h (APAC) e Rede Telemétrica Nacional (ANA).

## 📂 Estrutura do Projeto

```text
projeto-mapi/
├── src/
│   ├── main.py                # Ponto de entrada da aplicação
│   ├── collectors/            # Agentes de coleta (ANA, APAC, CEMADEN)
│   │   ├── ana_rest_collector.py
│   │   ├── apac_cemaden_collector.py
│   │   ├── apac_meteorologia24h_collector.py
│   │   └── base_collector.py  # Classe base com lógica comum
│   ├── controllers/           # Lógica de negócio e orquestração
│   │   └── sensor_manager.py  # Implementação do Sensor Virtual (Fog)
│   ├── services/              # Serviços de infraestrutura
│   │   ├── auth_manager.py    # Autenticação (OAuth ANA)
│   │   └── mqtt_manager.py    # Conectividade e Publicação MQTT
│   └── utils/                 # Funções utilitárias e processamento de texto
│       └── text_utils.py
├── tests/                     # Suíte de testes automatizados
│   ├── test_battery_logic.py
│   └── test_payload_structure.py
├── extract_rmr_stations.py    # Script utilitário para extração de estações
├── .env.example               # Template de variáveis de ambiente
├── requirements.txt           # Dependências do projeto
└── README.md                  # Documentação principal
```

## 📋 Instruções de Execução

### 1. Preparação do Ambiente
Certifique-se de ter o Python 3.12+ instalado. Recomenda-se o uso de ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate     # Windows
```

### 2. Instalação de Dependências
```bash
pip install -r requirements.txt
```

### 3. Configuração
Crie o arquivo `.env` a partir do exemplo e ajuste as credenciais e configurações do Broker MQTT:
```bash
cp .env.example .env
```

### 4. Inicialização
Para rodar a malha de coletores e sensores virtuais:
```bash
python -m src.main
```

## 📊 Exemplo de Payload (MQTT)

```json
{
  "id_sensor": "ANA-TELE-CAPIBARIBE-SLM",
  "timestamp_coleta": "2026-06-04T10:30:00.123456",
  "status_bateria": "98.5%",
  "fog_valor_referencia": 12.5,
  "nivel": 12.5,
  "chuva": 0.0,
  "vazao": 45.2
}
```

## 📄 Licença
Este projeto está sob a licença **MIT**.
