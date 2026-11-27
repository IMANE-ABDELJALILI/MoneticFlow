import time
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import streamlit as st
import warnings
warnings.filterwarnings("ignore")


st.set_page_config(
    page_title="MoneticFlow",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── DESIGN SYSTEM ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #13151f !important;
    color: #d4d8e8;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background: #1a1d2e !important;
    border-right: 1px solid #2a2d3e;
}

[data-testid="stSidebar"] * { color: #d4d8e8 !important; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }

/* ── HEADER ── */
.mf-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.6rem 2rem;
    background: #1a1d2e;
    border-radius: 12px;
    border-left: 3px solid #f07830;
    margin-bottom: 1.8rem;
}
.mf-header-left h1 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
    letter-spacing: -0.3px;
}
.mf-header-left p {
    font-size: 0.82rem;
    color: #6b7194;
    margin: 0.2rem 0 0;
    font-weight: 400;
}
.mf-badge {
    background: rgba(240,120,48,0.12);
    color: #f07830;
    border: 1px solid rgba(240,120,48,0.3);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.5px;
}

/* ── KPI CARDS ── */
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.8rem; }
.kpi-card {
    background: #1a1d2e;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: #2a2d3e;
}
.kpi-card.alert::before { background: #f07830; }
.kpi-card.warning::before { background: #e8a838; }
.kpi-card.safe::before { background: #38a878; }
.kpi-card.info::before { background: #3878e8; }
.kpi-card:hover { transform: translateY(-2px); }

.kpi-icon {
    font-size: 1.2rem;
    margin-bottom: 0.8rem;
    display: block;
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #fff;
    line-height: 1;
    margin-bottom: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
}
.kpi-card.alert .kpi-value { color: #f07830; }
.kpi-card.warning .kpi-value { color: #e8a838; }
.kpi-card.safe .kpi-value { color: #38a878; }
.kpi-label {
    font-size: 0.78rem;
    color: #6b7194;
    font-weight: 500;
    text-transform: none;
    letter-spacing: 0;
}
.kpi-delta {
    font-size: 0.75rem;
    color: #6b7194;
    margin-top: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ── SECTION HEADERS ── */
.section-header {
    font-size: 0.82rem;
    font-weight: 600;
    color: #6b7194;
    text-transform: none;
    letter-spacing: 0.3px;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #2a2d3e;
}

/* ── ALERT TABLE ── */
.fraud-row {
    display: grid;
    grid-template-columns: 2fr 1.5fr 1fr 1fr;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #1e2130;
    font-size: 0.83rem;
    align-items: center;
    transition: background 0.15s;
}
.fraud-row:hover { background: #1e2130; }
.fraud-row.header {
    font-size: 0.72rem;
    color: #6b7194;
    font-weight: 500;
    border-bottom: 1px solid #2a2d3e;
}
.fraud-score-bar {
    height: 4px;
    border-radius: 2px;
    background: #2a2d3e;
    margin-top: 4px;
}
.fraud-score-fill {
    height: 4px;
    border-radius: 2px;
    background: linear-gradient(90deg, #e8a838, #f07830);
}
.amount-mono { font-family: 'JetBrains Mono', monospace; color: #fff; }
.ts-label { color: #6b7194; font-size: 0.78rem; }

/* ── STAT CHIPS ── */
.stat-chip {
    display: inline-block;
    background: #1e2130;
    border: 1px solid #2a2d3e;
    border-radius: 6px;
    padding: 0.3rem 0.7rem;
    font-size: 0.78rem;
    color: #9aa0b8;
    margin: 0.2rem;
    font-family: 'JetBrains Mono', monospace;
}

/* Plotly container bg */
.js-plotly-plot { border-radius: 10px; overflow: hidden; }

/* Streamlit elements */
.stSlider > div { color: #d4d8e8; }
[data-testid="stSelectbox"] > div { background: #1e2130 !important; border-color: #2a2d3e !important; }
.stMultiSelect > div { background: #1e2130 !important; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ────────────────────────────────────────────────────────────────


@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/Lenovo/MoneticFlow/resultats_fraudes.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['index_num'] = range(len(df))
    return df


df_full = load_data()

# ── PLOTLY THEME ─────────────────────────────────────────────────────────────
PLOT_BG = '#1a1d2e'
PAPER_BG = '#1a1d2e'
GRID_COL = '#2a2d3e'
TEXT_COL = '#9aa0b8'
ORANGE = '#f07830'
SLATE = '#4a5068'
AMBER = '#e8a838'
GREEN = '#38a878'


def base_layout(**kwargs):
    defaults = dict(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT_COL, family='Inter, sans-serif', size=11),
        xaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL,
                   tickcolor=GRID_COL, zerolinecolor=GRID_COL),
        yaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL,
                   tickcolor=GRID_COL, zerolinecolor=GRID_COL),
        margin=dict(t=30, b=30, l=10, r=10),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT_COL)),
    )
    defaults.update(kwargs)
    return defaults


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filtres")
    st.markdown("---")

    score_range = st.slider(
        "Score de fraude",
        min_value=0.0, max_value=1.0,
        value=(0.0, 1.0), step=0.05,
        format="%.2f"
    )

    amount_max = int(df_full['amount'].max())
    amount_range = st.slider(
        "Montant (MAD)",
        min_value=0, max_value=amount_max,
        value=(0, amount_max),
        step=1000
    )

    show_only_fraud = st.checkbox("Fraudes uniquement", value=False)

    st.markdown("---")
    st.markdown("### À propos")
    st.markdown("""
    <div style='font-size:0.78rem; color:#6b7194; line-height:1.6'>
    Dataset : PaySim<br>
    Modèle : Random Forest<br>
    Pipeline : Kafka → Consumer → RF<br><br>
    <span style='color:#f07830'>MoneticFlow v1.0</span>
    </div>
    """, unsafe_allow_html=True)

# ── FILTER DATA ──────────────────────────────────────────────────────────────
df = df_full.copy()
df = df[(df['fraud_score'] >= score_range[0]) &
        (df['fraud_score'] <= score_range[1])]
df = df[(df['amount'] >= amount_range[0]) & (df['amount'] <= amount_range[1])]
if show_only_fraud:
    df = df[df['is_fraud'] == 1]

fraud_df = df[df['is_fraud'] == 1]
normal_df = df[df['is_fraud'] == 0]

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="mf-header">
    <div class="mf-header-left">
        <h1>💳 MoneticFlow</h1>
        <p>Détection de fraude monétique — {len(df):,} transactions analysées</p>
    </div>
    <div class="mf-badge">LIVE · RF MODEL</div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────────────────────
total = len(df)
n_fraud = int(df['is_fraud'].sum())
taux = round(df['is_fraud'].mean() * 100, 2) if total > 0 else 0
avg_score = round(fraud_df['fraud_score'].mean(),
                  3) if len(fraud_df) > 0 else 0
max_amount = round(fraud_df['amount'].max(), 2) if len(fraud_df) > 0 else 0

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card info">
        <span class="kpi-icon">📊</span>
        <div class="kpi-value">{total:,}</div>
        <div class="kpi-label">Transactions analysées</div>
        <div class="kpi-delta">dataset filtré</div>
    </div>
    <div class="kpi-card alert">
        <span class="kpi-icon">🚨</span>
        <div class="kpi-value">{n_fraud:,}</div>
        <div class="kpi-label">Fraudes détectées</div>
        <div class="kpi-delta">{taux}% du total</div>
    </div>
    <div class="kpi-card warning">
        <span class="kpi-icon">⚡</span>
        <div class="kpi-value">{avg_score}</div>
        <div class="kpi-label">Score moyen fraude</div>
        <div class="kpi-delta">confiance modèle</div>
    </div>
    <div class="kpi-card safe">
        <span class="kpi-icon">💰</span>
        <div class="kpi-value">{int(max_amount):,}</div>
        <div class="kpi-label">Montant max (MAD)</div>
        <div class="kpi-delta">transaction frauduleuse</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── ROW 1 : Répartition + Score distribution ─────────────────────────────────
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="section-header">Répartition des transactions</div>',
                unsafe_allow_html=True)
    fig_donut = go.Figure(go.Pie(
        values=[len(normal_df), len(fraud_df)],
        labels=['Normal', 'Fraude'],
        hole=0.6,
        marker=dict(colors=[SLATE, ORANGE]),
        textinfo='percent',
        textfont=dict(color='white', size=12),
        hovertemplate='%{label}: %{value:,}<extra></extra>'
    ))
    fig_donut.add_annotation(
        text=f"<b>{taux}%</b><br><span style='font-size:10px'>fraude</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color=ORANGE)
    )
    fig_donut.update_layout(**base_layout(height=280, showlegend=True,
                                          legend=dict(orientation='h', y=-0.1, x=0.5, xanchor='center')))
    st.plotly_chart(fig_donut, use_container_width=True,
                    config={'displayModeBar': False})

with col2:
    st.markdown('<div class="section-header">Distribution des scores de confiance</div>',
                unsafe_allow_html=True)
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=normal_df['fraud_score'], name='Normal',
        marker_color=SLATE, opacity=0.7, nbinsx=40,
        hovertemplate='Score: %{x}<br>Count: %{y}<extra>Normal</extra>'
    ))
    fig_hist.add_trace(go.Histogram(
        x=fraud_df['fraud_score'], name='Fraude',
        marker_color=ORANGE, opacity=0.85, nbinsx=40,
        hovertemplate='Score: %{x}<br>Count: %{y}<extra>Fraude</extra>'
    ))
    fig_hist.update_layout(**base_layout(
        height=280, barmode='overlay',
        xaxis_title='Score de fraude',
        yaxis_title='Nombre de transactions'
    ))
    st.plotly_chart(fig_hist, use_container_width=True,
                    config={'displayModeBar': False})

# ── ROW 2 : Timeline + Montants ──────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">Volume et fraudes dans le temps</div>',
                unsafe_allow_html=True)
    # Groupe par index binned (simuler le temps)
    df_time = df.copy()
    df_time['bin'] = pd.cut(df_time['index_num'], bins=50, labels=False)
    time_total = df_time.groupby('bin').size().reset_index(name='total')
    time_fraud = df_time[df_time['is_fraud'] == 1].groupby(
        'bin').size().reset_index(name='fraudes')
    time_merged = time_total.merge(time_fraud, on='bin', how='left').fillna(0)

    fig_time = make_subplots(specs=[[{"secondary_y": True}]])
    fig_time.add_trace(go.Bar(
        x=time_merged['bin'], y=time_merged['total'],
        name='Volume', marker_color=SLATE, opacity=0.5,
        hovertemplate='Bin %{x}<br>Volume: %{y}<extra></extra>'
    ), secondary_y=False)
    fig_time.add_trace(go.Scatter(
        x=time_merged['bin'], y=time_merged['fraudes'],
        name='Fraudes', line=dict(color=ORANGE, width=2),
        fill='tozeroy', fillcolor='rgba(240,120,48,0.15)',
        hovertemplate='Bin %{x}<br>Fraudes: %{y}<extra></extra>'
    ), secondary_y=True)
    fig_time.update_layout(**base_layout(height=280))
    fig_time.update_yaxes(gridcolor=GRID_COL, linecolor=GRID_COL,
                          tickcolor=GRID_COL, zerolinecolor=GRID_COL)
    st.plotly_chart(fig_time, use_container_width=True,
                    config={'displayModeBar': False})

with col2:
    st.markdown('<div class="section-header">Montants frauduleux</div>',
                unsafe_allow_html=True)
    fig_box = go.Figure()
    fig_box.add_trace(go.Box(
        y=fraud_df['amount'],
        name='Fraude',
        marker_color=ORANGE,
        line_color=ORANGE,
        fillcolor='rgba(240,120,48,0.15)',
        boxpoints='outliers',
        hovertemplate='Montant: %{y:,.0f} MAD<extra></extra>'
    ))
    fig_box.add_trace(go.Box(
        y=normal_df['amount'].sample(min(500, len(normal_df))),
        name='Normal',
        marker_color=SLATE,
        line_color=SLATE,
        fillcolor='rgba(74,80,104,0.15)',
        boxpoints=False,
        hovertemplate='Montant: %{y:,.0f} MAD<extra></extra>'
    ))
    fig_box.update_layout(**base_layout(height=280, showlegend=True))
    st.plotly_chart(fig_box, use_container_width=True,
                    config={'displayModeBar': False})

# ── ROW 3 : Scatter + Heatmap ────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-header">Montant vs score — transactions frauduleuses</div>',
                unsafe_allow_html=True)
    fig_scatter = px.scatter(
        fraud_df, x='index_num', y='amount',
        color='fraud_score',
        color_continuous_scale=[[0, '#c05010'], [0.5, ORANGE], [1, AMBER]],
        size_max=12,
        hover_data={'amount': ':,.0f', 'fraud_score': ':.3f'},
        labels={'index_num': 'Transaction #',
                'amount': 'Montant (MAD)', 'fraud_score': 'Score'}
    )
    fig_scatter.update_traces(marker=dict(size=7, opacity=0.8))
    fig_scatter.update_layout(**base_layout(height=280))
    fig_scatter.update_coloraxes(colorbar=dict(
        tickfont=dict(color=TEXT_COL), title=dict(font=dict(color=TEXT_COL))
    ))
    st.plotly_chart(fig_scatter, use_container_width=True,
                    config={'displayModeBar': False})

with col2:
    st.markdown('<div class="section-header">Densité des scores par type</div>',
                unsafe_allow_html=True)
    df_type = df.copy()
    df_type['type_label'] = df_type['type_encoded'].map(
        {0: 'CASH_OUT', 1: 'TRANSFER'})
    df_type['score_bin'] = pd.cut(df_type['fraud_score'],
                                  bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                                  labels=['0–0.2', '0.2–0.4', '0.4–0.6', '0.6–0.8', '0.8–1.0'])
    heatmap_data = df_type.groupby(
        ['type_label', 'score_bin']).size().reset_index(name='count')
    pivot = heatmap_data.pivot(
        index='type_label', columns='score_bin', values='count').fillna(0)

    fig_heat = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[[0, PLOT_BG], [0.3, '#3a2010'],
                    [0.7, '#c05010'], [1, ORANGE]],
        hovertemplate='Type: %{y}<br>Score: %{x}<br>Count: %{z}<extra></extra>',
        showscale=True
    ))
    fig_heat.update_layout(**base_layout(height=280))
    st.plotly_chart(fig_heat, use_container_width=True,
                    config={'displayModeBar': False})

# ── ROW 4 : Alertes récentes ─────────────────────────────────────────────────
st.markdown('<div class="section-header" style="margin-top:0.5rem">Alertes récentes — transactions suspectes</div>', unsafe_allow_html=True)

top_fraud = fraud_df.nlargest(15, 'fraud_score')[
    ['timestamp', 'amount', 'type_encoded', 'fraud_score']].copy()
top_fraud['type_label'] = top_fraud['type_encoded'].map(
    {0: 'CASH_OUT', 1: 'TRANSFER'})

fraud_html = """
<div style='background:#1a1d2e; border-radius:10px; overflow:hidden; border:1px solid #2a2d3e'>
<div class='fraud-row header'>
    <span>Horodatage</span>
    <span>Montant</span>
    <span>Type</span>
    <span>Score</span>
</div>
"""
for _, row in top_fraud.iterrows():
    score_pct = int(row['fraud_score'] * 100)
    score_color = ORANGE if row['fraud_score'] > 0.8 else AMBER
    fraud_html += f"""
<div class='fraud-row'>
    <span class='ts-label'>{row['timestamp'].strftime('%H:%M:%S') if hasattr(row['timestamp'], 'strftime') else row['timestamp']}</span>
    <span class='amount-mono'>{row['amount']:>12,.2f} MAD</span>
    <span style='color:#9aa0b8; font-size:0.78rem'>{row['type_label']}</span>
    <span>
        <span style='color:{score_color}; font-family:JetBrains Mono,monospace; font-size:0.82rem'>{row['fraud_score']:.4f}</span>
        <div class='fraud-score-bar'><div class='fraud-score-fill' style='width:{score_pct}%'></div></div>
    </span>
</div>"""

fraud_html += "</div>"
st.markdown(fraud_html, unsafe_allow_html=True)

# ── PREDICTION INTERACTIVE ───────────────────────────────────────────────────
st.markdown('<div class="section-header" style="margin-top:1.5rem">Tester une transaction</div>',
            unsafe_allow_html=True)

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        step = st.number_input("Step", min_value=1, max_value=743, value=1)
        type_encoded = st.selectbox("Type", options=[
                                    0, 1], format_func=lambda x: "CASH_OUT" if x == 0 else "TRANSFER")
        amount = st.number_input(
            "Montant (MAD)", min_value=0.0, value=10000.0, step=100.0)
        orig_account_emptied = st.selectbox("Compte émetteur vidé", options=[
                                            0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")

    with col2:
        oldbalanceOrg = st.number_input(
            "Solde initial émetteur", min_value=0.0, value=10000.0)
        newbalanceOrig = st.number_input(
            "Solde final émetteur", min_value=0.0, value=0.0)
        oldbalanceDest = st.number_input(
            "Solde initial destinataire", min_value=0.0, value=0.0)
        newbalanceDest = st.number_input(
            "Solde final destinataire", min_value=0.0, value=0.0)
        dest_was_empty = st.selectbox("Destinataire avait solde nul", options=[
                                      0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")

    with col3:
        balance_error_orig = oldbalanceOrg - newbalanceOrig - amount
        balance_error_dest = newbalanceDest - oldbalanceDest - amount
        amount_to_balance_ratio = amount / (oldbalanceOrg + 1)

        st.markdown(f"""
        <div style='background:#13151f; border-radius:8px; padding:1rem; margin-top:0.5rem'>
            <div class='kpi-label'>Features calculées</div><br>
            <div class='stat-chip'>balance_error_orig = {balance_error_orig:,.2f}</div>
            <div class='stat-chip'>balance_error_dest = {balance_error_dest:,.2f}</div>
            <div class='stat-chip'>amount_ratio = {amount_to_balance_ratio:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

    submitted = st.form_submit_button(
        "Analyser la transaction", use_container_width=True)

if submitted:
    import joblib
    import pandas as pd

    model = joblib.load("C:/Users/Lenovo/MoneticFlow/random_forest_fraud.pkl")

    features = pd.DataFrame([{
        'step': step,
        'type_encoded': type_encoded,
        'amount': amount,
        'oldbalanceOrg': oldbalanceOrg,
        'newbalanceOrig': newbalanceOrig,
        'oldbalanceDest': oldbalanceDest,
        'newbalanceDest': newbalanceDest,
        'balance_error_orig': balance_error_orig,
        'balance_error_dest': balance_error_dest,
        'orig_account_emptied': orig_account_emptied,
        'dest_was_empty': dest_was_empty,
        'amount_to_balance_ratio': amount_to_balance_ratio
    }])

    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0][1]

    if prediction == 1:
        st.markdown(f"""
        <div style='background:rgba(240,120,48,0.1); border:1px solid rgba(240,120,48,0.4);
                    border-radius:10px; padding:1.4rem 1.6rem; margin-top:1rem'>
            <div style='font-size:1.1rem; font-weight:700; color:#f07830'>🚨 FRAUDE DÉTECTÉE</div>
            <div style='color:#9aa0b8; margin-top:0.4rem; font-family:JetBrains Mono,monospace'>
                Score de confiance : {proba:.4f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background:rgba(56,168,120,0.1); border:1px solid rgba(56,168,120,0.4);
                    border-radius:10px; padding:1.4rem 1.6rem; margin-top:1rem'>
            <div style='font-size:1.1rem; font-weight:700; color:#38a878'>✅ TRANSACTION NORMALE</div>
            <div style='color:#9aa0b8; margin-top:0.4rem; font-family:JetBrains Mono,monospace'>
                Score de fraude : {proba:.4f}
            </div>
        </div>
        """, unsafe_allow_html=True)
# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-top:2rem; padding-top:1rem; border-top:1px solid #2a2d3e;
            display:flex; justify-content:space-between; align-items:center'>
    <span style='font-size:0.75rem; color:#6b7194'>MoneticFlow — Détection de fraude monétique</span>
    <span style='font-size:0.75rem; color:#6b7194; font-family:JetBrains Mono,monospace'>
        Random Forest · Kafka · Python
    </span>
</div>
""", unsafe_allow_html=True)
