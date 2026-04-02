# =============================================================================
#  Simulador de Impacto Climático na Produção Agrícola
#  Mudanças Climáticas e o Agronegócio
#  IMESB — Introdução à Agronomia
#  Profa. Ma. Mariana Dias Meneses
# =============================================================================
#
#  COMO RODAR:
#  1. Instale as dependências:
#       pip install streamlit plotly pandas
#
#  2. Execute o app:
#       streamlit run simulador_climatico.py
#
#  3. O navegador abrirá automaticamente em http://localhost:8501
#
#  PARA COMPARTILHAR COM OS ALUNOS (veja README ao final do arquivo):
#  - Opção A: Streamlit Community Cloud (gratuito, link público)
#  - Opção B: ngrok (link temporário, sem cadastro)
#  - Opção C: Google Colab (sem instalar nada)
# =============================================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import math

# ─── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Simulador Climático Agrícola",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS customizado ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 1.6rem;
        font-weight: 600;
        color: #1A5C2A;
        margin-bottom: 4px;
    }
    .subtitle {
        color: #555;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f4f9f4;
        border-left: 4px solid #27AE60;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .alert-low    { background:#EAF3DE; border-left:4px solid #639922;
                    border-radius:8px; padding:12px 16px; color:#3B6D11; }
    .alert-medium { background:#FAEEDA; border-left:4px solid #BA7517;
                    border-radius:8px; padding:12px 16px; color:#854F0B; }
    .alert-high   { background:#FCEBEB; border-left:4px solid #E24B4A;
                    border-radius:8px; padding:12px 16px; color:#A32D2D; }
    .fonte { font-size:0.75rem; color:#888; margin-top:8px; }
    .section-title { font-size:1.1rem; font-weight:600;
                     color:#1A5C2A; margin-top:1rem; margin-bottom:0.5rem; }
    .tag {
        display:inline-block; padding:2px 10px; border-radius:12px;
        font-size:0.78rem; font-weight:600; margin-left:6px;
    }
    .tag-ok  { background:#EAF3DE; color:#3B6D11; }
    .tag-med { background:#FAEEDA; color:#854F0B; }
    .tag-bad { background:#FCEBEB; color:#A32D2D; }
</style>
""", unsafe_allow_html=True)

# ─── Dados das culturas ───────────────────────────────────────────────────────
CULTURAS = {
    "☕ Café": {
        "emoji": "☕",
        "nome": "Café",
        "limite_temp": 2.0,
        "descricao": (
            "O café é uma das culturas mais sensíveis ao calor. "
            "Temperaturas acima de 30 °C durante a floração causam aborto floral "
            "e redução severa na qualidade dos grãos."
        ),
        "regioes": "SP, MG, GO, PR",
        "area_risco": {
            4.0: "95% das áreas aptas podem ser perdidas (Embrapa/UNICAMP)",
            2.0: "40–70% das áreas afetadas em cenário intermediário",
            1.0: "15–30% das áreas sob risco em cenário leve",
            0.0: "Impacto ainda controlável",
        },
        "solucoes": [
            "Sombreamento com árvores (sistemas agroflorestais)",
            "Variedades tolerantes ao calor (pesquisa Embrapa)",
            "Migração gradual para altitudes mais elevadas",
            "Irrigação de suporte durante a floração",
            "ZARC atualizado para replanejar épocas de plantio",
        ],
        "cor": "#6D4C41",
    },
    "🌱 Soja": {
        "emoji": "🌱",
        "nome": "Soja",
        "limite_temp": 3.0,
        "descricao": (
            "A soja tolera calor moderado, mas sofre com períodos de seca no "
            "enchimento dos grãos. O deslocamento das zonas produtivas para o Sul "
            "é uma tendência já observada nos dados."
        ),
        "regioes": "MT, GO, MS, PR (Matopiba em risco)",
        "area_risco": {
            3.0: "Expansão para o Sul; perdas significativas no Cerrado",
            1.5: "Deslocamento parcial das zonas produtivas",
            0.0: "Pequena redução nas áreas tropicais",
        },
        "solucoes": [
            "Plantio direto para conservar umidade do solo",
            "Fixação biológica de nitrogênio (reduz emissões de N₂O)",
            "Programa Soja de Baixo Carbono (Embrapa)",
            "Zoneamento agroclimático atualizado (ZARC)",
            "Monitoramento por satélite e machine learning",
        ],
        "cor": "#27AE60",
    },
    "🌽 Milho": {
        "emoji": "🌽",
        "nome": "Milho",
        "limite_temp": 2.5,
        "descricao": (
            "O milho é muito sensível ao calor durante o florescimento e ao déficit "
            "hídrico no enchimento de grãos. A safrinha (2ª safra) é a mais vulnerável "
            "às irregularidades climáticas do Centro-Oeste."
        ),
        "regioes": "MT, GO, MS, PR (safrinha em risco)",
        "area_risco": {
            2.5: "Safrinha do Centro-Oeste em alto risco",
            1.0: "Redução da janela de plantio seguro",
            0.0: "Risco manejável com boas práticas",
        },
        "solucoes": [
            "Escolha de híbridos tolerantes ao calor",
            "Ajuste do calendário de plantio via ZARC",
            "Irrigação de suporte na safrinha",
            "Seguro agrícola atualizado por dados climáticos",
            "Integração lavoura-pecuária-floresta (ILPF)",
        ],
        "cor": "#F39C12",
    },
    "🎋 Cana-de-açúcar": {
        "emoji": "🎋",
        "nome": "Cana-de-açúcar",
        "limite_temp": 3.5,
        "descricao": (
            "A cana adapta-se relativamente bem ao calor, mas déficits hídricos severos "
            "reduzem o teor de sacarose e a produtividade total. O ciclo fenológico "
            "se altera com temperaturas elevadas, afetando a qualidade do produto."
        ),
        "regioes": "SP, NE, MG, GO",
        "area_risco": {
            3.0: "Nordeste em risco crítico; Sudeste com perdas moderadas",
            1.5: "Alteração do ciclo e redução do teor de açúcar",
            0.0: "Impacto ainda gerenciável",
        },
        "solucoes": [
            "Irrigação eficiente por gotejamento",
            "Variedades com maior tolerância hídrica",
            "Bioenergia como geração de crédito de carbono",
            "Monitoramento fenológico por sensoriamento remoto",
            "Rotação com culturas de cobertura do solo",
        ],
        "cor": "#148F77",
    },
    "🐄 Pecuária": {
        "emoji": "🐄",
        "nome": "Pecuária",
        "limite_temp": 1.5,
        "descricao": (
            "O estresse térmico reduz o ganho de peso, a fertilidade e a produção de leite. "
            "Bovinos iniciam estresse acima de 27 °C, com queda drástica acima de 32 °C. "
            "A pecuária responde por 51% das emissões brutas do Brasil (SEEG 2025)."
        ),
        "regioes": "Norte, Nordeste, Centro-Oeste",
        "area_risco": {
            2.0: "Norte, NE e CO com estresse térmico severo",
            1.0: "Redução de 10–20% no ganho de peso médio",
            0.0: "Risco concentrado em regiões já quentes",
        },
        "solucoes": [
            "Sombreamento e bebedouros adequados nos currais",
            "Confinamento estratégico nos meses mais quentes",
            "Pastagem integrada com árvores (ILPF)",
            "Biodigestores para captura de metano dos dejetos",
            "Seleção de raças mais adaptadas ao calor (zebuínas)",
        ],
        "cor": "#D35400",
    },
}

# ─── Funções de cálculo ───────────────────────────────────────────────────────

def calcular_perda(cultura_key, temp, chuva, eventos, co2):
    """
    Calcula a perda estimada de produtividade (%) com base nos parâmetros climáticos.

    Parâmetros:
    -----------
    cultura_key : str   — nome da cultura
    temp        : float — aumento de temperatura (°C)
    chuva       : float — variação na precipitação (%)
    eventos     : float — frequência de eventos extremos por ano
    co2         : float — concentração de CO₂ (ppm)

    Retorna:
    --------
    float — perda estimada (0 a 100%)

    Lógica simplificada (baseada em estudos Embrapa/UNICAMP/CEPAGRI):
    - Cada grau de temperatura tem um peso diferente por cultura
    - Seca (precipitação negativa) amplifica a perda
    - Eventos extremos adicionam impacto adicional
    - CO₂ elevado pode ter leve efeito fertilizante (compensação parcial)
    """
    # Efeito de fertilização pelo CO₂ (leve compensação acima de 425 ppm)
    bonus_co2 = max(0, (co2 - 425) / 275) * 5  # até 5% de compensação

    # Deficit hídrico: só conta precipitação negativa
    deficit = max(0, -chuva)

    # Coeficientes por cultura (temperatura, deficit hídrico, eventos extremos)
    coeficientes = {
        "☕ Café":          (18.0, 0.40, 3.0),
        "🌱 Soja":          ( 8.0, 0.50, 2.5),
        "🌽 Milho":         (10.0, 0.45, 3.0),
        "🎋 Cana-de-açúcar":( 6.0, 0.60, 2.0),
        "🐄 Pecuária":      (12.0, 0.30, 4.0),
    }

    ct, cc, ce = coeficientes[cultura_key]
    perda_bruta = temp * ct + deficit * cc + eventos * ce
    perda_liquida = max(0.0, perda_bruta - bonus_co2)
    return round(min(100.0, perda_liquida), 1)


def classificar_risco(perda):
    """Classifica o nível de risco com base na perda estimada."""
    if perda < 10:
        return "Baixo", "🟢", "alert-low"
    elif perda < 30:
        return "Moderado", "🟡", "alert-medium"
    elif perda < 60:
        return "Alto", "🔴", "alert-high"
    else:
        return "Crítico", "🔴", "alert-high"


def get_area_risco(cultura_key, temp):
    """Retorna a descrição textual do risco por área para uma cultura e temperatura."""
    limiares = sorted(
        CULTURAS[cultura_key]["area_risco"].keys(),
        reverse=True
    )
    for limiar in limiares:
        if temp >= limiar:
            return CULTURAS[cultura_key]["area_risco"][limiar]
    return CULTURAS[cultura_key]["area_risco"][0.0]


def get_estresse_hidrico(chuva, temp):
    """Retorna a descrição dos sintomas de estresse hídrico."""
    severo = chuva < -30 or temp > 2.5
    leve   = chuva < -10 or temp > 1.0

    if not leve:
        return (
            "**Sem sinais relevantes** neste cenário.\n\n"
            "Estômatos abertos · Turgidez celular normal · "
            "Crescimento radicular sem restrição · "
            "Fotossíntese em ritmo pleno."
        )
    elif not severo:
        return (
            "**Estresse hídrico leve a moderado:**\n\n"
            "🔸 Fechamento parcial dos estômatos\n"
            "🔸 Redução da turgidez celular\n"
            "🔸 Acúmulo de ABA (ácido abscísico)\n"
            "🔸 Crescimento radicular reduzido\n"
            "🔸 Enrolamento foliar nos horários de pico"
        )
    else:
        return (
            "**Estresse hídrico severo:**\n\n"
            "🔴 Fechamento total dos estômatos\n"
            "🔴 Murchamento e senescência foliar precoce\n"
            "🔴 Forte acúmulo de ABA e espécies reativas de oxigênio (ERO)\n"
            "🔴 Abortamento floral e de frutos\n"
            "🔴 Queda severa na produtividade"
        )


def get_estresse_termico(temp, eventos):
    """Retorna a descrição dos sintomas de estresse térmico."""
    if temp < 1.0 and eventos < 2.0:
        return (
            "**Estresse térmico mínimo** neste cenário.\n\n"
            "Processos fotossintéticos e de floração dentro da "
            "faixa normal para a maioria das culturas."
        )
    elif temp < 2.5:
        return (
            "**Estresse térmico moderado:**\n\n"
            "🔸 Redução da fotossíntese líquida\n"
            "🔸 Aceleração da maturação dos grãos\n"
            "🔸 Menor tamanho e peso de grãos\n"
            "🔸 Abortamento parcial de flores nos picos de calor"
        )
    else:
        return (
            "**Estresse térmico severo:**\n\n"
            "🔴 Desnaturação de proteínas celulares acima de 38 °C\n"
            "🔴 Colapso parcial da fotossíntese\n"
            "🔴 Abortamento floral massivo\n"
            "🔴 Senescência precoce das folhas\n"
            "🔴 Redução drástica da qualidade dos produtos"
        )


def emissoes_adicionais(temp, eventos):
    """Estima emissões adicionais de GEE associadas ao cenário (MtCO₂e)."""
    return round(temp * 25 + eventos * 15)


# ─── Interface — Barra lateral ────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/"
        "Seedling_emoji_U+1F331.svg/120px-Seedling_emoji_U+1F331.svg.png",
        width=60,
    )
    st.markdown("### Simulador Climático Agrícola")
    st.markdown(
        "**IMESB · Introdução à Agronomia**  \n"
        "Aula 05 — Mudanças Climáticas"
    )
    st.divider()

    st.markdown("#### ⚙️ Parâmetros climáticos")

    temp = st.slider(
        "🌡️ Aumento de temperatura (°C)",
        min_value=0.0, max_value=5.8, value=1.5, step=0.1,
        help="Aumento em relação à média histórica 1850–1900. "
             "Acordo de Paris: meta de 1,5 °C. Projeções pessimistas: 4–5 °C."
    )

    chuva = st.slider(
        "🌧️ Variação na precipitação (%)",
        min_value=-60, max_value=40, value=-15, step=1,
        help="Negativo = seca (déficit hídrico). Positivo = excesso de chuva. "
             "A seca de 2024 foi a pior em 75 anos no Brasil."
    )

    eventos = st.slider(
        "⚡ Frequência de eventos extremos (por ano)",
        min_value=1.0, max_value=5.0, value=2.0, step=0.5,
        help="Ondas de calor, secas severas, chuvas intensas. "
             "Atualmente ~2x/ano; projeções indicam até 5x até 2100."
    )

    co2 = st.slider(
        "💨 Concentração de CO₂ (ppm)",
        min_value=420, max_value=700, value=425, step=5,
        help="Nível atual: ~425 ppm. Pré-industrial: 280 ppm. "
             "Cenário pessimista 2100: 700–1000 ppm. "
             "CO₂ elevado tem leve efeito fertilizante em algumas culturas."
    )

    st.divider()
    cultura_sel = st.selectbox(
        "🌿 Selecione a cultura:",
        list(CULTURAS.keys()),
    )

    st.divider()
    st.markdown(
        '<p class="fonte">Baseado em: SEEG 2024 (Observatório do Clima), '
        'modelos UNICAMP/CEPAGRI, Embrapa, estudos UNESP e SciELO Brasil.</p>',
        unsafe_allow_html=True
    )

# ─── Cálculos para exibição ───────────────────────────────────────────────────
perdas = {k: calcular_perda(k, temp, chuva, eventos, co2) for k in CULTURAS}
perda_sel  = perdas[cultura_sel]
perda_media = round(sum(perdas.values()) / len(perdas), 1)
risco_label, risco_emoji, risco_css = classificar_risco(perda_sel)
risco_geral, _, _ = classificar_risco(perda_media)
emis_add = emissoes_adicionais(temp, eventos)

# ─── Cabeçalho ────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="main-title">🌍 Simulador de Impacto Climático na Produção Agrícola</div>'
    '<div class="subtitle">Aula 05 — Mudanças Climáticas e o Agronegócio · IMESB · '
    'Profa. Dra. Laura Matos Ribera</div>',
    unsafe_allow_html=True
)

# ─── Métricas gerais ──────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🌡️ Aquecimento simulado",
        value=f"+{temp:.1f} °C",
        delta="Meta Paris: 1.5 °C" if temp <= 1.5 else f"{temp-1.5:.1f} °C acima da meta",
        delta_color="normal" if temp <= 1.5 else "inverse",
    )

with col2:
    st.metric(
        label="📉 Perda média nas culturas",
        value=f"{perda_media:.0f}%",
        delta=f"Risco {risco_geral}",
        delta_color="inverse" if perda_media > 15 else "normal",
    )

with col3:
    hidrico = ("Normal" if chuva > -10
               else "Leve" if chuva > -30
               else "Severo" if chuva > -50
               else "Extremo")
    st.metric(
        label="💧 Estresse hídrico",
        value=hidrico,
        delta=f"{chuva:+d}% precipitação",
        delta_color="inverse" if chuva < -10 else "normal",
    )

with col4:
    st.metric(
        label="🏭 Emissões adicionais est.",
        value=f"+{emis_add} MtCO₂e",
        delta="vs. cenário atual",
        delta_color="inverse",
    )

st.divider()

# ─── Gráfico comparativo ──────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title">📊 Perda de produtividade estimada por cultura</div>',
    unsafe_allow_html=True
)

df_perdas = pd.DataFrame({
    "Cultura": [CULTURAS[k]["nome"] for k in CULTURAS],
    "Perda (%)": [perdas[k] for k in CULTURAS],
    "Cor": [CULTURAS[k]["cor"] for k in CULTURAS],
})

fig_bar = go.Figure(go.Bar(
    x=df_perdas["Perda (%)"],
    y=df_perdas["Cultura"],
    orientation="h",
    marker_color=df_perdas["Cor"],
    text=[f"{v:.0f}%" for v in df_perdas["Perda (%)"]],
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Perda estimada: %{x:.1f}%<extra></extra>",
))

fig_bar.update_layout(
    height=260,
    margin=dict(l=10, r=70, t=10, b=40),
    xaxis=dict(
        range=[0, 105],
        showgrid=True,
        gridcolor="#e0e0e0",
        ticksuffix="%",
        tickfont=dict(size=14, color="#333333"),
        title="Perda estimada de produtividade (%)",
        title_font=dict(size=14, color="#333333"),
    ),
    yaxis=dict(
        autorange="reversed",
        tickfont=dict(size=15, color="#1A5C2A", family="Arial"),
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14, color="#333333", family="Arial"),
)

st.plotly_chart(fig_bar, use_container_width=True)

# ─── Análise da cultura selecionada ───────────────────────────────────────────
st.divider()
st.markdown(
    f'<div class="section-title">'
    f'{CULTURAS[cultura_sel]["emoji"]} Análise detalhada — {CULTURAS[cultura_sel]["nome"]}'
    f'</div>',
    unsafe_allow_html=True
)

col_a, col_b = st.columns([1.2, 1])

with col_a:
    # Descrição e alerta
    st.markdown(f"**Sobre a cultura:** {CULTURAS[cultura_sel]['descricao']}")
    st.markdown(f"**Regiões em risco:** {CULTURAS[cultura_sel]['regioes']}")

    # Indicador de limiar
    limiar = CULTURAS[cultura_sel]["limite_temp"]
    acima  = temp >= limiar
    st.markdown(
        f"**Limiar crítico de temperatura:** +{limiar} °C — "
        f"{'⚠️ **ATINGIDO** neste cenário' if acima else '✅ ainda não atingido'}"
    )

    # Projeção de área em risco
    area_txt = get_area_risco(cultura_sel, temp)
    st.markdown(f"**Projeção de área afetada:** {area_txt}")

    # Alerta contextual
    if perda_sel < 10:
        msg = (f"Impacto mínimo neste cenário. "
               f"Com +{temp:.1f} °C, a {CULTURAS[cultura_sel]['nome']} "
               f"ainda opera abaixo do limiar crítico.")
    elif perda_sel < 30:
        msg = (f"Impacto moderado: perda estimada de {perda_sel:.0f}% na produtividade. "
               f"Medidas preventivas já são recomendadas para {CULTURAS[cultura_sel]['regioes']}.")
    elif perda_sel < 60:
        msg = (f"Alerta: com +{temp:.1f} °C e {chuva:+d}% de precipitação, "
               f"a {CULTURAS[cultura_sel]['nome']} pode perder {perda_sel:.0f}% de produtividade. "
               f"{area_txt}.")
    else:
        msg = (f"Situação crítica: perda projetada de {perda_sel:.0f}% na "
               f"{CULTURAS[cultura_sel]['nome']}. "
               f"{area_txt}. Adaptação urgente é necessária.")

    st.markdown(
        f'<div class="{risco_css}">{risco_emoji} <strong>Risco {risco_label}:</strong> {msg}</div>',
        unsafe_allow_html=True
    )

with col_b:
    # Gráfico de gauge
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=perda_sel,
        delta={"reference": 0, "suffix": "%", "valueformat": ".0f"},
        title={"text": f"Perda estimada<br>{CULTURAS[cultura_sel]['nome']}", "font": {"size": 14}},
        number={"suffix": "%", "font": {"size": 32}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#888"},
            "bar":  {"color": CULTURAS[cultura_sel]["cor"]},
            "steps": [
                {"range": [0,  10], "color": "#EAF3DE"},
                {"range": [10, 30], "color": "#FAEEDA"},
                {"range": [30, 60], "color": "#FCEBEB"},
                {"range": [60,100], "color": "#F7C1C1"},
            ],
            "threshold": {
                "line": {"color": "#A32D2D", "width": 3},
                "thickness": 0.75,
                "value": perda_sel,
            },
        },
    ))
    fig_gauge.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

# ─── Mecanismos fisiológicos ──────────────────────────────────────────────────
st.divider()
st.markdown(
    '<div class="section-title">🔬 Como o estresse climático afeta as plantas</div>',
    unsafe_allow_html=True
)

col_h, col_t = st.columns(2)

with col_h:
    st.markdown("**Estresse hídrico (déficit de água)**")
    st.markdown(get_estresse_hidrico(chuva, temp))

with col_t:
    st.markdown("**Estresse térmico (excesso de calor)**")
    st.markdown(get_estresse_termico(temp, eventos))

# ─── Soluções e adaptação ────────────────────────────────────────────────────
st.divider()
st.markdown(
    f'<div class="section-title">💡 Estratégias de adaptação — '
    f'{CULTURAS[cultura_sel]["nome"]}</div>',
    unsafe_allow_html=True
)

solucoes = CULTURAS[cultura_sel]["solucoes"]
cols_sol = st.columns(len(solucoes))

for i, (col, sol) in enumerate(zip(cols_sol, solucoes), 1):
    with col:
        st.markdown(
            f'<div class="metric-card">'
            f'<div style="font-size:0.8rem;color:#888;margin-bottom:4px">#{i}</div>'
            f'<div style="font-size:0.88rem;font-weight:500;color:#1A5C2A">{sol}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

# ─── Conexão com ciência de dados ────────────────────────────────────────────
st.divider()
st.markdown(
    '<div class="section-title">🤖 Como a ciência de dados ajuda neste cenário</div>',
    unsafe_allow_html=True
)

col_cd1, col_cd2, col_cd3 = st.columns(3)

with col_cd1:
    st.info(
        "**Random Forest & XGBoost**  \n"
        "Algoritmos de machine learning que preveem a produtividade com meses "
        "de antecedência usando dados climáticos históricos. "
        "Erro 25–30% menor que modelos tradicionais. (Fonte: UNESP, 2021)"
    )

with col_cd2:
    st.info(
        "**Sensoriamento remoto (satélite)**  \n"
        "Imagens NDVI identificam lavouras em estresse antes da perda ser visível. "
        "IA combinada com satélite prevê sinistros agrícolas e subsidia "
        "o seguro rural. (Fonte: SciELO, 2023)"
    )

with col_cd3:
    st.info(
        "**ZARC — Zoneamento de Risco Climático**  \n"
        "Modelos estatísticos que indicam onde e quando plantar com menor risco. "
        "Atualizado com dados do SEEG e modelos de projeção climática do IPCC."
    )

# ─── Rodapé ───────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    '<p class="fonte">'
    'Fontes: SEEG / Observatório do Clima (2025) · Embrapa · '
    'UNICAMP/CEPAGRI · UNESP (2021) · SciELO Brasil (2023) · '
    'COP30 / UNFCCC (2025) · FAO · IPCC AR6 · '
    'Os coeficientes de impacto são simplificados para fins didáticos. '
    'Para modelagem científica, consulte os estudos originais.'
    '</p>',
    unsafe_allow_html=True
)

# =============================================================================
#  README — COMO COMPARTILHAR COM OS ALUNOS
# =============================================================================
#
#  OPÇÃO A — Streamlit Community Cloud (RECOMENDADO, gratuito, permanente)
#  -----------------------------------------------------------------------
#  1. Crie uma conta gratuita em: https://streamlit.io/cloud
#  2. Suba este arquivo para um repositório GitHub
#  3. Clique em "New app" → conecte o repositório → Deploy
#  4. O app recebe um link público permanente tipo:
#     https://seunome-simulador-climatico.streamlit.app
#  5. Compartilhe o link com os alunos via WhatsApp, Moodle ou e-mail
#  Tempo estimado: 10–15 minutos na primeira vez

