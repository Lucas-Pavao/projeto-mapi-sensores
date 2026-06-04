# Projeto MAPI - Coletores e Sensores Virtuais (Fog Computing) 📡🌊

O **Projeto MAPI** (Monitoramento de Águas e Pluviometria Inteligente) é uma solução de **Fog Computing (Computação em Névoa)** desenvolvida para o monitoramento hidrometeorológico resiliente. Este repositório contém a "Malha de Sensores Virtuais", que atua como a camada de borda do ecossistema MAPI.

O sistema virtualiza estações de monitoramento físicas das agências **ANA (Agência Nacional de Águas)** e **APAC (Agência Pernambucana de Águas e Clima)**, aplicando inteligência local para otimização de banda e detecção de anomalias antes de enviar os dados para a nuvem.

---

## 🚀 Integração com o Ecossistema MAPI

Este projeto é o **produtor de dados** do ecossistema. Ele trabalha em conjunto com a **MAPI API**, que processa e armazena as informações enviadas via MQTT.

- **Central API:** [projeto-mapi-api](/home/lucas/Documents/Projetos/MAPI/projeto-mapi-api)
- **Fluxo de Dados:** 
  1. `Coletores` buscam dados brutos de APIs Governamentais.
  2. `Sensores Virtuais` processam os dados (Fog Logic).
  3. Dados são publicados via `MQTT`.
  4. `MAPI API` subscreve os tópicos e disponibiliza para o Dashboard/Usuários.

---

## 🛠️ Tecnologias Escolhidas

- **Linguagem:** [Python 3.12+](https://www.python.org/)
- **Protocolo de Comunicação:** [Paho-MQTT](https://eclipse.org/paho/index.php?page=clients/python/index.php) (Ideal para IoT e baixa latência).
- **Web Scraping & APIs:**
  - `BeautifulSoup4`: Extração de dados de portais HTML da APAC.
  - `Requests`: Consumo de APIs REST (ANA).
  - `XMLtoDict`: Conversão de respostas SOAP/XML da ANA para JSON.
- **Inteligência de Borda:** Lógica personalizada para detecção de anomalias (Média Móvel).
- **Configuração:** `Python-Dotenv` para gestão de segredos e URLs.

---

## ✨ Funcionalidades Principais

- **Virtualização de Sensores:** Emula o comportamento de dispositivos físicos (incluindo simulação de dreno e recarga de bateria solar).
- **Fog Intelligence (Inteligência de Névoa):**
  - **Frequência Adaptativa:** O sensor aumenta a taxa de coleta automaticamente ao detectar anomalias (ex: aumento súbito no nível do rio ou chuva forte).
  - **Processamento na Borda:** Filtragem e normalização de dados antes da transmissão.
- **Resiliência:** Capaz de operar em modo de "Recarga Solar" quando a bateria virtual se esgota, suspendendo transmissões não essenciais.
- **Suporte Multi-fonte:** Integração nativa com CEMADEN, Meteorologia 24h (APAC) e Rede Telemétrica Nacional (ANA).

---

## 📂 Estrutura do Projeto

```text
projeto-mapi/
├── src/
│   ├── collectors/      # Agentes de extração (Scraping APAC e REST ANA)
│   │   ├── ana_rest_collector.py     # Integração com WebService da ANA
│   │   ├── apac_cemaden_collector.py # Scraping de pluviômetros
│   │   └── base_collector.py         # Classe base com lógica de cache
│   ├── controllers/     # Orquestração e Lógica de Negócio
│   │   └── sensor_manager.py         # Implementação do Sensor Virtual (Fog Logic)
│   ├── services/        # Serviços de infraestrutura
│   │   ├── auth_manager.py           # Gestão de Tokens OAUTH (ANA)
│   │   └── mqtt_manager.py           # Cliente de publicação MQTT
│   ├── utils/           # Utilitários (Normalização de texto, filtros RMR)
│   └── main.py          # Ponto de entrada (Bootstrapping da malha)
├── tests/               # Testes automatizados (Lógica de bateria e payloads)
├── .env.example         # Exemplo de configurações necessárias
├── requirements.txt     # Dependências Python
└── README.md            # Documentação principal
```

---

## 📋 Instruções de Execução

### 1. Pré-requisitos
- Python 3.12 ou superior.
- Um Broker MQTT ativo (recomendado: Mosquitto ou HiveMQ).

### 2. Instalação
```bash
# Clone o repositório
git clone https://github.com/Lucas-Pavao/projeto-mapi-sensores.git
cd projeto-mapi-sensores

# Crie o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configuração
Crie um arquivo `.env` baseado no `.env.example`:
```bash
cp .env.example .env
```
Edite as variáveis `MQTT_BROKER`, `MQTT_PORT` e `MQTT_TOPIC_PREFIX` conforme necessário.

### 4. Rodando a Malha de Sensores
```bash
python -m src.main
```

---

## 📊 Exemplo de Payload (MQTT)

Os dados são publicados no tópico `projeto-mapi/sensores/{ID_DO_SENSOR}` no formato JSON:

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

---

## 📄 Licença
Este projeto está sob a licença **MIT**.
