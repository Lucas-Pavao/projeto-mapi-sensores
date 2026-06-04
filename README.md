# Projeto MAPI - Coletores e Sensores Virtuais 📡🌊

O **Projeto MAPI** é uma solução de **Fog Computing (Computação em Névoa)** projetada para o monitoramento hidrometeorológico inteligente na Região Metropolitana do Recife. Ele atua como um middleware que virtualiza estações de monitoramento governamentais (ANA e APAC), aplicando lógica de borda para detecção de anomalias e otimização da transmissão de dados via MQTT.

## 🛠️ Tecnologias Escolhidas

- **Linguagem:** Python 3.12+
- **Comunicação:** Paho-MQTT (Protocolo IoT)
- **Extração de Dados:** BeautifulSoup4, Requests, XMLtoDict
- **Processamento:** Threading (para gerenciamento paralelo de sensores)
- **Configuração:** Python-Dotenv

## ✨ Funcionalidades / Features

- 🔄 **Virtualização de Sensores:** Simula o comportamento de dispositivos físicos a partir de dados de APIs governamentais.
- 🧠 **Inteligência de Borda (Edge Intelligence):** Adaptação dinâmica da frequência de coleta baseada na detecção de anomalias (ex: aumento de chuva ou nível do rio).
- 📡 **Coleta Multi-fonte:** Integração com WebServices da ANA e Scraping de dados da APAC e CEMADEN.
- ⚡ **Baixa Latência:** Publicação de dados em tempo real via protocolo MQTT para consumo pela API central.

## 📂 Estrutura de Pastas

```text
projeto-mapi/
├── src/
│   ├── collectors/      # Agentes de extração (Scraping/API ANA e APAC)
│   ├── controllers/     # Lógica de Fog e Gerenciamento de Sensores Virtuais
│   ├── services/        # Gestão de Autenticação e Conexão MQTT
│   ├── utils/           # Funções auxiliares e normalização de dados
│   └── main.py          # Ponto de entrada e orquestração do sistema
├── tests/               # Suite de testes unitários e integração
├── .env.example         # Template de variáveis de ambiente
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação principal
```

## 📋 Pré-requisitos

- Python 3.12 ou superior instalado.
- Acesso a um Broker MQTT (ex: Mosquitto, HiveMQ).
- Pip (gerenciador de pacotes do Python).

## 🚀 Como instalar e rodar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Lucas-Pavao/projeto-mapi-sensores.git
   cd projeto-mapi-sensores
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações de MQTT e APIs
   ```

5. **Execute a aplicação:**
   ```bash
   python -m src.main
   ```

## 🤝 Como contribuir

1. Faça um **Fork** do projeto.
2. Crie uma **Branch** para sua modificação (`git checkout -b feature/minha-feature`).
3. Faça o **Commit** de suas alterações (`git commit -m 'Add: nova funcionalidade'`).
4. Faça o **Push** para a sua Branch (`git push origin feature/minha-feature`).
5. Abra um **Pull Request**.

## 📄 Licença

Este projeto está sob a licença **MIT**.
