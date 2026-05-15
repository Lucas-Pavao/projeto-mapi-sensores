# Projeto MAPI - Monitoramento de Águas e Pluviometria Inteligente

O **Projeto MAPI** é uma solução de IoT industrial e ambiental focada no monitoramento em tempo real de níveis de rios e índices pluviométricos. O sistema utiliza o conceito de **Virtualização de Sensores** e **Fog Computing (Computação em Névoa)** para integrar dados de múltiplas fontes governamentais (ANA e APAC) e disponibilizá-los via protocolo MQTT para plataformas de análise e dashboards.

---

## 🏗️ Arquitetura do Sistema

O projeto segue um modelo de camadas para garantir resiliência e modularidade:

1.  **Camada de Coleta (Collectors):** Agents especializados em fazer scraping ou consumir APIs REST de órgãos oficiais.
2.  **Camada de Controle (Fog/Edge):** Gerencia sensores virtuais, aplica lógica de detecção de anomalias e ajusta a frequência de amostragem dinamicamente.
3.  **Camada de Serviços:** Gerenciamento de comunicações (MQTT) e autenticação segura (OAuth).
4.  **Orquestração:** Gerenciamento de concorrência via Threads para monitoramento simultâneo de múltiplas cidades e estações.

---

## 📂 Estrutura de Arquivos e Funções

### 🌍 `/src` (Core do Sistema)
*   **`main.py`**: O orquestrador central. Inicializa os serviços, define as cidades e estações alvo, e provisiona os sensores virtuais em threads separadas para garantir execução paralela.

### 📡 `/src/collectors` (Agentes de Coleta)
Responsáveis por buscar dados brutos e normalizá-los.
*   **`base_collector.py`**: Classe base para coletores APAC. Contém a lógica de extração de JSON embutido em HTML usando BeautifulSoup e filtragem por cidade.
*   **`apac_cemaden_collector.py`**: Coleta dados de pluviômetros (chuva) da rede Cemaden via portal da APAC.
*   **`apac_meteorologia24h_collector.py`**: Coleta dados meteorológicos completos (temperatura, umidade, vento, pressão) das últimas 24h.
*   **`ana_rest_collector.py`**: Interface com o WebService da ANA. Gerencia o consumo de dados de telemetria (nível, vazão e chuva) usando tokens de autenticação.

### ⚙️ `/src/controllers` (Lógica de Negócio)
*   **`sensor_manager.py` (VirtualSensor)**: A inteligência do sistema. Representa um sensor físico no mundo virtual.
    *   **Lógica de Fog:** Mantém um histórico de leituras para calcular médias móveis.
    *   **Frequência Adaptativa:** Se detectar uma anomalia (ex: chuva 50% acima da média), aumenta automaticamente a frequência de coleta para prover dados mais precisos em situações críticas.
    *   **Gestão de Energia:** Simula o consumo de bateria para monitoramento de vida útil do "dispositivo".

### 🛠️ `/src/services` (Infraestrutura)
*   **`mqtt_manager.py`**: Gerencia a conexão com o Broker MQTT (HiveMQ por padrão). Converte os dados processados em JSON e publica nos tópicos correspondentes.
*   **`auth_manager.py`**: Gerencia o ciclo de vida dos tokens OAuth para a API da ANA, garantindo renovação automática antes da expiração.

### 🧰 `/src/utils`
*   **`text_utils.py`**: Funções auxiliares, como limpeza de strings e remoção de acentos para facilitar buscas e filtros.

---

## 🧠 Lógica de Fog Computing (Inteligência na Borda)

O grande diferencial do MAPI é não ser apenas um retransmissor de dados. Cada `VirtualSensor` opera com autonomia:
1.  **Monitoramento Passivo:** Coleta dados em intervalos longos (ex: 5 min) para economizar recursos.
2.  **Detecção de Eventos:** Ao identificar um aumento súbito nos índices (Anomalia), o sensor entra em "Modo Crítico".
3.  **Adaptação:** A frequência de coleta aumenta para intervalos curtos (ex: 30 seg), permitindo uma resposta mais rápida a desastres naturais como inundações.
4.  **Normalização:** Assim que os níveis estabilizam, o sensor retorna à sua frequência de operação padrão.

---

## 🚀 Como Executar

### Pré-requisitos
*   Python 3.10+
*   Pip (gerenciador de pacotes)

### Instalação
1. Clone o repositório.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure o arquivo `.env` baseado no `.env.example`:
   ```env
   ANA_IDENTIFICADOR=seu_id
   ANA_SENHA=sua_senha
   MQTT_BROKER=broker.hivemq.com
   ```

### Execução
Inicie a malha de sensores:
```bash
python src/main.py
```

---

## 📡 Tópicos MQTT
Os dados são publicados seguindo o padrão:
`projeto-mapi/sensores/[ID_DO_SENSOR]`

**Exemplo de Payload:**
```json
{
  "id_sensor": "APAC-PLUVIO-RECIFE",
  "timestamp_coleta": "2026-05-14T10:30:00",
  "status_bateria": "98.5%",
  "fog_valor_referencia": 12.5,
  "dados_originais": { ... }
}
```

---
**Desenvolvido para monitoramento inteligente e prevenção de desastres.**
