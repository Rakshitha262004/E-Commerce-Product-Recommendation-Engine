# app.py
# E-Commerce Product Recommendation Engine — Streamlit Dashboard
# Author: Rakshitha A S | ACS College of Engineering | DSA Project

import streamlit as st
import json
import os
import sys

# ── Path fix so src imports work from project root ──────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import load_products, load_users
from src.recommender import get_recommendations, get_category_recommendations, get_all_scores
from src.similarity import get_similar_products
from src.report import generate_report, save_report

# ── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title="ShopSense — Recommendation Engine",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── Background ── */
.stApp {
    background: #0a0e1a;
    color: #e8eaf0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f1424 !important;
    border-right: 1px solid #1e2640;
}
[data-testid="stSidebar"] * { color: #c8ccd8 !important; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0f1e3d 0%, #162040 40%, #0d2847 100%);
    border: 1px solid #1e3a6e;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 300px; height: 150px;
    background: radial-gradient(ellipse, rgba(99,102,241,0.08) 0%, transparent 70%);
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin: 0 0 0.3rem 0;
}
.hero-subtitle {
    font-size: 0.9rem;
    color: #8892a8;
    margin: 0;
    font-weight: 300;
}
.hero-badge {
    display: inline-block;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.3);
    color: #60a5fa;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 0.8rem;
}

