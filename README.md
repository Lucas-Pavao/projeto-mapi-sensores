# Projeto MAPI - Monitoramento de Águas e Pluviometria Inteligente 📡🌊

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Architecture](https://img.shields.io/badge/architecture-Fog%20Computing-orange)

O **Projeto MAPI** é uma solução avançada de **Fog Computing (Computação em Névoa)** e virtualização de sensores voltada para o monitoramento hidrometeorológico. Ele atua como um middleware inteligente que extrai, normaliza e processa dados ambientais de órgãos oficiais (ANA e APAC), transformando-os em fluxos de dados em tempo real via protocolo MQTT.

## 📋 Descrição Geral

O sistema funciona através de uma malha de **Sensores Virtuais**. Em vez de depender exclusivamente de hardware físico, o MAPI "virtualiza" estações de monitoramento governamentais, aplicando lógica de borda para detectar anomalias (como subida rápida de rios ou chuvas intensas). 

Diferente de uma coleta simples, o MAPI implementa **Inteligência de Borda**: quando uma anomalia é detectada, o sensor virtual aumenta automaticamente sua frequência de coleta (polling), garantindo dados granulares em momentos críticos sem sobrecarregar a rede em períodos de normalidade.

## ✨ Funcionalidades Principais

- **Virtualização Multi-Fonte:** Integração nativa com:
  - **APAC:** Scraping de dados meteorológicos e pluviométricos (Cemaden).
  - **ANA:** Integração com WebService REST via autenticação OAuth2.
- **Lógica de Fog Computing:** Adaptação dinâmica do intervalo de coleta baseada no comportamento dos dados.
- **Processamento de Borda:** Limpeza, normalização e "achatamento" (flattening) de payloads complexos antes do envio.
- **Simulação de Telemetria:** Cada sensor virtual simula status de bateria, ciclos de carga/descarga e telemetria de sinal.
- **Concorrência Escalável:** Arquitetura baseada em threads que permite monitorar centenas de estações simultaneamente.
- **Integração MQTT:** Publicação de dados em tópicos hierárquicos para fácil consumo por dashboards ou sistemas de alerta.

## 🛠️ Tecnologias Utilizadas

### Core
- **Python 3.12+**: Linguagem base do projeto.
- **Threading**: Para execução paralela de sensores virtuais.

### Integração e Dados
- **Requests & BeautifulSoup4**: Extração e scraping de dados governamentais.
- **Paho-MQTT**: Protocolo de comunicação leve para IoT.
- **XMLtoDict**: Conversão de respostas SOAP/XML da ANA para formatos amigáveis.
- **Python-Dotenv**: Gerenciamento de variáveis de ambiente.

## 🏗️ Arquitetura e Estrutura de Pastas

O projeto segue um padrão modular baseado em agentes:

```text
projeto-mapi/
├── src/
│   ├── collectors/      # Agentes de extração (ANA, APAC, Base)
│   ├── controllers/     # Lógica do VirtualSensor e gerenciamento de anomalias
│   ├── services/        # Infraestrutura (MQTT, Auth Manager)
│   ├── utils/           # Processamento de texto e normalização
│   └── main.py          # Orquestrador e ponto de entrada
├── tests/               # Testes unitários e de integração
├── .env.example         # Template de configuração
├── AGENTS.md            # Documentação detalhada dos agentes
└── README.md            # Documentação principal
```

## ⚙️ Pré-requisitos

Antes de iniciar, você precisará ter instalado:
- **Python 3.12** ou superior.
- **Broker MQTT** (Ex: Mosquitto local ou brokers públicos como HiveMQ/EMQX).
- **Pip** (Gerenciador de pacotes do Python).

## 🚀 Como Executar o Projeto

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/projeto-mapi.git
cd projeto-mapi
```

### 2. Configurar Ambiente Virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate     # Windows
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Copie o arquivo `.env.example` para `.env` e preencha com suas credenciais:
```bash
cp .env.example .env
```
> **Nota:** Para acesso à API da ANA, é necessário possuir um `identificador` e `senha` válidos fornecidos pelo órgão.

### 5. Executar o Sistema
```bash
python src/main.py
```

## 📡 Exemplos de Uso (Payload MQTT)

O sistema publica dados no tópico configurado (padrão: `projeto-mapi/sensores/{id_sensor}`). Exemplo de payload enviado:

```json
{
  "id_sensor": "APAC-METEO-RECIFE",
  "estacao_nome": "Recife (Curado)",
  "municipio": "Recife",
  "temperatura": 28.5,
  "umidade": 75,
  "chuva_acumulada": 0.0,
  "status_bateria": 98.5,
  "fog_modo_critico": false,
  "fog_valor_referencia": 0.0,
  "timestamp": "2024-05-24T14:30:00Z"
}
```

## 🤝 Como Contribuir

1. Faça um **Fork** do projeto.
2. Crie uma **Branch** para sua feature (`git checkout -b feature/nova-funcionalidade`).
3. Faça o **Commit** de suas alterações (`git commit -m 'Adiciona nova funcionalidade'`).
4. Faça o **Push** para a Branch (`git push origin feature/nova-funcionalidade`).
5. Abra um **Pull Request**.

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
**Desenvolvido como parte da camada de inteligência para prevenção de desastres naturais.**
