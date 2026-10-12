import random
import streamlit as st

# =====================================================================
# PERSONALIZE AQUI
# =====================================================================
NOME_DELE = "Amor"      # nome ou apelido dele
CACHORRA = "Gretha"
PRESENTE = "Seu presente de verdade está te esperando. (escreva aqui onde ele está)"
MENSAGEM_FINAL = (
    "Morar junto tem louça, indecisão e uma cachorra que ocupa a cama inteira. "
    "Mas também tem jantar no chão no meio das caixas, série no domingo e alguém "
    "pra contar o dia. Eu queria que você visse que isso pode ser bom. "
    "Feliz aniversário."
)  # troque por palavras suas, fica melhor

# =====================================================================
# CONFIGURAÇÃO E ESTILO
# =====================================================================
st.set_page_config(page_title="Nossa Casa: o Jogo", page_icon="🏡", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: #1e1e2e; }
    .stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp div[data-testid="stMarkdownContainer"] {
        color: #f2f2f2;
    }
    .stApp h1, .stApp h2, .stApp h3 { color: #ff8fa3; text-align: center; }
    .stButton > button {
        background-color: #ff6b81; color: white; border: none;
        border-radius: 10px; width: 100%; font-weight: bold; padding: .6rem;
    }
    .stButton > button:hover { background-color: #ff8fa3; color: white; }
    .stButton > button:disabled { background-color: #555; color: #aaa; opacity: .6; }
    .tab { display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; margin: 10px 0 18px 0; }
    .casa { width: 44px; height: 44px; border-radius: 10px; background: #3a3a4f;
            display: flex; align-items: center; justify-content: center; font-size: 22px; }
    .casa.feita { opacity: .4; }
    .casa.atual { background: #ff6b81; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# DADOS DO JOGO
# =====================================================================
NOMES = {
    "sintonia": "❤️ Sintonia",
    "energia": "⚡ Energia",
    "humor": f"🐶 Humor da {CACHORRA}",
}

CLASSES = {
    "🍳 Chef de Fim de Semana": {
        "desc": "Começa com mais sintonia. Cozinhar junto rende pontos.",
        "sintonia": 60, "humor": 40, "bonus_dano": 0,
    },
    f"🐶 Guardião da {CACHORRA}": {
        "desc": f"A {CACHORRA} começa de bom humor e ajuda mais nas lutas.",
        "sintonia": 50, "humor": 65, "bonus_dano": 0,
    },
    "🔧 Faz-Tudo": {
        "desc": "Bate mais forte contra a bagunça da casa.",
        "sintonia": 50, "humor": 40, "bonus_dano": 5,
    },
}

# Tabuleiro: cada casa é um tipo. As casas "evento" sorteiam uma carta.
CASAS = ["evento", "evento", "tiro", "evento", "evento", "boss", "evento", "final"]
ICONES = {"evento": "🎴", "tiro": "🎯", "boss": "🍽️", "final": "🏁"}

EVENTOS = {
    "primeira_noite": {
        "titulo": "📦 A primeira noite",
        "texto": "Tem caixa em todo canto e vocês não acham nem a panela nem o carregador. "
                 "São 22h e ninguém jantou.",
        "opcoes": [
            {"label": "Pedir pizza e comer sentados no chão",
             "efeitos": {"sintonia": 15, "energia": 10},
             "resultado": "Melhor jantar da semana, mesmo sem prato."},
            {"label": "Abrir caixa por caixa até achar a panela",
             "efeitos": {"energia": -15, "sintonia": 5},
             "resultado": "A panela estava na quinta caixa. Junto vieram as meias que você achava que tinha perdido."},
        ],
    },
    "armario": {
        "titulo": "👕 O guarda-roupa",
        "texto": "O armário tem espaço pra uma pessoa e meia. Vocês são duas.",
        "opcoes": [
            {"label": "Dividir ao meio, sem discutir",
             "efeitos": {"sintonia": 10},
             "resultado": "Ficou justo. Ninguém precisou de planilha."},
            {"label": "Argumentar que seus casacos são essenciais",
             "efeitos": {"sintonia": -10, "energia": -5},
             "resultado": "Você perdeu a discussão e ainda ganhou três cabides a menos."},
        ],
    },
    "cama": {
        "titulo": f"🛏️ {CACHORRA} na cama",
        "texto": f"A {CACHORRA} ocupa 70% da cama, bem no meio, sem nenhuma vergonha.",
        "opcoes": [
            {"label": "Dormir na pontinha",
             "efeitos": {"humor": 20, "energia": -10},
             "resultado": f"A {CACHORRA} dormiu feliz. Você acordou com torcicolo.",
             "conquista": "Inquilino da Pontinha"},
            {"label": "Mudar ela de lugar",
             "efeitos": {"humor": -10, "energia": 5},
             "resultado": "Ela voltou pro meio em dois minutos."},
        ],
    },
    "domingo": {
        "titulo": "📺 Domingo sem plano",
        "texto": "Ninguém sabe o que ver. Vem a frase: 'escolhe você'. É uma armadilha.",
        "opcoes": [
            {"label": "Escolher uma série e começar sem enrolar",
             "efeitos": {"sintonia": 15},
             "resultado": "Primeiro episódio já rodando. Decisão rápida é um tipo de carinho.",
             "conquista": "Diplomata do Controle Remoto"},
            {"label": "Rodar o menu por 45 minutos",
             "efeitos": {"sintonia": -10, "energia": -5},
             "resultado": "Vocês acabaram revendo uma série que já tinham visto."},
        ],
    },
    "sexta": {
        "titulo": "🍝 Sexta à noite",
        "texto": "Estão os dois em casa e deu fome.",
        "opcoes": [
            {"label": "Cozinhar juntos",
             "efeitos": {"sintonia": 15, "energia": -5},
             "resultado": "Ficou meio esquisito, mas comeram tudo."},
            {"label": "Pedir delivery",
             "efeitos": {"energia": 10, "sintonia": 5},
             "resultado": "Zero louça. Ninguém reclamou."},
        ],
    },
    "dia_pesado": {
        "titulo": "🛋️ Dia pesado",
        "texto": f"Você chega cansado do trabalho. Ela está no sofá com a {CACHORRA} no colo.",
        "opcoes": [
            {"label": "Sentar junto e contar como foi o dia",
             "efeitos": {"sintonia": 15, "energia": 5, "humor": 5},
             "resultado": "Chegar em casa e ter com quem falar muda bastante o dia."},
            {"label": "Dizer que está tudo bem e ir tomar banho",
             "efeitos": {"sintonia": -5, "energia": 5},
             "resultado": "Ela percebeu. Conversaram depois, e foi bom do mesmo jeito."},
        ],
    },
    "passeio": {
        "titulo": "🦮 Hora do passeio",
        "texto": f"A {CACHORRA} vê a guia na sua mão e entra em colapso de felicidade.",
        "opcoes": [
            {"label": "Passear os três juntos",
             "efeitos": {"humor": 20, "sintonia": 10, "energia": -5},
             "resultado": f"A {CACHORRA} puxou a guia o caminho todo e parou em todo poste."},
            {"label": "Levar só ela, rapidinho",
             "efeitos": {"humor": 10, "energia": -5},
             "resultado": "Passeio rápido. Ela achou pouco."},
        ],
    },
}

MOVEIS = ["🛋️", "📦", "🪴", "🧺", "🚪", "🛏️", "📺", "🧸", "🪑"]
FILEIRAS = ["de cima", "do meio", "de baixo"]


# =====================================================================
# LÓGICA
# =====================================================================
def clamp(v, lo=0, hi=100):
    return max(lo, min(hi, v))


def novo_jogo():
    s = st.session_state
    s.cena = "inicio"
    s.pos = 0
    s.sintonia = 50
    s.energia = 100
    s.humor = 40
    s.bonus_dano = 0
    s.classe = None
    s.fila = random.sample(list(EVENTOS), 5)
    s.evento = None
    s.resultado = ""
    s.delta = {}
    s.conquistas = []
    s.baloes = False
    s.tiro = {}
    s.boss = {}


def aplicar(efeitos):
    s = st.session_state
    for k, v in efeitos.items():
        s[k] = clamp(s[k] + v)


def conquista(nome):
    if nome not in st.session_state.conquistas:
        st.session_state.conquistas.append(nome)


def mostrar(texto, efeitos=None):
    s = st.session_state
    s.resultado = texto
    s.delta = efeitos or {}
    s.cena = "resultado"


def texto_delta(d):
    return " · ".join(f"{NOMES[k]} {v:+d}" for k, v in d.items() if v)


def escolher_classe(nome):
    s = st.session_state
    c = CLASSES[nome]
    s.classe = nome
    s.sintonia = c["sintonia"]
    s.humor = c["humor"]
    s.bonus_dano = c["bonus_dano"]
    s.cena = "tabuleiro"


def avancar():
    s = st.session_state
    s.pos += 1
    tipo = CASAS[s.pos - 1]
    if tipo == "evento":
        s.evento = s.fila.pop(0)
        s.cena = "evento"
    elif tipo == "tiro":
        s.tiro = {"tiros": 8, "acertos": 0, "msg": "", "alvo": random.randint(0, 8)}
        s.cena = "tiro"
    elif tipo == "boss":
        s.boss = {"hp": 80, "msg": "O Chefão da Louça surge da pia. Ele não vai sair sozinho.",
                  "gretha": 2, "dupla": 2, "ajuda": False}
        s.cena = "boss"
    else:
        s.cena = "final"


def voltar_tabuleiro():
    st.session_state.cena = "tabuleiro"


def escolher_opcao(i):
    s = st.session_state
    op = EVENTOS[s.evento]["opcoes"][i]
    aplicar(op["efeitos"])
    if op.get("conquista"):
        conquista(op["conquista"])
    mostrar(op["resultado"], op["efeitos"])


# ---------- Minigame de tiro ----------
def atirar(i):
    t = st.session_state.tiro
    t["tiros"] -= 1
    if i == t["alvo"]:
        t["acertos"] += 1
        t["msg"] = f"🎯 Acertou! A {CACHORRA} pegou o petisco no ar."
    else:
        t["msg"] = f"💨 Errou. O petisco rolou pro chão e a {CACHORRA} mudou de esconderijo."
    t["alvo"] = random.randint(0, 8)
    if t["tiros"] == 0:
        fim_tiro()


def fim_tiro():
    t = st.session_state.tiro
    a = t["acertos"]
    efeitos = {"humor": a * 7, "sintonia": 5 if a >= 4 else 0}
    aplicar(efeitos)
    if a >= 5:
        conquista("Atirador de Petisco")
    mostrar(f"Você acertou {a} de 8 petiscos. "
            f"{'A ' + CACHORRA + ' está muito bem alimentada.' if a >= 5 else 'A ' + CACHORRA + ' ainda quer mais.'}",
            efeitos)


# ---------- Batalha contra o Chefão ----------
def acao_boss(tipo):
    s = st.session_state
    b = s.boss
    dano = 0
    pula_contra = False

    if tipo == "esponja":
        dano = random.randint(8, 14) + s.bonus_dano
        msg = f"🧽 Você esfrega a pilha com a esponja ({dano} de dano)."
    elif tipo == "detergente":
        s.energia = clamp(s.energia - 10)
        dano = random.randint(18, 26) + s.bonus_dano
        msg = f"🫧 Detergente especial! ({dano} de dano, -10 de energia)."
    elif tipo == "gretha":
        b["gretha"] -= 1
        if s.humor >= 40:
            dano = random.randint(12, 18)
            pula_contra = True
            msg = (f"🐶 A {CACHORRA} late tão alto que a pilha estremece. "
                   f"O Chefão fica sem reação neste turno ({dano} de dano).")
        else:
            msg = f"🐶 A {CACHORRA} deita no tapete e te olha. Hoje ela não está num bom dia."
    else:  # dupla
        b["dupla"] -= 1
        b["ajuda"] = True
        dano = 25
        aplicar({"sintonia": 5})
        msg = "💑 Vocês lavam lado a lado. Rende mais que sozinho (25 de dano)."

    b["hp"] = max(0, b["hp"] - dano)

    if b["hp"] == 0:
        vitoria_boss()
        return

    if not pula_contra:
        d = random.randint(6, 12)
        s.energia = clamp(s.energia - d)
        msg += f" O Chefão contra-ataca com uma panela de arroz grudado (-{d} de energia)."

    if s.energia <= 0:
        s.energia = 30
        b["hp"] = max(1, b["hp"] // 2)
        b["ajuda"] = True
        aplicar({"sintonia": 10})
        msg += " Você desaba no sofá. Ela assume a pia e lava metade da pilha. Morar junto também serve pra isso."

    b["msg"] = msg


def vitoria_boss():
    s = st.session_state
    b = s.boss
    if b["ajuda"]:
        conquista("Time da Louça")
        texto = "Vocês derrotaram o Chefão da Louça juntos. A pia está vazia pela primeira vez desde a mudança."
    else:
        conquista("Rei da Louça")
        texto = "Você derrotou o Chefão da Louça sozinho. A pia está vazia pela primeira vez desde a mudança."
    efeitos = {"sintonia": 10}
    aplicar(efeitos)
    mostrar(texto, efeitos)


# =====================================================================
# TELA
# =====================================================================
if "cena" not in st.session_state:
    novo_jogo()

s = st.session_state


def painel():
    c1, c2, c3 = st.columns(3)
    c1.caption(f"{NOMES['sintonia']}: {s.sintonia}")
    c1.progress(s.sintonia / 100)
    c2.caption(f"{NOMES['energia']}: {s.energia}")
    c2.progress(s.energia / 100)
    c3.caption(f"{NOMES['humor']}: {s.humor}")
    c3.progress(s.humor / 100)


def tabuleiro():
    casas = ["🏠"] + [ICONES[c] for c in CASAS]
    html = '<div class="tab">'
    for i, c in enumerate(casas):
        cls = "casa atual" if i == s.pos else ("casa feita" if i < s.pos else "casa")
        html += f'<div class="{cls}">{"🧍" if i == s.pos else c}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


st.title("🏡 Nossa Casa: o Jogo")

if s.cena == "inicio":
    st.write(f"Feliz aniversário, {NOME_DELE}! Este jogo é um tabuleiro com cartas de situações "
             f"da nossa casa, um minigame de tiro e uma luta contra um chefão. A {CACHORRA} também joga.")
    st.write("**Escolha sua classe:**")
    for nome, c in CLASSES.items():
        st.button(nome, key=f"classe_{nome}", on_click=escolher_classe, args=(nome,))
        st.caption(c["desc"])

elif s.cena == "tabuleiro":
    painel()
    tabuleiro()
    if s.pos == 0:
        st.write("A mudança acabou de chegar. Vamos ver como é a vida aqui.")
    else:
        st.write("Casa concluída. Próxima.")
    st.button("🎲 Avançar no tabuleiro", on_click=avancar)

elif s.cena == "evento":
    painel()
    tabuleiro()
    ev = EVENTOS[s.evento]
    st.subheader(ev["titulo"])
    st.write(ev["texto"])
    for i, op in enumerate(ev["opcoes"]):
        st.button(op["label"], key=f"op_{s.evento}_{i}", on_click=escolher_opcao, args=(i,))

elif s.cena == "resultado":
    painel()
    tabuleiro()
    st.info(s.resultado)
    d = texto_delta(s.delta)
    if d:
        st.caption(d)
    st.button("Continuar ➡️", on_click=voltar_tabuleiro)

elif s.cena == "tiro":
    painel()
    tabuleiro()
    t = s.tiro
    st.subheader(f"🎯 Tiro ao Petisco")
    st.write(f"A {CACHORRA} está se escondendo atrás dos móveis e pedindo petisco. "
             f"Ouvi um latido vindo da fileira **{FILEIRAS[t['alvo'] // 3]}**. "
             f"Petiscos restantes: **{t['tiros']}** · Acertos: **{t['acertos']}**")
    if t["msg"]:
        st.caption(t["msg"])
    for linha in range(3):
        cols = st.columns(3)
        for col in range(3):
            i = linha * 3 + col
            cols[col].button(MOVEIS[i], key=f"tiro_{t['tiros']}_{i}", on_click=atirar, args=(i,))

elif s.cena == "boss":
    painel()
    tabuleiro()
    b = s.boss
    st.subheader("🍽️ Chefão da Louça")
    st.caption(f"HP do Chefão: {b['hp']}/80")
    st.progress(b["hp"] / 80)
    st.info(b["msg"])

    c1, c2 = st.columns(2)
    c1.button("🧽 Esponja", on_click=acao_boss, args=("esponja",))
    c2.button("🫧 Detergente especial (-10 energia)", on_click=acao_boss, args=("detergente",),
              disabled=s.energia <= 10)
    c3, c4 = st.columns(2)
    c3.button(f"🐶 Chamar a {CACHORRA} ({b['gretha']} usos)", on_click=acao_boss, args=("gretha",),
              disabled=b["gretha"] <= 0)
    c4.button(f"💑 Lavar em dupla ({b['dupla']} usos)", on_click=acao_boss, args=("dupla",),
              disabled=b["dupla"] <= 0 or s.sintonia < 40)
    st.caption(f"A {CACHORRA} só ajuda se o humor dela estiver em 40 ou mais. "
               "Lavar em dupla exige sintonia 40 ou mais.")

elif s.cena == "final":
    if not s.baloes:
        st.balloons()
        s.baloes = True
    tabuleiro()
    st.subheader(f"🎂 Feliz aniversário, {NOME_DELE}!")
    if s.sintonia >= 75:
        st.write(f"Resultado: casa funcionando. Sintonia {s.sintonia}%. Pouca briga, bastante jantar no chão.")
    elif s.sintonia >= 45:
        st.write(f"Resultado: casa em andamento. Sintonia {s.sintonia}%. Tem arestas, a gente ajusta junto.")
    else:
        st.write(f"Resultado: casa em obras. Sintonia {s.sintonia}%. Obra faz parte da mudança, e a louça a gente divide.")
    st.write(f"Humor final da {CACHORRA}: {s.humor}%.")
    st.success(MENSAGEM_FINAL)
    st.write(f"🎁 {PRESENTE}")
    if s.conquistas:
        st.write("**Conquistas desbloqueadas:** " + " · ".join(f"🏅 {c}" for c in s.conquistas))
    st.button("Jogar de novo 🔄", on_click=novo_jogo)
