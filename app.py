import streamlit as st
import pandas as pd
import requests

# --- הגדרות דף ---
st.set_page_config(page_title="AlphaScan AI | Solana Whale Hunter", layout="wide", page_icon="⚡")

# עיצוב פינטק מתקדם (Dark Mode Custom CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: #e9eaeb; }
    .stButton>button { width: 100%; border-radius: 8px; background: linear-gradient(90deg, #00ffbd, #00d4ff); color: black; font-weight: bold; border: none; }
    .metric-card { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; }
    .token-row { border-bottom: 1px solid #30363d; padding: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- כותרת ראשית ---
st.title("⚡ AlphaScan AI: Solana Hunter")
st.write("סורק בזמן אמת מטבעות חדשים עם זינוק בנפח המסחר (ווליום)")

# --- תפריט צד (Affiliate & Links) ---
with st.sidebar:
    st.image("https://cryptologos.cc/logos/solana-sol-logo.png", width=50)
    st.header("💎 פלטפורמות מומלצות")
    st.markdown("### 🤖 מסחר מהיר (הכי מומלץ)")
    # כאן תחליף לקישור השותפים שלך ב-BonkBot
    st.markdown("[🚀 Trade via BonkBot (Referral)](https://t.me/bonkbot?start=ref_your_id)")
    
    st.markdown("---")
    st.markdown("### 📊 בורסות מובילות")
    st.markdown("[🔗 Binance (10% Discount)](https://your-link)")
    st.markdown("[🔗 OKX Bonus](https://your-link)")
    
    st.write("---")
    st.caption("הכלי סורק מטבעות שנוצרו ב-24 שעות האחרונות עם נזילות של מעל $10k.")

# --- לוגיקת משיכת נתונים ---
@st.cache_data(ttl=30)  # רענון כל 30 שניות
def fetch_data():
    url = "https://api.dexscreener.com/latest/dex/networks/solana"
    try:
        response = requests.get(url)
        return response.json().get('pairs', [])
    except:
        return []

def filter_and_process(pairs):
    processed = []
    for p in pairs:
        # פילטרים למניעת זבל: ווליום מעל 50k ונזילות מעל 10k
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
    
    # כותרות טבלה
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
            
            # שם המטבע
            cols[0].write(f"**{item['name']}** ({item['symbol']})")
            
            # מחיר
            cols[1].write(item['price'])
            
            # שינוי במחיר (צבעוני)
            color = "#00ffbd" if item['change'] > 0 else "#ff4b4b"
            cols[2].markdown(f"<span style='color:{color}'>{item['change']}%</span>", unsafe_allow_html=True)
            
            # נזילות
            cols[3].write(f"${item['liq']:,.0f}")
            
            # קישור לגרף
            cols[4].link_button("🔍 View Graph", item['url'])
            
            # כפתור קנייה (Affiliate)
            # הקישור הזה שולח לבוט בטלגרם עם כתובת המטבע מוכנה לקנייה
           buy_link = f"https://t.me/MaestroSniperBot?start=67bcf12a-{item['address']}"
            cols[5].link_button("🚀 Buy (BonkBot)", buy_link)
else:
    st.error("לא ניתן למשוך נתונים כרגע. נסה שוב בעוד דקה.")
