import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import io

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Fintrack — Expense Tracker",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ---- Root Variables ---- */
:root {
    --bg: #0a0a0f;
    --surface: #13131a;
    --surface2: #1c1c28;
    --border: #2a2a3d;
    --accent: #7c6aff;
    --accent2: #ff6a9b;
    --accent3: #6affd4;
    --text: #e8e8f0;
    --muted: #6b6b85;
    --success: #4ade80;
    --warning: #fbbf24;
    --danger: #f87171;
}

/* ---- Global Reset ---- */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

.stApp {
    background: var(--bg);
}

/* ---- Hide Streamlit Branding ---- */
#MainMenu, footer, header { visibility: hidden; }

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* ---- Hero Header ---- */
.hero-header {
    background: linear-gradient(135deg, #1a1030 0%, #0d1a2e 50%, #1a0a20 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(124,106,255,0.25) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 150px; height: 150px;
    background: radial-gradient(circle, rgba(106,255,212,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, #c8b8ff 50%, #6affd4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    margin-top: 0.5rem;
    font-weight: 300;
}

/* ---- Metric Cards ---- */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.metric-card:hover { border-color: var(--accent); }
.metric-card .label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    font-weight: 500;
    margin-bottom: 0.5rem;
}
.metric-card .value {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    line-height: 1.1;
}
.metric-card .badge {
    display: inline-block;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 20px;
    margin-top: 0.4rem;
    font-weight: 500;
}
.badge-purple { background: rgba(124,106,255,0.2); color: #a99aff; }
.badge-pink   { background: rgba(255,106,155,0.2); color: #ff9ec0; }
.badge-teal   { background: rgba(106,255,212,0.2); color: #6affd4; }
.badge-yellow { background: rgba(251,191,36,0.2);  color: #fbbf24; }
.accent-bar {
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 16px 0 0 16px;
}

/* ---- Section Headers ---- */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ---- Styled Table ---- */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
}
.styled-table th {
    background: var(--surface2);
    color: var(--muted);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.75rem 1rem;
    text-align: left;
    font-weight: 500;
    border-bottom: 1px solid var(--border);
}
.styled-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid rgba(42,42,61,0.5);
    color: var(--text);
}
.styled-table tr:last-child td { border-bottom: none; }
.styled-table tr:hover td { background: rgba(124,106,255,0.05); }
.cat-chip {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 500;
}

/* ---- Budget Progress Bars ---- */
.budget-row {
    margin-bottom: 1.2rem;
}
.budget-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.4rem;
    font-size: 0.85rem;
}
.budget-bar-bg {
    background: var(--surface2);
    border-radius: 99px;
    height: 8px;
    overflow: hidden;
}
.budget-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.6s ease;
}

/* ---- Sidebar Styling ---- */
.sidebar-section {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
}
.sidebar-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin-bottom: 0.75rem;
    font-weight: 600;
}

/* ---- Streamlit Widget Overrides ---- */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #5a4de0) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.2rem !important;
    transition: opacity 0.2s !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.85 !important; }

div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stDateInput"] input,
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: white !important;
}

.stAlert {
    border-radius: 10px !important;
}

