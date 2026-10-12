import random
import streamlit as st

# =====================================================================
# TEXTOS PRINCIPAIS (já estão prontos, edite só se quiser)
# =====================================================================
NOME_DELE = "Amor"
CACHORRA = "Gretha"
PRESENTE = "Seu presente de verdade está te esperando."
MENSAGEM_FINAL = (
    "Morar junto tem louça, indecisão e uma cachorra que ocupa a cama inteira. "
    "Mas também tem jantar no chão no meio das caixas, série no domingo e alguém "
    "pra contar o dia. Eu queria que você visse que isso pode ser bom. "
    "Feliz aniversário."
)

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
    .tab { display: flex; gap: 5px; justify-content: center; flex-wrap: wrap; margin: 10px 0 18px 0; }
    .casa { width: 38px; height: 38px; border-radius: 10px; background: #3a3a4f;
            display: flex; align-items: center; justify-content: center; font-size: 19px; }
    .casa.feita { opacity: .4; }
    .casa.atual { background: #ff6b81; }
    .stApp .cartao, .stApp .cartao p, .stApp .cartao h2 { color: #3b1f2b; text-align: center; }
    .cartao { background: linear-gradient(135deg, #ffb3c1, #ffd6a5); border-radius: 18px;
              padding: 22px 24px; margin: 14px 0; }
    .cartao h2 { margin-top: 0; }
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
    "humor": f"Humor da {CACHORRA}",
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

# Tabuleiro: as casas "evento" e "surpresa" sorteiam uma carta diferente a cada partida.
CASAS = ["evento", "evento", "surpresa", "tiro", "evento", "evento",
         "boss", "evento", "surpresa", "evento", "boss2", "final"]
ICONES = {"evento": "🎴", "surpresa": "🎁", "tiro": "🎯",
          "boss": "🍽️", "boss2": "🧺", "final": "🏁"}

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
        "texto": "O armário tem espaço pra uma pessoa e meia. Vocês são dois.",
        "opcoes": [
            {"label": "Dividir ao meio, sem discutir",
             "efeitos": {"sintonia": 10},
             "resultado": "Ficou justo. Ninguém precisou de planilha."},
            {"label": "Argumentar que seus casacos são essenciais",
             "efeitos": {"sintonia": -10, "energia": -5},
             "resultado": "Você perdeu a discussão e ficou com duas gavetas."},
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
        "titulo": "📺 Noite sem plano",
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
    "sabado": {
        "titulo": "☀️ Sábado de manhã",
        "texto": f"Ela já acordou, a {CACHORRA} também. Você ainda está debaixo do cobertor.",
        "opcoes": [
            {"label": "Levantar e fazer o café",
             "efeitos": {"sintonia": 15, "energia": -5},
             "resultado": "Café na mesa antes das dez. Recorde da casa."},
            {"label": "Fingir que está dormindo",
             "efeitos": {"energia": 10, "sintonia": -5},
             "resultado": f"A {CACHORRA} subiu na sua barriga e encerrou o fingimento."},
        ],
    },
    "mercado": {
        "titulo": "🛒 Compras do mês",
        "texto": "Vocês no mercado, com uma lista de 12 itens e um carrinho que já está cheio.",
        "opcoes": [
            {"label": "Seguir a lista à risca",
             "efeitos": {"energia": -5, "sintonia": 5},
             "resultado": "Compra eficiente. Meio sem graça, mas eficiente."},
            {"label": f"Colocar um petisco extra pra {CACHORRA} no carrinho",
             "efeitos": {"humor": 15, "sintonia": 5},
             "resultado": "A lista ficou mais cara e a Gretha mais feliz."},
        ],
    },
    "entregador": {
        "titulo": "🔔 A campainha",
        "texto": f"O entregador toca a campainha e a {CACHORRA} acha que o mundo vai acabar.",
        "opcoes": [
            {"label": "Rir da situação e pegar a encomenda",
             "efeitos": {"humor": 5, "sintonia": 5},
             "resultado": "O entregador também riu. Pacote entregue, cachorra ofendida."},
            {"label": "Tentar acalmar ela com um petisco",
             "efeitos": {"humor": 10, "energia": -5},
             "resultado": "Funcionou por uns quarenta segundos."},
        ],
    },
    "descanso": {
        "titulo": "😴 Domingo à tarde",
        "texto": "Não tem nada pra fazer e a casa está em silêncio.",
        "opcoes": [
            {"label": f"Tirar uma soneca com a {CACHORRA}",
             "efeitos": {"energia": 25, "humor": 10, "sintonia": 5},
             "resultado": "Três horas de sono. Ninguém sentiu culpa.",
             "conquista": "Soneca Oficial"},
            {"label": "Aproveitar pra arrumar a casa",
             "efeitos": {"energia": -10, "sintonia": 10},
             "resultado": "A casa ficou boa. Você ficou cansado."},
        ],
    },
    "toalha": {
        "titulo": "🧖 A toalha molhada",
        "texto": "Tem uma toalha molhada em cima da cama. Ninguém assume.",
        "opcoes": [
            {"label": "Assumir e pendurar",
             "efeitos": {"sintonia": 5},
             "resultado": "Conflito encerrado em dois segundos."},
            {"label": f"Culpar a {CACHORRA}",
             "efeitos": {"humor": -10, "sintonia": 5},
             "resultado": "Ela não tem polegares, mas foi acusada do mesmo jeito. Ninguém acreditou."},
        ],
    },
    "espaco": {
        "titulo": "📖 Cada um no seu canto",
        "texto": "Ela quer ficar um tempo sozinha com um livro e uma xícara de chá.",
        "opcoes": [
            {"label": f"Respeitar e ir brincar com a {CACHORRA}",
             "efeitos": {"sintonia": 10, "humor": 5},
             "resultado": "Uma hora de silêncio. Depois vocês se reencontraram com assunto novo."},
            {"label": "Ficar do lado fazendo perguntas",
             "efeitos": {"sintonia": -5},
             "resultado": "Ela riu, mas foram umas 30 perguntas."},
        ],
    },
}

SURPRESAS = [
    ("Você achou uma nota de R$ 20 esquecida no bolso do casaco. Vira petisco.",
     {"humor": 10, "energia": 5}),
    (f"A vizinha parou pra elogiar a {CACHORRA} no elevador. Ela fingiu que era sempre assim.",
     {"humor": 15}),
    ("Acabou a luz no prédio e vocês jantaram à luz de vela, por falta de opção.",
     {"sintonia": 10}),
    ("Ela colocou a playlist de vocês enquanto você lavava o banheiro.",
     {"sintonia": 10, "energia": 5}),
    (f"A {CACHORRA} devolveu o chinelo que mordeu semana passada. Está pior do que antes.",
     {"humor": 10}),
    ("Acabou o gás no meio do banho. Ela riu até você sair.",
     {"energia": -10, "sintonia": 5}),
]

BOSSES = {
    "boss": {
        "nome": "Chefão da Louça", "emoji": "🍽️", "hp": 80,
        "intro": "O Chefão da Louça surge da pia. Ele não vai sair sozinho.",
        "basica": ("🧽 Esponja", "🧽 Você esfrega a pilha com a esponja"),
        "forte": ("🫧 Detergente especial", "🫧 Detergente especial!"),
        "contra": "O Chefão contra-ataca com uma panela de arroz grudado",
        "gretha": "late tão alto que a pilha estremece",
        "dupla": "Vocês lavam lado a lado. Rende mais que sozinho",
        "resgate": "Você desaba no sofá. Ela assume a pia e lava metade da pilha. Morar junto também serve pra isso.",
        "vit_junto": "Vocês derrotaram o Chefão da Louça juntos. A pia está vazia pela primeira vez desde a mudança.",
        "vit_sozinho": "Você derrotou o Chefão da Louça sozinho. A pia está vazia pela primeira vez desde a mudança.",
        "conq_junto": "Time da Louça", "conq_sozinho": "Rei da Louça",
    },
    "boss2": {
        "nome": "Monstro da Roupa Suja", "emoji": "🧺", "hp": 90,
        "intro": "Você tomou um café e recuperou um pouco de energia. O cesto de roupa suja começa a se mexer.",
        "basica": ("🧺 Lavar uma leva", "🧺 Você enfia uma leva na máquina"),
        "forte": ("🧼 Sabão em pó turbo", "🧼 Sabão em pó turbo!"),
        "contra": "O Monstro lança uma meia sem par direto no seu rosto",
        "gretha": "pula dentro do cesto e espalha tudo, mas assusta o Monstro",
        "dupla": "Vocês dobram a roupa em dupla, um passa e o outro guarda",
        "resgate": "Você senta no meio da pilha de roupa. Ela pega o ferro de passar e termina junto com você.",
        "vit_junto": "Vocês derrotaram o Monstro da Roupa Suja juntos. A última meia sem par fica como troféu.",
        "vit_sozinho": "Você derrotou o Monstro da Roupa Suja sozinho. A última meia sem par fica como troféu.",
        "conq_junto": "Time da Roupa", "conq_sozinho": "Rei da Roupa",
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
    s.fila = random.sample(list(EVENTOS), 6)
    s.fila_surp = random.sample(range(len(SURPRESAS)), 2)
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
    elif tipo == "surpresa":
        texto, efeitos = SURPRESAS[s.fila_surp.pop(0)]
        aplicar(efeitos)
        mostrar("🎁 Carta surpresa: " + texto, efeitos)
    elif tipo == "tiro":
        s.tiro = {"tiros": 10, "acertos": 0, "msg": "",
                  "alvo": random.randint(0, 8), "errados": []}
        s.cena = "tiro"
    elif tipo in BOSSES:
        cfg = BOSSES[tipo]
        if tipo == "boss2":
            aplicar({"energia": 15})
        s.boss = {"id": tipo, "hp": cfg["hp"], "msg": cfg["intro"],
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
        t["msg"] = f"🎯 Acertou! A {CACHORRA} pegou o petisco no ar e foi se esconder em outro lugar."
        t["alvo"] = random.randint(0, 8)
        t["errados"] = []
    else:
        t["errados"].append(i)
        t["msg"] = f"💨 Errou. O petisco rolou pro chão. Ela continua escondida na mesma fileira."
    if t["tiros"] == 0:
        fim_tiro()


def fim_tiro():
    t = st.session_state.tiro
    a = t["acertos"]
    efeitos = {"humor": a * 6, "sintonia": 5 if a >= 4 else 0}
    aplicar(efeitos)
    if a >= 5:
        conquista("Atirador de Petisco")
        fecho = f"A {CACHORRA} está muito bem alimentada."
    else:
        fecho = f"A {CACHORRA} ainda quer mais."
    mostrar(f"Você acertou {a} de 10 petiscos. {fecho}", efeitos)


# ---------- Batalhas ----------
def acao_boss(tipo):
    s = st.session_state
    b = s.boss
    cfg = BOSSES[b["id"]]
    dano = 0
    pula_contra = False

    if tipo == "basica":
        dano = random.randint(8, 14) + s.bonus_dano
        msg = f"{cfg['basica'][1]} ({dano} de dano)."
    elif tipo == "forte":
        s.energia = clamp(s.energia - 10)
        dano = random.randint(18, 26) + s.bonus_dano
        msg = f"{cfg['forte'][1]} ({dano} de dano, -10 de energia)."
    elif tipo == "gretha":
        b["gretha"] -= 1
        if s.humor >= 40:
            dano = random.randint(12, 18)
            pula_contra = True
            msg = (f"🐶 A {CACHORRA} {cfg['gretha']}. "
                   f"O inimigo fica sem reação neste turno ({dano} de dano).")
        else:
            msg = f"🐶 A {CACHORRA} deita no tapete e te olha. Hoje ela não está num bom dia."
    else:  # dupla
        b["dupla"] -= 1
        b["ajuda"] = True
        dano = 25
        aplicar({"sintonia": 5})
        msg = f"💑 {cfg['dupla']} (25 de dano)."

    b["hp"] = max(0, b["hp"] - dano)

    if b["hp"] == 0:
        vitoria_boss()
        return

    if not pula_contra:
        d = random.randint(6, 12)
        s.energia = clamp(s.energia - d)
        msg += f" {cfg['contra']} (-{d} de energia)."

    if s.energia <= 0:
        s.energia = 30
        b["hp"] = max(1, b["hp"] // 2)
        b["ajuda"] = True
        aplicar({"sintonia": 10})
        msg += " " + cfg["resgate"]

    b["msg"] = msg


def vitoria_boss():
    s = st.session_state
    b = s.boss
    cfg = BOSSES[b["id"]]
    if b["ajuda"]:
        conquista(cfg["conq_junto"])
        texto = cfg["vit_junto"]
    else:
        conquista(cfg["conq_sozinho"])
        texto = cfg["vit_sozinho"]
    efeitos = {"sintonia": 10}
    aplicar(efeitos)
    mostrar(texto, efeitos)


# =====================================================================
# TELA
# =====================================================================
if "cena" not in st.session_state:
    novo_jogo()

s = st.session_state


def carinha():
    if s.humor >= 70:
        return "🥰"
    if s.humor >= 40:
        return "🐶"
    return "😒"


def painel():
    c1, c2, c3 = st.columns(3)
    c1.caption(f"{NOMES['sintonia']}: {s.sintonia}")
    c1.progress(s.sintonia / 100)
    c2.caption(f"{NOMES['energia']}: {s.energia}")
    c2.progress(s.energia / 100)
    c3.caption(f"{carinha()} {NOMES['humor']}: {s.humor}")
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
    st.write(f"Feliz aniversário, {NOME_DELE}! Este jogo é um tabuleiro com situações da nossa casa, "
             f"cartas surpresa, um minigame de tiro e duas lutas contra chefões. A {CACHORRA} também joga.")
    st.write("**Escolha sua classe:**")
    for nome, c in CLASSES.items():
        st.button(nome, key=f"classe_{nome}", on_click=escolher_classe, args=(nome,))
        st.caption(c["desc"])

elif s.cena == "tabuleiro":
    painel()
    tabuleiro()
    if s.pos == 0:
        st.write("A mudança acabou de chegar. Fique de olho nas três barras: elas decidem como as lutas vão ser.")
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
    st.subheader("🎯 Tiro ao Petisco")
    st.write(f"A {CACHORRA} se escondeu atrás de um móvel da fileira **{FILEIRAS[t['alvo'] // 3]}**. "
             "Se você errar, ela fica no mesmo lugar, então dá pra ir eliminando. "
             f"Petiscos restantes: **{t['tiros']}** · Acertos: **{t['acertos']}**")
    if t["msg"]:
        st.caption(t["msg"])
    for linha in range(3):
        cols = st.columns(3)
        for col in range(3):
            i = linha * 3 + col
            errado = i in t["errados"]
            cols[col].button("❌" if errado else MOVEIS[i], key=f"tiro_{t['tiros']}_{i}",
                             on_click=atirar, args=(i,), disabled=errado)

elif s.cena == "boss":
    painel()
    tabuleiro()
    b = s.boss
    cfg = BOSSES[b["id"]]
    st.subheader(f"{cfg['emoji']} {cfg['nome']}")
    st.caption(f"HP: {b['hp']}/{cfg['hp']}")
    st.progress(b["hp"] / cfg["hp"])
    st.info(b["msg"])

    c1, c2 = st.columns(2)
    c1.button(cfg["basica"][0], on_click=acao_boss, args=("basica",))
    c2.button(f"{cfg['forte'][0]} (-10 energia)", on_click=acao_boss, args=("forte",),
              disabled=s.energia <= 10)
    c3, c4 = st.columns(2)
    c3.button(f"🐶 Chamar a {CACHORRA} ({b['gretha']} usos)", on_click=acao_boss, args=("gretha",),
              disabled=b["gretha"] <= 0)
    c4.button(f"💑 Fazer em dupla ({b['dupla']} usos)", on_click=acao_boss, args=("dupla",),
              disabled=b["dupla"] <= 0 or s.sintonia < 40)
    st.caption(f"A {CACHORRA} só ajuda se o humor dela estiver em 40 ou mais. "
               "Fazer em dupla exige sintonia 40 ou mais.")

elif s.cena == "final":
    if not s.baloes:
        st.balloons()
        s.baloes = True
    tabuleiro()
    n = len(s.conquistas)
    titulo = "Morador Veterano" if n >= 5 else ("Morador Oficial" if n >= 3 else "Morador em Treinamento")
    st.markdown(
        f'<div class="cartao"><h2>🎂 Feliz aniversário, {NOME_DELE}!</h2>'
        f"<p>{MENSAGEM_FINAL}</p><p>🎁 {PRESENTE}</p></div>",
        unsafe_allow_html=True,
    )
    if s.sintonia >= 75:
        st.write(f"Resultado: casa funcionando. Sintonia {s.sintonia}%. Pouca briga, bastante jantar no chão.")
    elif s.sintonia >= 45:
        st.write(f"Resultado: casa em andamento. Sintonia {s.sintonia}%. Tem arestas, a gente ajusta junto.")
    else:
        st.write(f"Resultado: casa em obras. Sintonia {s.sintonia}%. Obra faz parte da mudança, e a louça a gente divide.")
    st.write(f"Humor final da {CACHORRA}: {s.humor}% {carinha()}")
    st.write(f"**Título conquistado:** {titulo}")
    if s.conquistas:
        st.write("**Conquistas:** " + " · ".join(f"🏅 {c}" for c in s.conquistas))
    st.button("Jogar de novo 🔄", on_click=novo_jogo)
