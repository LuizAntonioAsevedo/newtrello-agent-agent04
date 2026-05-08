import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from trello import TrelloClient
from datetime import datetime

# Carregar variáveis do .env
load_dotenv()

# Credenciais
API_SECRET = os.getenv('TRELLO_API_SECRET')
API_KEY = os.getenv('TRELLO_API_KEY')   
TOKEN = os.getenv('TRELLO_TOKEN')

# ==============================
# CONTEXTO TEMPORAL
# ==============================
def get_temporal_context():
    now = datetime.now()
    
    return {
        "data": now.strftime("%d/%m/%Y"),
        "hora": now.strftime("%H:%M"),
        "dia_semana": now.strftime("%A")
    }

# ==============================
# FORMATAR DATA
# ==============================
def formatar_data(due_date: str):
    try:
        data = datetime.strptime(due_date, "%d/%m/%Y %H:%M")
        return data.isoformat()
    except:
        return None

# ==============================
# ADICIONAR TAREFA
# ==============================
def adicionar_tarefa(nome_da_task: str, descricao_da_task: str, due_date: str):

    client = TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )

    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == "Agent04"][0]

    listas = meu_board.list_lists()

    minha_lista = [
        l for l in listas 
        if l.name.upper() in ("TO DO", "A FAZER")
    ][0]

    data_formatada = formatar_data(due_date) if due_date else None

    minha_lista.add_card(
        name=nome_da_task,
        desc=descricao_da_task,
        due=data_formatada
    )

    return f"Tarefa '{nome_da_task}' criada com sucesso no Trello!"

# ==============================
# LISTAR TAREFAS
# ==============================
def listar_tarefas(status: str = "todas"):   

    client = TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )

    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == "Agent04"][0]

    listas = meu_board.list_lists()

    status = status.lower()

    if status == "todas":
        listas_filtradas = listas

    elif status == "a fazer":
        listas_filtradas = [
            l for l in listas 
            if l.name.upper() in ("A FAZER", "TO DO", "TODO")
        ]

    elif status == "em andamento":
        listas_filtradas = [
            l for l in listas 
            if l.name.upper() in ("EM ANDAMENTO", "DOING")
        ]

    elif status in ("concluido", "concluída", "concluído"):
        listas_filtradas = [
            l for l in listas 
            if l.name.upper() in ("CONCLUIDO", "CONCLUÍDO", "DONE")
        ]

    else:
        listas_filtradas = listas

    tarefas = []

    for lista in listas_filtradas:
        cards = lista.list_cards()
        for card in cards:
            tarefas.append({
                "nome": card.name,
                "descricao": card.desc,
                "vencimento": str(card.due),
                "status": lista.name,
                "id": card.id
            })

    if not tarefas:
        return "Nenhuma tarefa encontrada."

    return tarefas

# ==============================
# MOVER TAREFA
# ==============================
def mover_tarefa(id_card: str, novo_status: str):

    client = TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )

    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == "Agent04"][0]

    listas = meu_board.list_lists()

    novo_status = novo_status.lower()

    # Definir lista destino
    if novo_status == "a fazer":
        lista_destino = [l for l in listas if l.name.upper() in ("A FAZER", "TO DO")][0]

    elif novo_status == "em andamento":
        lista_destino = [l for l in listas if l.name.upper() in ("EM ANDAMENTO", "DOING")][0]

    elif novo_status in ("concluido", "concluída", "concluído"):
        lista_destino = [l for l in listas if l.name.upper() in ("CONCLUIDO", "CONCLUÍDO", "DONE")][0]

    else:
        return "Status inválido. Use: 'a fazer', 'em andamento' ou 'concluido'."

    # Encontrar e mover card
    for lista in listas:
        for card in lista.list_cards():
            if card.id == id_card:
                card.change_list(lista_destino.id)
                return f"Tarefa movida para '{lista_destino.name}' com sucesso!"

    return "Tarefa não encontrada."

# ==============================
# AGENTE
# ==============================
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Agente de organização de tarefas.',
    instruction="""
Você é um agente de organização de tarefas integrado ao Trello.

Fluxo obrigatório:

1. Ao iniciar:
- Use get_temporal_context
- Cumprimente com a data atual
- Pergunte: Quais são as tarefas do dia?

2. Ao receber tarefas:
- Para cada tarefa:
  - Use adicionar_tarefa
  - Se não houver horário, use a data atual às 18:00

3. Após criar tarefas:
- Pergunte se deseja listar tarefas
- Se sim, use listar_tarefas

4. Para mover tarefas:
- Sempre use listar_tarefas antes
- Localize automaticamente o ID do card pelo nome da tarefa
- Depois use mover_tarefa

5. Nunca pergunte o ID manualmente ao usuário.

6. Status permitidos:
- a fazer
- em andamento
- concluido

7. Nunca execute ações sem usar tools.

Seja direto, objetivo e automatize todo o processo.
""",
    tools=[
        get_temporal_context,
        adicionar_tarefa,
        listar_tarefas,
        mover_tarefa
    ],
)