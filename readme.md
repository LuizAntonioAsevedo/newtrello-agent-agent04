# Trello Agent (Agent04)

Este projeto implementa um **agente inteligente de gerenciamento de tarefas**, integrado ao Trello, utilizando o Google ADK (Agent Development Kit) e modelos da família Gemini.

O agente é capaz de **interagir com o usuário**, organizar tarefas automaticamente e gerenciar o fluxo de trabalho dentro de um board do Trello.

---

## Funcionalidades

O agente executa automaticamente as seguintes ações:

- Criar tarefas no Trello
- Listar tarefas (com filtro por status)
- Mover tarefas entre listas (A Fazer → Em Andamento → Concluído)
- Gerar contexto temporal (data, hora e dia da semana)
- Interagir com o usuário de forma conversacional

---

## Fluxo de Funcionamento

Ao iniciar, o agente segue um fluxo estruturado:

1. Cumprimenta o usuário com a **data atual**
2. Pergunta: *"Quais são as tarefas do dia?"*
3. Para cada tarefa informada:
   - Cria automaticamente um card no Trello
4. Pergunta se o usuário deseja:
   - Listar tarefas
   - Mover tarefas entre status
5. Executa ações sempre utilizando **tools (funções automatizadas)**

---

## Tecnologias Utilizadas

- **Python 3.10+**
- **Google ADK** (`google-adk`)
- **Modelo Gemini (LLM)**
- **Trello API** (`py-trello`)
- **dotenv** (gerenciamento de variáveis de ambiente)
- **FastAPI / Uvicorn** (via ADK Web)

---

## Configuração (.env)

Crie um arquivo `.env` dentro da pasta do agente com:

```env
GOOGLE_API_KEY= SUA_CHAVE_GOOGLE
GOOGLE_GENAI_USE_VERTEXAI=0

TRELLO_API_KEY= SUA_API_KEY
TRELLO_API_SECRET= SEU_API_SECRET
TRELLO_TOKEN= SEU_TOKEN

▶ Como Executar

1. Ativar ambiente virtual
cd agent04
.\.lab-dio\Scripts\activate
2. Instalar dependências
pip install -r requirements.txt
3. Rodar o agente
adk web

4. Acessar no navegador

http://127.0.0.1:8000

Estrutura do Board no Trello

O agente espera um board com o nome:

Agent04

E listas com nomes como:

To Do / A Fazer
Em Andamento / Doing
Concluído / Done
Tools (Funções do Agente)
get_temporal_context

Retorna data, hora e dia da semana atual.

adicionar_tarefa

Cria um card no Trello.

Parâmetros:

nome_da_task
descricao_da_task
due_date
listar_tarefas

Lista tarefas com filtro opcional:

todas
a fazer
em andamento
concluido
mover_tarefa

Move uma tarefa entre listas.

Parâmetros:

id_card
novo_status
Finalidade do Projeto

Este projeto foi desenvolvido com fins educacionais para demonstrar:

Uso de agentes inteligentes (LLM)
Integração com APIs externas (Trello)
Automação de tarefas com IA
Arquitetura baseada em tools (ações executáveis)
⚠️ Observações Importantes
O modelo Gemini pode apresentar erros como:
503 UNAVAILABLE (alta demanda)
404 model not found (modelo incompatível)

Solução: utilizar modelos compatíveis com sua API Key.

Possíveis Melhorias
Interface gráfica customizada
Integração com banco de dados
Suporte a múltiplos usuários
Logs e histórico de ações
Deploy em nuvem

Autor

Projeto desenvolvido para fins de estudo e prática com agentes inteligentes.

Luiz Antônio Asevedo
