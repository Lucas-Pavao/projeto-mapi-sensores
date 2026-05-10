# Projeto MAPI - Instruções de Desenvolvimento

Este arquivo contém as diretrizes fundamentais para o desenvolvimento e manutenção do projeto MAPI.

## Arquitetura e Convenções

O projeto segue uma arquitetura baseada em agentes de coleta e processamento, conforme detalhado em [AGENTS.md](AGENTS.md).

### 1. Configuração e Variáveis de Ambiente
- Todas as URLs, credenciais e parâmetros de conexão DEVEM ser configurados via arquivo `.env`.
- Utilize `os.getenv()` para acessar as configurações.
- Nunca versione o arquivo `.env` (já incluído no `.gitignore`).

### 2. Padrões de Código
- **Idioma:** Código e comentários em Português/Inglês (mantenha a consistência com o que já existe).
- **Coletores:** Devem herdar de uma classe base quando aplicável e implementar o método de extração de dados de forma robusta.
- **Tratamento de Erros:** Implementar logs claros e não interromper a execução global por falha em um único sensor (resiliência).

### 3. Lógica de Fog (Edge Computing)
- O `VirtualSensor` deve manter a lógica de adaptação de frequência baseada em anomalias.
- Valores de referência para anomalias (chuva > 0.5mm, etc.) devem ser refinados conforme a necessidade do projeto.

### 4. Integração de APIs
- **APAC:** Utiliza scraping de JSON exposto em endpoints HTML.
- **ANA:** Utiliza REST API com autenticação Bearer Token.

## Referências
- [AGENTS.md](AGENTS.md) - Descrição detalhada dos componentes do sistema.
- [README.md](README.md) - Instruções de instalação e execução.
