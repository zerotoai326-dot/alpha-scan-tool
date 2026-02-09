import streamlit as st
import pandas as pd
import requests

# --- הגדרות דף ---
st.set_page_config(page_title="AlphaScan AI | Solana Whale Hunter", layout="wide", page_icon="⚡")

# עיצוב פינטק מתקדם
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: #e9eaeb; }
    .stButton>button { width: 100%; border-radius: 8px; background: linear-gradient(90deg, #00ffbd, #00d4ff); color: black; font-weight: bold; border: none; }
    .token-row { border-bottom: 1px solid #30363d; padding: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- כותרת ראשית ---
st.title("⚡ AlphaScan AI: Solana Hunter")
st.write("סורק בזמן אמת מטבעות עם זינוק בנפח המסחר (ווליום)")

# --- תפריט צד ---
with st.sidebar:
    st.image("https://cryptologos.cc/logos/solana-sol-logo.png", width=50)
    st.header("💎 פלטפורמות מומלצות")
    st.markdown("### 🤖 מסחר מהיר")
    # קישור השותפים שלך ל-Maestro
    st.markdown("[🚀 Trade via Maestro (Referral)](https://t.me/MaestroSniperBot?start=67bcf12a)")
    st.write("---")
    st.caption("הכלי סורק מטבעות עם ווליום מעל $50k ונזילות מעל $10k.")

# --- לוגיקת משיכת נתונים מתוקנת ---
@st.cache_data(ttl=30)
def fetch_data():
    url = "https://api.dexscreener.com/latest/dex/networks/solana"
    # הוספת Headers כדי למנוע חסימה מהשרת
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('pairs', [])
        else:
            return []
    except:
        return []

def filter_and_process(pairs):
    processed = []
    for p in pairs:
        vol_24h = float(p.get('volume', {}).get('h24', 0))
        liquidity = float(p.get('liquidity', {}).get('usd', 0))
        price_change_1h = float(p.get('priceChange', {}).get('h1', 0))
        
        if vol_24h > 50000 and liquidity > 10000:
            processed.append({
                "name": p.get('baseToken', {}).get('name', 'N/A'),
                "symbol": p.get('baseToken', {}).get('symbol', ''),
                "price": f"${float(p.get('priceUsd', 0)):.8f}",
                "change": price_change_1h,
                "vol": vol_24h,
                "liq": liquidity,
                "address": p.get('baseToken', {}).get('address', ''),
                "url": p.get('url', '')
            })
    return processed

# --- הצגת הנתונים ---
raw_pairs = fetch_data()
if raw_pairs:
    cleaned_data = filter_and_process(raw_pairs)
    
    st.markdown("---")
    h_cols = st.columns([2, 1.5, 1.5, 1.5, 2, 2])
    h_cols[0].write("**Token**")
    h_cols[1].write("**Price**")
    h_cols[2].write("**1h Change**")
    h_cols[3].write("**Liquidity**")
    h_cols[4].write("**Analysis**")
    h_cols[5].write("**Action**")

    for item in cleaned_data:
        with st.container():
            cols = st.columns([2, 1.5, 1.5, 1.5, 2, 2])
            cols[0].write(f"**{item['name']}** ({item['symbol']})")
            cols[1].write(item['price'])
            color = "#00ffbd" if item['change'] > 0 else "#ff4b4b"
            cols[2].markdown(f"<span style='color:{color}'>{item['change']}%</span>", unsafe_allow_html=True)
            cols[3].write(f"${item['liq']:,.0f}")
            cols[4].link_button("🔍 View Graph", item['url'])
            
            # קישור שותפים מעודכן עם ה-ID שלך ל-Maestro
            buy_link = f"https://t.me/MaestroSniperBot?start=67bcf12a-{item['address']}"
            cols[5].link_button("🚀 Buy via Bot", buy_link)
else:
    st.error("מתחבר לנתונים... האתר יתרענן אוטומטית בעוד כמה שניות")
    if st.button("נסה רענון ידני"):
        st.rerun()