div[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== CATEGORY CONFIG ====================
CATEGORIES = {
    "🍔 Food":          {"color": "#ff6a9b", "badge": "badge-pink"},
    "🚗 Transport":     {"color": "#7c6aff", "badge": "badge-purple"},
    "🎮 Entertainment": {"color": "#6affd4", "badge": "badge-teal"},
    "💡 Utilities":     {"color": "#fbbf24", "badge": "badge-yellow"},
    "🏥 Healthcare":    {"color": "#f87171", "badge": "badge-pink"},
    "🛍️ Shopping":      {"color": "#34d399", "badge": "badge-teal"},
    "🏠 Housing":       {"color": "#60a5fa", "badge": "badge-purple"},
    "📚 Education":     {"color": "#a78bfa", "badge": "badge-purple"},
    "✈️ Travel":        {"color": "#fb923c", "badge": "badge-yellow"},
    "💼 Business":      {"color": "#94a3b8", "badge": "badge-purple"},
    "🎁 Gifts":         {"color": "#e879f9", "badge": "badge-pink"},
    "🔧 Other":         {"color": "#64748b", "badge": "badge-purple"},
}

# ==================== SESSION STATE ====================
defaults = {
    'expenses': pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description', 'Payment']),
    'budgets': {cat: 0.0 for cat in CATEGORIES},
    'currency': '₹',
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==================== HELPERS ====================
def add_expense(date, category, amount, description, payment):
    if amount <= 0:
        st.error("⚠️ Amount must be greater than 0.")
        return False
    new = pd.DataFrame([[str(date), category, amount, description, payment]],
                       columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new], ignore_index=True)
    st.session_state.expenses['Amount'] = pd.to_numeric(st.session_state.expenses['Amount'], errors='coerce')
    return True

def safe_load_csv(uploaded):
    df = pd.read_csv(uploaded)
    required = ['Date', 'Category', 'Amount', 'Description']
    if not all(c in df.columns for c in required):
        st.error(f"CSV must have columns: {', '.join(required)}")
        return None
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').astype(str)
    if 'Payment' not in df.columns:
        df['Payment'] = 'Cash'
    return df[['Date', 'Category', 'Amount', 'Description', 'Payment']]

def fmt(v):
    return f"{st.session_state.currency} {v:,.2f}"

def get_filtered(df, period='All Time'):
    if df.empty:
        return df
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    today = pd.Timestamp.today()
    if period == 'This Month':
        df = df[df['Date'].dt.month == today.month]
    elif period == 'Last 30 Days':
        df = df[df['Date'] >= today - pd.Timedelta(days=30)]
    elif period == 'Last 7 Days':
        df = df[df['Date'] >= today - pd.Timedelta(days=7)]
    elif period == 'This Year':
        df = df[df['Date'].dt.year == today.year]
    return df

def cat_color(cat):
    for k, v in CATEGORIES.items():
        if k in cat or cat in k:
            return v['color']
    return "#7c6aff"

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;
    background:linear-gradient(135deg,#fff,#c8b8ff);-webkit-background-clip:text;
    -webkit-text-fill-color:transparent;background-clip:text;margin-bottom:1.5rem;">
    💸 Fintrack
    </div>
    """, unsafe_allow_html=True)

    # --- Currency ---
    st.markdown('<div class="sidebar-label">⚙️ Settings</div>', unsafe_allow_html=True)
    currency_map = {"Indian Rupee ₹": "₹", "US Dollar $": "$", "Euro €": "€", "British Pound £": "£"}
    selected_cur = st.selectbox("Currency", list(currency_map.keys()), label_visibility="collapsed")
    st.session_state.currency = currency_map[selected_cur]

    st.divider()

    # --- Add Expense ---
    st.markdown('<div class="sidebar-label">➕ Add Expense</div>', unsafe_allow_html=True)
    with st.form("add_form", clear_on_submit=True):
        date       = st.date_input("Date", value=datetime.today())
        category   = st.selectbox("Category", list(CATEGORIES.keys()))
        amount     = st.number_input("Amount", min_value=0.0, step=10.0, format="%.2f")
        description= st.text_input("Description", placeholder="What was this for?")
        payment    = st.selectbox("Payment Mode", ["Cash", "UPI", "Credit Card", "Debit Card", "Net Banking", "Other"])
        submitted  = st.form_submit_button("Add Expense ✓")
        if submitted:
            if add_expense(date, category, amount, description, payment):
                st.success("Expense added!")

    st.divider()

    # --- Budget Manager ---
    st.markdown('<div class="sidebar-label">🎯 Monthly Budgets</div>', unsafe_allow_html=True)
    with st.expander("Set Budgets", expanded=False):
        for cat in CATEGORIES:
            st.session_state.budgets[cat] = st.number_input(
                cat, min_value=0.0, step=100.0, format="%.0f",
                value=st.session_state.budgets.get(cat, 0.0),
                key=f"budget_{cat}"
            )

    st.divider()

    # --- Upload / Download ---
    st.markdown('<div class="sidebar-label">📂 Data</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload CSV", type=['csv'])
    if uploaded:
        loaded = safe_load_csv(uploaded)
        if loaded is not None:
            merge_mode = st.radio("Mode", ["Replace", "Append"], horizontal=True)
            if st.button("Load File"):
                if merge_mode == "Replace":
                    st.session_state.expenses = loaded
                else:
                    st.session_state.expenses = pd.concat(
                        [st.session_state.expenses, loaded], ignore_index=True
                    )
                st.success("Loaded!")

    csv = st.session_state.expenses.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", data=csv, file_name='fintrack_export.csv', mime='text/csv')

    if st.button("🗑️ Clear All"):
        st.session_state.expenses = pd.DataFrame(
            columns=['Date', 'Category', 'Amount', 'Description', 'Payment'])
        st.warning("All cleared.")

# ==================== MAIN ====================

# Hero
st.markdown("""
<div class="hero-header">
    <div class="hero-title">Expense Tracker</div>
    <div class="hero-sub">Track, analyze, and control your spending — beautifully.</div>
</div>
""", unsafe_allow_html=True)

# Period filter
period = st.selectbox(
    "", ["All Time", "This Month", "Last 30 Days", "Last 7 Days", "This Year"],
    label_visibility="collapsed"
)
df = get_filtered(st.session_state.expenses.copy(), period)
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)

# ==================== METRICS ====================
total   = df['Amount'].sum()
avg_day = 0.0
txn_count = len(df)
top_cat = "—"
if not df.empty:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    days = max((df['Date'].max() - df['Date'].min()).days, 1)
    avg_day = total / days
    top_cat = df.groupby('Category')['Amount'].sum().idxmax() if txn_count > 0 else "—"

col1, col2, col3, col4 = st.columns(4)
metrics = [
    (col1, "Total Spent",     fmt(total),       "badge-purple", "#7c6aff", f"{txn_count} transactions"),
    (col2, "Avg / Day",       fmt(avg_day),     "badge-teal",   "#6affd4", "Daily burn rate"),
    (col3, "Transactions",    str(txn_count),   "badge-pink",   "#ff6a9b", period),
    (col4, "Top Category",    top_cat.split(" ", 1)[-1] if top_cat != "—" else "—",
                                                 "badge-yellow", "#fbbf24", "Highest spend"),
]
for col, label, value, badge_cls, bar_color, sub in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="accent-bar" style="background:{bar_color};"></div>
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <span class="badge {badge_cls}">{sub}</span>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== TABS ====================
tab1, tab2, tab3, tab4 = st.tabs(["📋 Transactions", "📊 Analytics", "🎯 Budgets", "📈 Trends"])

# -------- Tab 1: Transactions --------
with tab1:
    if df.empty:
        st.info("No expenses yet. Add one from the sidebar!")
    else:
        # Search & filter
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            search = st.text_input("🔍 Search", placeholder="Search descriptions...")
        with c2:
            cats = ["All"] + sorted(df['Category'].unique().tolist())
            cat_filter = st.selectbox("Category", cats)
        with c3:
            sort_by = st.selectbox("Sort", ["Date ↓", "Date ↑", "Amount ↓", "Amount ↑"])

        view = df.copy()
        if search:
            view = view[view['Description'].str.contains(search, case=False, na=False)]
        if cat_filter != "All":
            view = view[view['Category'] == cat_filter]

        sort_map = {
            "Date ↓": ("Date", False), "Date ↑": ("Date", True),
            "Amount ↓": ("Amount", False), "Amount ↑": ("Amount", True)
        }
        scol, sasc = sort_map[sort_by]
        view = view.sort_values(scol, ascending=sasc)

        # Render table
        rows_html = ""
        for _, row in view.iterrows():
            color = cat_color(str(row.get('Category', '')))
            badge_cls = next((v['badge'] for k, v in CATEGORIES.items()
                              if k in str(row.get('Category', ''))), 'badge-purple')
            rows_html += f"""
            <tr>
                <td>{str(row.get('Date',''))[:10]}</td>
                <td><span class="cat-chip {badge_cls}" style="border:1px solid {color}44;color:{color};">
                    {row.get('Category','')}</span></td>
                <td style="font-family:'Syne',sans-serif;font-weight:600;">
                    {fmt(float(row.get('Amount', 0)))}</td>
                <td style="color:var(--muted);">{row.get('Description', '—')}</td>
                <td style="color:var(--muted);font-size:0.8rem;">{row.get('Payment', '—')}</td>
            </tr>"""

        st.markdown(f"""
        <div style="background:var(--surface);border:1px solid var(--border);border-radius:16px;overflow:hidden;">
            <table class="styled-table">
                <thead><tr>
                    <th>Date</th><th>Category</th><th>Amount</th>
                    <th>Description</th><th>Payment</th>
                </tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align:right;color:var(--muted);font-size:0.8rem;margin-top:0.5rem;">
            Showing {len(view)} of {len(df)} entries
        </div>""", unsafe_allow_html=True)

# -------- Tab 2: Analytics --------
with tab2:
    if df.empty:
        st.info("Add expenses to see analytics.")
    else:
        c1, c2 = st.columns(2)

        # Donut
        with c1:
            cat_df = df.groupby('Category')['Amount'].sum().reset_index()
            colors = [cat_color(c) for c in cat_df['Category']]
            fig_donut = go.Figure(go.Pie(
                labels=cat_df['Category'],
                values=cat_df['Amount'],
                hole=0.6,
                marker=dict(colors=colors, line=dict(color='#0a0a0f', width=2)),
                textinfo='label+percent',
                textfont=dict(color='white', size=11),
            ))
            fig_donut.update_layout(
                title=dict(text="Spend by Category", font=dict(color='white', size=14, family='Syne')),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False,
                margin=dict(t=40, b=10, l=10, r=10),
                annotations=[dict(text=fmt(total), x=0.5, y=0.5, showarrow=False,
                                  font=dict(size=16, color='white', family='Syne'), xanchor='center')]
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        # Bar chart
        with c2:
            bar_df = df.groupby('Category')['Amount'].sum().sort_values(ascending=True).reset_index()
            fig_bar = go.Figure(go.Bar(
                x=bar_df['Amount'], y=bar_df['Category'],
                orientation='h',
                marker=dict(color=[cat_color(c) for c in bar_df['Category']],
                            line=dict(color='rgba(0,0,0,0)')),
                text=[fmt(v) for v in bar_df['Amount']],
                textposition='outside',
                textfont=dict(color='white', size=10),
            ))
            fig_bar.update_layout(
                title=dict(text="Category Breakdown", font=dict(color='white', size=14, family='Syne')),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showticklabels=False, color='white'),
                yaxis=dict(color='white', tickfont=dict(size=11)),
                margin=dict(t=40, b=10, l=10, r=80),
                showlegend=False,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Payment mode breakdown
        if 'Payment' in df.columns:
            pay_df = df.groupby('Payment')['Amount'].sum().reset_index()
            fig_pay = go.Figure(go.Bar(
                x=pay_df['Payment'], y=pay_df['Amount'],
                marker=dict(
                    color=['#7c6aff','#ff6a9b','#6affd4','#fbbf24','#f87171','#60a5fa'],
                    line=dict(color='rgba(0,0,0,0)')
                ),
                text=[fmt(v) for v in pay_df['Amount']],
                textposition='outside',
                textfont=dict(color='white', size=11),
            ))
            fig_pay.update_layout(
                title=dict(text="Spend by Payment Mode", font=dict(color='white', size=14, family='Syne')),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(color='white', showgrid=False),
                yaxis=dict(color='white', showgrid=False, showticklabels=False),
                margin=dict(t=40, b=10, l=10, r=10),
                showlegend=False,
            )
            st.plotly_chart(fig_pay, use_container_width=True)

# -------- Tab 3: Budgets --------
with tab3:
    st.markdown('<div class="section-title">🎯 Budget vs. Actual</div>', unsafe_allow_html=True)
    budgets_set = {k: v for k, v in st.session_state.budgets.items() if v > 0}

    if not budgets_set:
        st.info("Set budgets from the sidebar to track spending limits.")
    elif df.empty:
        st.info("No expenses to compare against budgets.")
    else:
        cat_actual = df.groupby('Category')['Amount'].sum().to_dict()

        for cat, budget in budgets_set.items():
            actual  = cat_actual.get(cat, 0)
            pct     = min((actual / budget) * 100, 100) if budget > 0 else 0
            over    = actual > budget
            color   = cat_color(cat)
            bar_clr = "#f87171" if over else color
            status  = f"⚠️ Over by {fmt(actual - budget)}" if over else f"{fmt(budget - actual)} remaining"
            st.markdown(f"""
            <div class="budget-row">
                <div class="budget-label">
                    <span style="font-weight:500;">{cat}</span>
                    <span style="color:{'#f87171' if over else 'var(--muted)'};">{status}</span>
                </div>
                <div style="display:flex;align-items:center;gap:0.75rem;">
                    <div class="budget-bar-bg" style="flex:1;">
                        <div class="budget-bar-fill" style="width:{pct}%;background:{bar_clr};"></div>
                    </div>
                    <span style="font-family:'Syne',sans-serif;font-size:0.85rem;min-width:80px;text-align:right;">
                        {fmt(actual)} / {fmt(budget)}
                    </span>
                </div>
            </div>""", unsafe_allow_html=True)

# -------- Tab 4: Trends --------
with tab4:
    if df.empty or len(df) < 2:
        st.info("Add more expenses to see trends.")
    else:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Daily trend line
        daily = df.groupby(df['Date'].dt.date)['Amount'].sum().reset_index()
        daily.columns = ['Date', 'Amount']
        daily['Cumulative'] = daily['Amount'].cumsum()

        fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
        fig_trend.add_trace(go.Bar(
            x=daily['Date'], y=daily['Amount'],
            name="Daily", marker_color='rgba(124,106,255,0.4)',
            hovertemplate='%{x}<br>Daily: ₹%{y:,.0f}<extra></extra>'
        ), secondary_y=False)
        fig_trend.add_trace(go.Scatter(
            x=daily['Date'], y=daily['Cumulative'],
            name="Cumulative", line=dict(color='#6affd4', width=2.5),
            fill='tozeroy', fillcolor='rgba(106,255,212,0.06)',
            hovertemplate='%{x}<br>Total: ₹%{y:,.0f}<extra></extra>'
        ), secondary_y=True)

        fig_trend.update_layout(
            title=dict(text="Daily & Cumulative Spending", font=dict(color='white', size=14, family='Syne')),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(color='white', showgrid=False),
            yaxis=dict(color='white', showgrid=False, title='Daily'),
            yaxis2=dict(color='#6affd4', showgrid=False, title='Cumulative'),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='white')),
            margin=dict(t=50, b=30, l=20, r=20),
            hovermode='x unified',
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # Monthly summary
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        monthly = df.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
        fig_monthly = px.bar(
            monthly, x='Month', y='Amount', color='Category',
            color_discrete_map={cat: cat_color(cat) for cat in df['Category'].unique()},
            title="Monthly Spending by Category"
        )
        fig_monthly.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font=dict(family='Syne', size=14),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            legend=dict(bgcolor='rgba(0,0,0,0)'),
            margin=dict(t=50, b=30),
        )
        st.plotly_chart(fig_monthly, use_container_width=True)











-----------------------------------------------------------------------------------------------------------
        import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------- Initialize --------------------
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=['Date', 'Category', 'Amount', 'Description']
    )

# -------------------- Functions --------------------
def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame(
        [[date, category, amount, description]],
        columns=st.session_state.expenses.columns
    )
    st.session_state.expenses = pd.concat(
        [st.session_state.expenses, new_expense],
        ignore_index=True
    )

def visualize_expenses():
    if not st.session_state.expenses.empty:
        df = st.session_state.expenses.groupby('Category')['Amount'].sum().reset_index()

        fig, ax = plt.subplots()
        sns.barplot(data=df, x='Category', y='Amount', ax=ax)
        plt.xticks(rotation=45)
        ax.set_title("Expenses by Category")
        st.pyplot(fig)
    else:
        st.warning("No expenses to visualize!")

def download_expenses():
    csv = st.session_state.expenses.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Expenses CSV",
        data=csv,
        file_name='expenses.csv',
        mime='text/csv'
    )

# -------------------- UI --------------------
st.title('💰 DevDuniya Expense Tracker')

# -------- Sidebar --------
with st.sidebar:
    st.header('➕ Add Expense')

    date = st.date_input('Date')
    category = st.selectbox(
        'Category',
        ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other']
    )
    amount = st.number_input('Amount', min_value=0.0, format="%.2f")
    description = st.text_input('Description')

    if st.button('Add Expense'):
        add_expense(date, category, amount, description)
        st.success('Expense added!')

    st.divider()

    st.header('📂 File Upload')
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

    if uploaded_file is not None:
        st.session_state.expenses = pd.read_csv(uploaded_file)
        st.success("File loaded successfully!")

    st.divider()

    st.header('💾 Save Data')
    download_expenses()

    st.divider()

    if st.button("🗑 Clear All Expenses"):
        st.session_state.expenses = pd.DataFrame(
            columns=['Date', 'Category', 'Amount', 'Description']
        )
        st.warning("All data cleared!")

# -------- Main Section --------
st.header('📋 Expenses Table')

if not st.session_state.expenses.empty:
    st.dataframe(st.session_state.expenses)

    # Total Expense
    total = st.session_state.expenses['Amount'].sum()
    st.subheader(f"💵 Total Expense: ₹ {total:.2f}")
else:
    st.info("No expenses added yet.")

# -------- Visualization --------
st.header('📊 Visualization')

if st.button('Show Visualization'):
    visualize_expenses()