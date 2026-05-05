# Agentes do Projeto MAPI

Este documento descreve os agentes virtuais e componentes principais do projeto MAPI (Monitoramento de Águas e Pluviometria Inteligente).

## 1. Agente Coletor APAC (APAC Collector Agent)
**Responsabilidade:** Extrair e processar dados das APIs da APAC (Agência Pernambucana de Águas e Clima).
- **Sub-agente Cemaden:** Focado em sensores de pluviometria (chuva) integrados.
- **Sub-agente Meteorologia:** Coleta dados meteorológicos completos (temperatura, umidade, vento, etc.).
- **Localização:** `src/collectors/apac_*`

## 2. Agente Coletor ANA (ANA Collector Agent)
**Responsabilidade:** Interface com o WebService da ANA (Agência Nacional de Águas).
- **Função:** Gerenciar autenticação OAUTH e buscar séries telemétricas adotadas.
- **Localização:** `src/collectors/ana_rest_collector.py`

## 3. Agente de Gerenciamento de Sensores (Sensor Manager Agent)
**Responsabilidade:** Orquestrar o ciclo de vida dos sensores virtuais.
- **Fog Logic:** Aplica inteligência na borda para detectar anomalias e ajustar a frequência de coleta dinamicamente.
- **Localização:** `src/controllers/sensor_manager.py`

## 4. Agente de Comunicação (Communication Agent)
**Responsabilidade:** Garantir a entrega dos dados processados via protocolo MQTT.
- **Localização:** `src/services/mqtt_manager.py`

## 5. Agente de Autenticação (Auth Agent)
**Responsabilidade:** Gerenciar credenciais e tokens para acesso a APIs protegidas (ANA).
- **Localização:** `src/services/auth_manager.py`
