# 🌱 Simulador de Impacto Climático na Produção Agrícola

Aplicativo interativo desenvolvido como material didático complementar para a **Aula 05 — Mudanças Climáticas e o Agronegócio**, do curso de Engenharia Agronômica do **IMESB — Instituto Municipal de Ensino Superior de Bebedouro "Victório Cardassi"**.

> **Profa. Dra. Laura Matos Ribera** · Introdução à Agronomia

---

## 🎯 O que o app faz

O simulador permite que estudantes ajustem parâmetros climáticos em tempo real e visualizem os impactos projetados sobre as principais culturas agrícolas brasileiras:

- **Aumento de temperatura** (0 a +5,8 °C)
- **Variação na precipitação** (−60% a +40%)
- **Frequência de eventos extremos** (ondas de calor, secas)
- **Concentração de CO₂** (420 a 700 ppm)

Para cada cenário, o app calcula e exibe a perda estimada de produtividade, o nível de risco, os mecanismos fisiológicos de estresse nas plantas e as estratégias de adaptação recomendadas — para **café, soja, milho, cana-de-açúcar e pecuária**.

---

## 🖥️ Como rodar localmente

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/simulador-climatico.git
cd simulador-climatico

# 2. Instale as dependências
pip install streamlit plotly pandas

# 3. Execute o app
streamlit run simulador_climatico.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

---

## 🌐 Acesso online (para os alunos)

O app está publicado no Streamlit Community Cloud e pode ser acessado diretamente pelo navegador, sem instalar nada:

**🔗 [simulador-climatico-imesb.streamlit.app](https://friw4qr893z3qncqg6b4nn.streamlit.app/)**

Funciona em celular, tablet e computador.

---

## 📦 Dependências

| Pacote | Versão mínima | Uso |
|--------|--------------|-----|
| `streamlit` | 1.28+ | Interface web interativa |
| `plotly` | 5.0+ | Gráficos de barras e gauge |
| `pandas` | 1.3+ | Manipulação dos dados das culturas |

---

## 🗂️ Estrutura do repositório

```
simulador-climatico/
│
├── simulador_climatico.py   # Código principal do app
└── README.md                # Este arquivo
```

---

## 🔬 Base científica

Os coeficientes de impacto e os limiares críticos por cultura são baseados em:

- **SEEG / Observatório do Clima** — Sistema de Estimativas de Emissões de GEE, coleção 13.0 (2025)
- **Embrapa / UNICAMP-CEPAGRI** — Modelos de vulnerabilidade climática agrícola
- **UNESP (2021)** — Previsão de produtividade com machine learning e dados agrometeorológicos
- **SciELO Brasil (2023)** — IA e sensoriamento remoto para previsão de sinistros agrícolas
- **COP30 / UNFCCC (2025)** — Pacote de Belém e metas climáticas internacionais
- **IPCC AR6** — Projeções de aquecimento global e impactos regionais
- **FAO** — Financiamento climático para sistemas agroalimentares

> Os coeficientes são simplificados para fins didáticos. Para modelagem científica, consulte os estudos originais.

---

## 🎓 Contexto pedagógico

Este simulador foi desenvolvido como parte de um conjunto de materiais complementares para a Aula 05, que inclui:

- 📄 Material complementar em Word (dados SEEG 2024, COP30, estudos de ciência de dados)
- 📊 Apresentação de slides com 11 telas temáticas
- 📋 Roteiro de estudo e preparação docente
- 💻 Este aplicativo interativo em Python

### Objetivos de aprendizagem

Ao interagir com o simulador, o estudante deve ser capaz de:

1. Compreender a relação entre parâmetros climáticos e produtividade agrícola
2. Identificar as culturas mais vulneráveis a diferentes tipos de estresse climático
3. Conectar os mecanismos fisiológicos (fechamento de estômatos, abortamento floral) com perdas de produção
4. Reconhecer o papel da ciência de dados na previsão e adaptação agrícola
5. Avaliar estratégias de adaptação para cada cultura e cenário

---

## 💡 Sugestões de uso em sala

**Atividade 1 — Exploração livre (10 min)**
Cada aluno acessa o app e ajusta os controles para simular o cenário climático da região onde mora ou trabalha.

**Atividade 2 — Debate guiado**
A professora projeta o app e propõe cenários específicos para a turma discutir:
- *"O que acontece com o café se a temperatura subir 4 °C?"*
- *"Qual cultura é mais resiliente à seca?"*
- *"Como o CO₂ elevado pode compensar parcialmente as perdas?"*

**Atividade 3 — Conexão com ciência de dados**
Mostrar o código-fonte lado a lado com o app funcionando, explicando como algoritmos como Random Forest e XGBoost fazem previsões semelhantes com dados reais.

---

## 🔄 Como atualizar o app

Se precisar modificar o simulador (adicionar uma cultura, ajustar coeficientes, etc.):

1. Edite o arquivo `simulador_climatico.py` localmente
2. Faça o upload do arquivo atualizado no GitHub (substituindo o anterior)
3. O Streamlit Community Cloud detecta a mudança automaticamente e republica em 1–2 minutos

---

## 📬 Contato

**Profa. Ma. Mariana Dias Meneses**  
 
📧 menesesmarianadias@gmail.com

---

<sub>Material desenvolvido para fins didáticos. Livre para uso e adaptação com atribuição.</sub>
