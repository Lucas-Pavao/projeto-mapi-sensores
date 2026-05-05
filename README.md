# Sistema de Monitoramento Ambiental Distribuído (projeto-mapi)

Este projeto, batizado internamente como `projeto-mapi`, é um sistema de monitoramento ambiental distribuído que simula uma arquitetura de Edge/Fog Computing. Ele foi projetado para coletar, processar e unificar dados meteorológicos e hidrológicos de múltiplas fontes em tempo real, integrando agora comunicação via protocolo **MQTT**.

## Tabela de Conteúdos
- [Sobre o Projeto](#sobre-o-projeto)
- [Principais Características](#principais-características)
- [Arquitetura e Tecnologias](#arquitetura-e-tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Começar](#como-começar)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)
- [Configuração](#configuração)
  - [MQTT](#mqtt)
  - [API da ANA](#api-da-ana)
- [Como Executar](#como-executar)

## Sobre o Projeto

O sistema utiliza um modelo de **Sensores Virtuais Paralelos**. Cada ponto de monitoramento e cada tipo de dado funciona como um "nó" independente, executando sua coleta de forma paralela e publicando os resultados em um broker MQTT.

- **Multithreading**: Cada sensor virtual roda em uma thread independente, garantindo alta disponibilidade e resiliência a falhas de rede.
- **Comunicação MQTT**: Todos os dados coletados são publicados em tópicos estruturados, permitindo a integração fácil com dashboards (como Node-RED ou Grafana) e outros sistemas.
- **Modularidade**: Divisão clara entre coletores de dados, gerenciamento de sensores e serviços de comunicação.

## Principais Características

- **3 Malhas de Sensores Virtuais**:
  1. **Clima (APAC Meteorologia 24h)**: Temperatura, umidade do ar, radiação solar e umidade do solo.
  2. **Pluviômetros (APAC Cemaden)**: Precipitação acumulada e dados geotécnicos.
  3. **Telemétricos (ANA)**: Nível de rios, vazão e chuva adotada via API REST.
- **Protocolo MQTT**: Publicação automática no tópico `projeto-mapi/sensores/{ID_SENSOR}`.
- **Refatoração Orientada a Objetos**: Utilização de classes base para coletores, minimizando duplicação de código.

## Arquitetura e Tecnologias

- **Linguagem**: Python 3.x
- **Bibliotecas Principais**:
    - `paho-mqtt`: Comunicação com o broker MQTT.
    - `requests`: Requisições HTTP/REST para as APIs.
    - `beautifulsoup4`: Parsing de dados quando necessário.
    - `python-dotenv`: Gerenciamento de variáveis de ambiente.
    - `threading`: Execução paralela dos sensores.

## Estrutura do Projeto

```
projeto-mapi/
├── requirements.txt
├── src/
│   ├── main.py                 # Ponto de entrada do sistema
│   ├── collectors/
│   │   ├── base_collector.py   # Lógica base para coletores APAC
│   │   ├── ana_rest_collector.py
│   │   ├── apac_cemaden_collector.py
│   │   └── apac_meteorologia24h_collector.py
│   ├── controllers/
│   │   └── sensor_manager.py   # Gerenciamento do ciclo de vida do sensor
│   ├── services/
│   │   ├── auth_manager.py     # Autenticação (ANA)
│   │   └── mqtt_manager.py     # Cliente MQTT
│   └── utils/
│       └── text_utils.py       # Tratamento de strings e acentos
└── ...
```

## Como Começar

### Pré-requisitos
- Python 3.8+
- Broker MQTT (Ex: HiveMQ, Mosquitto ou local)

### Instalação

1. **Clone o repositório:**
   ```sh
   git clone <url-do-seu-repositorio>
   cd projeto-mapi
   ```

2. **Crie e ative um ambiente virtual:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

## Configuração

O sistema utiliza variáveis de ambiente para todas as suas configurações críticas. Crie um arquivo `.env` na raiz do projeto baseando-se no arquivo `.env.example`.

### Variáveis de Ambiente (.env)

```ini
# APAC Config
APAC_BASE_URL=http://dados.apac.pe.gov.br:41120
APAC_CEMADEN_ENDPOINT=cemaden
APAC_METEOROLOGIA_ENDPOINT=meteorologia24h

# ANA Config
ANA_AUTH_URL=https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/OAUth/v1
ANA_BASE_URL=https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroinfoanaSerieTelemetricaAdotada/v1
ANA_IDENTIFICADOR="seu_identificador"
ANA_SENHA="sua_senha"

# MQTT Config
MQTT_BROKER=broker.hivemq.com
MQTT_PORT=1883
MQTT_TOPIC_PREFIX=projeto-mapi/sensores
```

*Para obter credenciais da ANA, envie e-mail para hidro@ana.gov.br.*

## Como Executar

Inicie o sistema com:
```sh
python src/main.py
```

O sistema irá:
1. Conectar ao Broker MQTT.
2. Iniciar threads para cada sensor das cidades alvo.
3. Coletar e publicar dados periodicamente.
4. Exibir o status das leituras no console.