/* ── Metric Cards ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: #111827;
    border: 1px solid #1e2d45;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #3b5f9e; }
.metric-label {
    font-size: 0.72rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #6b7a9a;
    font-weight: 600;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #e2e8f0;
    line-height: 1;
}
.metric-sub {
    font-size: 0.75rem;
    color: #4a5a78;
    margin-top: 0.2rem;
}

/* ── Section Headers ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: -0.2px;
    margin: 0 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2640;
}
.section-icon { margin-right: 0.5rem; }

/* ── Product Recommendation Cards ── */
.rec-card {
    background: #111827;
    border: 1px solid #1e2d45;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}
.rec-card:hover {
    border-color: #3b5fa0;
    background: #141e30;
    transform: translateX(3px);
}
.rec-rank {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #1e3a6e;
    min-width: 36px;
    text-align: center;
}
.rec-rank-top { color: #f59e0b; }
.rec-info { flex: 1; }
.rec-name {
    font-weight: 600;
    font-size: 0.92rem;
    color: #e2e8f0;
    margin-bottom: 0.2rem;
}
.rec-meta {
    font-size: 0.76rem;
    color: #4a5a78;
}
.rec-price {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: #34d399;
}
.rec-score-bar {
    position: absolute;
    bottom: 0; left: 0;
    height: 2px;
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    border-radius: 0 0 0 14px;
}

/* ── Tag Pills ── */
.tag-pill {
    display: inline-block;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.2);
    color: #93c5fd;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.5px;
    padding: 2px 8px;
    border-radius: 10px;
    margin: 2px;
}

/* ── History Pills ── */
.history-item {
    display: inline-block;
    background: #1a2540;
    border: 1px solid #263655;
    color: #8892a8;
    font-size: 0.76rem;
    padding: 4px 10px;
    border-radius: 8px;
    margin: 3px;
}
.history-purchased {
    background: rgba(52,211,153,0.08);
    border-color: rgba(52,211,153,0.2);
    color: #6ee7b7;
}
.history-cart {
    background: rgba(251,191,36,0.08);
    border-color: rgba(251,191,36,0.2);
    color: #fcd34d;
}
.history-searched {
    background: rgba(139,92,246,0.08);
    border-color: rgba(139,92,246,0.2);
    color: #c4b5fd;
}

/* ── Rating Stars ── */
.stars { color: #fbbf24; font-size: 0.8rem; }

/* ── Similarity Card ── */
.sim-card {
    background: #111827;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.sim-score {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #818cf8;
}
.sim-bar-wrap {
    width: 80px;
    background: #1e2d45;
    border-radius: 4px;
    height: 5px;
    overflow: hidden;
}
.sim-bar-fill {
    height: 5px;
    background: linear-gradient(90deg, #818cf8, #a78bfa);
    border-radius: 4px;
}

/* ── Category Badge ── */
.cat-badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 6px;
    margin-right: 0.4rem;
}
.cat-Electronics { background: rgba(59,130,246,0.15); color: #93c5fd; border: 1px solid rgba(59,130,246,0.2); }
.cat-Fitness      { background: rgba(52,211,153,0.12); color: #6ee7b7; border: 1px solid rgba(52,211,153,0.2); }
.cat-Footwear     { background: rgba(251,191,36,0.12); color: #fcd34d; border: 1px solid rgba(251,191,36,0.2); }
.cat-Accessories  { background: rgba(244,114,182,0.12); color: #f9a8d4; border: 1px solid rgba(244,114,182,0.2); }
.cat-Bags         { background: rgba(251,146,60,0.12); color: #fdba74; border: 1px solid rgba(251,146,60,0.2); }

/* ── Algorithm Info Box ── */
.algo-box {
    background: #0d1829;
    border: 1px solid #1e3050;
    border-left: 3px solid #3b82f6;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    font-size: 0.82rem;
    color: #8892a8;
    line-height: 1.6;
}
.algo-box code {
    background: #1a2540;
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 0.8rem;
    color: #93c5fd;
}

/* ── Download Button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #1d4ed8, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: opacity 0.2s !important;
}
.stDownloadButton > button:hover { opacity: 0.88 !important; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] label { color: #8892a8 !important; font-size: 0.8rem !important; }

/* ── Divider ── */
hr { border-color: #1e2640 !important; margin: 1.2rem 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #1e2d45; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Load Data (cached) ───────────────────────────────────────
@st.cache_data
def load_all_data():
    base = os.path.dirname(os.path.abspath(__file__))
    product_map, category_map = load_products(os.path.join(base, "data/products.json"))
    user_map = load_users(
        os.path.join(base, "data/users.json"),
        os.path.join(base, "data/interactions.json")
    )
    return product_map, category_map, user_map

product_map, category_map, user_map = load_all_data()

# ── Helpers ─────────────────────────────────────────────────
def stars(rating):
    full = int(rating)
    return "★" * full + ("½" if rating % 1 >= 0.5 else "") + "☆" * (5 - full)

def cat_badge(category):
    cls = f"cat-{category.replace(' ', '')}"
    return f'<span class="cat-badge {cls}">{category}</span>'

def score_bar_width(score, max_score=12.0):
    return min(100, int((score / max_score) * 100))

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 0.5rem 0;">
        <div style="font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 800; color: #e2e8f0;">
            🛒 ShopSense
        </div>
        <div style="font-size: 0.75rem; color: #4a5a78; margin-top: 2px;">
            DSA Recommendation Engine
        </div>
    </div>
    <hr style="border-color: #1e2640; margin: 0.8rem 0;">
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.72rem; letter-spacing:1px; text-transform:uppercase; color:#4a5a78; font-weight:600; margin-bottom:0.5rem;">Select User</div>', unsafe_allow_html=True)

    user_options = {f"{u.name} ({uid})": uid for uid, u in user_map.items()}
    selected_label = st.selectbox("User", list(user_options.keys()), label_visibility="collapsed")
    selected_uid = user_options[selected_label]
    user = user_map[selected_uid]

    st.markdown("<hr>", unsafe_allow_html=True)

    top_n = st.slider("Top N Recommendations", min_value=3, max_value=10, value=5)

    st.markdown("<hr>", unsafe_allow_html=True)

    # DSA Info
    st.markdown("""
    <div style="font-size:0.72rem; letter-spacing:1px; text-transform:uppercase; color:#4a5a78; font-weight:600; margin-bottom:0.7rem;">DSA Concepts</div>
    """, unsafe_allow_html=True)

    dsa_concepts = [
        ("🗂️", "HashMap", "O(1) product lookup"),
        ("⚡", "Min-Heap", "Top-N extraction"),
        ("⊕", "Sets", "O(1) filter"),
        ("∩", "Jaccard", "Similarity scoring"),
        ("↕", "Sorting", "Affinity ranking"),
    ]
    for icon, name, desc in dsa_concepts:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.6rem; padding:0.4rem 0; border-bottom:1px solid #12192a;">
            <span style="font-size:0.85rem;">{icon}</span>
            <div>
                <div style="font-size:0.78rem; font-weight:600; color:#c8ccd8;">{name}</div>
                <div style="font-size:0.68rem; color:#4a5a78;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.7rem; color:#2a3650; text-align:center; padding-top:0.5rem;">
        Rakshitha A S · ACS College<br>B.E. Cybersecurity · VTU
    </div>
    """, unsafe_allow_html=True)

# ── Main Content ─────────────────────────────────────────────

# Hero Banner
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-badge">DSA Project · B.E. Cybersecurity</div>
    <div class="hero-title">🛒 E-Commerce Recommendation Engine</div>
    <div class="hero-subtitle">
        HashMap · Priority Queue · Jaccard Similarity · Sorting &nbsp;|&nbsp;
        Showing results for <strong style="color:#93c5fd;">{user.name}</strong>
        &nbsp;·&nbsp; Interests: {', '.join(user.interests)}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Compute everything ───────────────────────────────────────
recommendations    = get_recommendations(user, product_map, top_n=top_n)
category_recs      = get_category_recommendations(user, product_map, category_map, top_n=3)
all_scores         = get_all_scores(user, product_map)

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Products</div>
        <div class="metric-value">{len(product_map)}</div>
        <div class="metric-sub">in catalog</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Purchased</div>
        <div class="metric-value">{len(user.purchased)}</div>
        <div class="metric-sub">by {user.name}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">In Cart</div>
        <div class="metric-value">{len(user.cart)}</div>
        <div class="metric-sub">saved items</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Recommendations</div>
        <div class="metric-value">{top_n}</div>
        <div class="metric-sub">generated</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Main Layout: Left heavy ──────────────────────────────────
left, right = st.columns([3, 2], gap="large")

with left:
    # Top Recommendations
    st.markdown('<div class="section-header"><span class="section-icon">🎯</span>Top Recommendations</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="algo-box">
        <strong style="color:#93c5fd;">Algorithm:</strong> 
        Affinity score = Σ(Jaccard_sim × interaction_weight) + category_bonus + rating×0.5
        &nbsp;|&nbsp; Weights: <code>purchase=3</code> <code>cart=2</code> <code>search=1</code>
        &nbsp;|&nbsp; Top-N via <code>heapq</code> min-heap — O(n log k)
    </div>
    """, unsafe_allow_html=True)

    if not recommendations:
        st.info("No recommendations found. User has purchased all products!")
    else:
        max_score = max(s for _, s in recommendations) if recommendations else 1
        for i, (product, score) in enumerate(recommendations):
            rank_class = "rec-rank-top" if i == 0 else "rec-rank"
            bar_pct = int((score / max(max_score, 0.01)) * 100)
            tag_html = "".join(f'<span class="tag-pill">{t}</span>' for t in list(product.tags)[:3])
            st.markdown(f"""
            <div class="rec-card">
                <div class="{rank_class}" style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:800; min-width:32px; text-align:center;">
                    #{i+1}
                </div>
                <div class="rec-info">
                    <div class="rec-name">{product.name}</div>
                    <div class="rec-meta">
                        {cat_badge(product.category)}
                        <span class="stars">{stars(product.rating)}</span>
                        <span style="font-size:0.72rem; color:#4a5a78; margin-left:4px;">{product.rating}</span>
                        &nbsp;&nbsp;{tag_html}
                    </div>
                </div>
                <div style="text-align:right;">
                    <div class="rec-price">₹{product.price:,}</div>
                    <div style="font-size:0.7rem; color:#3b82f6; margin-top:3px;">score: {score:.3f}</div>
                </div>
                <div class="rec-score-bar" style="width:{bar_pct}%;"></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Category Recommendations
    st.markdown('<div class="section-header"><span class="section-icon">📂</span>Category-Wise Picks</div>', unsafe_allow_html=True)

    if not category_recs:
        st.info("No category recommendations available.")
    else:
        for category, recs in category_recs.items():
            with st.expander(f"  {category}  ({len(recs)} products)", expanded=True):
                if not recs:
                    st.write("All products in this category already purchased.")
                    continue
                for score, product in recs:
                    tag_html = "".join(f'<span class="tag-pill">{t}</span>' for t in list(product.tags)[:3])
                    st.markdown(f"""
                    <div class="sim-card">
                        <div>
                            <div style="font-size:0.86rem; font-weight:600; color:#e2e8f0;">{product.name}</div>
                            <div style="margin-top:3px;">{tag_html}</div>
                        </div>
                        <div style="text-align:right; min-width:90px;">
                            <div style="font-family:'Syne',sans-serif; font-weight:700; color:#34d399; font-size:0.9rem;">₹{product.price:,}</div>
                            <div style="font-size:0.7rem; color:#4a5a78;">score: {score:.3f}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

with right:
    # User Interaction History
    st.markdown('<div class="section-header"><span class="section-icon">📋</span>Interaction History</div>', unsafe_allow_html=True)

    if user.purchased:
        st.markdown('<div style="font-size:0.73rem; letter-spacing:0.8px; text-transform:uppercase; color:#4a5a78; margin-bottom:5px;">✅ Purchased</div>', unsafe_allow_html=True)
        pills = "".join(
            f'<span class="history-item history-purchased">{product_map[pid].name if pid in product_map else pid}</span>'
            for pid in user.purchased
        )
        st.markdown(f'<div style="margin-bottom:0.8rem;">{pills}</div>', unsafe_allow_html=True)

    if user.cart:
        st.markdown('<div style="font-size:0.73rem; letter-spacing:0.8px; text-transform:uppercase; color:#4a5a78; margin-bottom:5px;">🛒 In Cart</div>', unsafe_allow_html=True)
        pills = "".join(
            f'<span class="history-item history-cart">{product_map[pid].name if pid in product_map else pid}</span>'
            for pid in user.cart
        )
        st.markdown(f'<div style="margin-bottom:0.8rem;">{pills}</div>', unsafe_allow_html=True)

    if user.searched:
        st.markdown('<div style="font-size:0.73rem; letter-spacing:0.8px; text-transform:uppercase; color:#4a5a78; margin-bottom:5px;">🔍 Searched</div>', unsafe_allow_html=True)
        pills = "".join(
            f'<span class="history-item history-searched">{product_map[pid].name if pid in product_map else pid}</span>'
            for pid in user.searched
        )
        st.markdown(f'<div style="margin-bottom:0.8rem;">{pills}</div>', unsafe_allow_html=True)

    if user.ratings:
        st.markdown('<div style="font-size:0.73rem; letter-spacing:0.8px; text-transform:uppercase; color:#4a5a78; margin-bottom:5px;">⭐ Ratings Given</div>', unsafe_allow_html=True)
        for pid, rating in user.ratings.items():
            name = product_map[pid].name if pid in product_map else pid
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:4px 0; border-bottom:1px solid #12192a;">
                <span style="font-size:0.8rem; color:#c8ccd8;">{name}</span>
                <span class="stars" style="font-size:0.8rem;">{"★" * rating}{"☆" * (5-rating)}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Affinity Score Chart (using st.bar_chart)
    st.markdown('<div class="section-header"><span class="section-icon">📊</span>Affinity Score Chart</div>', unsafe_allow_html=True)

    chart_data = {
        name: score
        for name, score in all_scores.items()
        if score is not None
    }

    if chart_data:
        import pandas as pd
        df = pd.DataFrame.from_dict(chart_data, orient='index', columns=['Affinity Score'])
        df = df.sort_values('Affinity Score', ascending=False).head(8)

        # Shorten long names for display
        df.index = [n[:18] + "…" if len(n) > 18 else n for n in df.index]

        st.bar_chart(df, color="#3b82f6", height=230)
        st.markdown('<div style="font-size:0.7rem; color:#2a3650; text-align:center;">Top 8 non-purchased products by affinity</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Similar Products
    st.markdown('<div class="section-header"><span class="section-icon">🔍</span>Similar to Your Purchases</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="algo-box">
        <strong style="color:#93c5fd;">Jaccard Similarity:</strong>
        <code>|A ∩ B| / |A ∪ B|</code> on product tag sets
    </div>
    """, unsafe_allow_html=True)

    for pid in user.purchased:
        if pid not in product_map:
            continue
        target = product_map[pid]
        similar = get_similar_products(target, product_map, top_n=3)
        if not similar:
            continue

        st.markdown(f'<div style="font-size:0.78rem; font-weight:600; color:#8892a8; margin: 0.6rem 0 0.3rem 0;">Based on: <span style="color:#93c5fd;">{target.name}</span></div>', unsafe_allow_html=True)

        for sim_score, sp in similar:
            bar_w = int(sim_score * 100)
            st.markdown(f"""
            <div class="sim-card">
                <div style="flex:1;">
                    <div style="font-size:0.83rem; font-weight:600; color:#e2e8f0;">{sp.name}</div>
                    <div style="margin-top:5px;">
                        <div class="sim-bar-wrap">
                            <div class="sim-bar-fill" style="width:{bar_w}%;"></div>
                        </div>
                    </div>
                </div>
                <div class="sim-score">{sim_score:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Report Download ──────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown('<div class="section-header"><span class="section-icon">📄</span>Export Report</div>', unsafe_allow_html=True)

similar_map = {}
for pid in user.purchased:
    if pid in product_map:
        similar_map[pid] = get_similar_products(product_map[pid], product_map, top_n=3)

report = generate_report(user, recommendations, category_recs, similar_map)
report_json = json.dumps(report, indent=2, ensure_ascii=False)

dl_col, info_col = st.columns([1, 3])
with dl_col:
    st.download_button(
        label="⬇️  Download JSON Report",
        data=report_json,
        file_name=f"recommendation_report_{user.id}.json",
        mime="application/json"
    )
with info_col:
    st.markdown(f"""
    <div style="padding: 0.55rem 0; font-size:0.8rem; color:#4a5a78;">
        Report for <strong style="color:#93c5fd;">{user.name}</strong> ·
        {len(recommendations)} recommendations ·
        {len(category_recs)} categories ·
        Generated at {report['generated_at']}
    </div>
    """, unsafe_allow_html=True)
