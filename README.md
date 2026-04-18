# Sistema de Monitoramento Ambiental Distribuído (projeto-mapi)

Este projeto, batizado internamente como `projeto-mapi`, é um sistema de monitoramento ambiental distribuído que simula uma arquitetura de Edge/Fog Computing. Ele foi projetado para coletar, processar e unificar dados meteorológicos e hidrológicos de múltiplas fontes em tempo real.

## Tabela de Conteúdos
- [Sobre o Projeto](#sobre-o-projeto)
- [Principais Características](#principais-características)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Começar](#como-começar)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)
- [Configuração](#configuração)
  - [Obtendo Acesso à API da ANA](#obtendo-acesso-à-api-da-ana)
- [Como Executar](#como-executar)

## Sobre o Projeto

O sistema utiliza um modelo de **Sensores Virtuais Paralelos**. Em vez de uma coleta sequencial e lenta, cada ponto de monitoramento (cidade) e cada tipo de dado (clima, chuva, nível de rio) funciona como um "nó" independente na rede, executando sua própria coleta de forma paralela.

- **Multithreading**: Utilizamos a biblioteca `threading` para que cada sensor virtual rode em paralelo. Isso garante que a lentidão ou falha em um endpoint (ex: API da APAC) não trave a coleta de dados de outras fontes (ex: ANA).
- **Separação de Responsabilidades**: O sistema é modular e dividido em:
  - **Coletores**: Drivers que sabem como se comunicar com as APIs de origem (APAC, ANA, etc.).
  - **Gerenciador de Sensores**: Controla o ciclo de vida, a formatação e a apresentação dos dados de cada sensor virtual.
  - **Orquestrador (`main.py`)**: Ponto de entrada que inicializa e gerencia a operação do sistema.

## Principais Características

- **Coletores de Dados Implementados**:
  - **APAC Meteorologia 24h**: Extrai dados de estações automáticas (umidade/temperatura do solo, radiação solar, etc.).
  - **APAC Cemaden**: Focado em pluviometria (chuva) e dados geotécnicos.
  - **ANA (Agência Nacional de Águas)**: Integração via REST para consumir dados de telemetria de bacias hidrográficas.
- **Processamento e Normalização**:
  - Funções para remover acentos e padronizar nomes de cidades (ex: "JABOATÃO" -> "JABOATAO"), garantindo o cruzamento de dados entre APIs.
  - Roteamento inteligente de formatação para exibir os dados de forma limpa e legível no console, identificando a origem.

## Estrutura do Projeto

A estrutura de diretórios e arquivos do projeto está organizada da seguinte forma:

```
projeto-mapi/
├── .env
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── collectors/
│   │   ├── __init__.py
│   │   └── ana_rest.py
│   └── services/
│       ├── __init__.py
│       └── auth_manager.py
└── tests/
    └── ...
```

## Como Começar

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

- Python 3.8 ou superior
- `pip` (gerenciador de pacotes do Python)

### Instalação

1. **Clone o repositório:**
   ```sh
   git clone <url-do-seu-repositorio>
   cd projeto-mapi
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # No Windows, use: .venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure suas credenciais (veja a seção abaixo):**
   Crie um arquivo chamado `.env` na raiz do projeto, usando o `.env.example` como modelo.

## Configuração

O sistema precisa de credenciais para acessar APIs protegidas, como a da ANA. Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

**.env.example**
```ini
# =================================================
# CREDENCIAIS PARA A AGÊNCIA NACIONAL DE ÁGUAS (ANA)
# =================================================
# O AuthManager irá ler estas variáveis para se autenticar na API da ANA
# e obter um token de acesso dinamicamente.

ANA_IDENTIFICADOR="seu_identificador_aqui"
ANA_SENHA="sua_senha_aqui"
```

### Obtendo Acesso à API da ANA

Diferente da APAC, que fornece dados abertos, a ANA exige um fluxo mais formal para acesso aos seus serviços de telemetria. O processo é o seguinte:

1.  **Solicite suas Credenciais**: O primeiro passo é solicitar o acesso. Envie um e-mail para **hidro@ana.gov.br** com o assunto `CPF ou CNPJ - Solicitação de acesso à API HidroWebService`. A equipe da ANA irá processar sua solicitação e retornar com um `identificador` e uma `senha`.

2.  **Explore a Documentação**: Enquanto aguarda, você pode consultar a documentação oficial nos portais da ANA, como o Sistema de Informações Hidrológicas (SNIRH) ou o portal de dados abertos. O coletor deste projeto está preparado para a versão REST da API.

3.  **Configure as Credenciais no Projeto**: Assim que receber suas credenciais, preencha as variáveis `ANA_IDENTIFICADOR` e `ANA_SENHA` no arquivo `.env`. O objeto `AuthManager()` cuidará do resto, usando essas credenciais para solicitar um token de acesso dinâmico e injetá-lo nas requisições.

## Como Executar

Após a instalação e configuração do arquivo `.env`, inicie o sistema com o seguinte comando:

```sh
python main.py
```

Ao ser executado, o `main.py` irá:
1.  Instanciar os drivers de conexão (Coletores).
2.  Provisionar as malhas de sensores para as cidades configuradas (atualmente, da Região Metropolitana do Recife).
3.  Iniciar o loop de coleta de cada sensor em uma thread separada.
4.  Exibir os dados filtrados e formatados no console, prontos para serem enviados futuramente para um banco de dados ou dashboard.
