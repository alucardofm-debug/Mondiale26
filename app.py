import streamlit as st
import random
import re
import glob
import csv
from datetime import datetime, timedelta

# ==========================================
# SIMULATORE MONDIALE 2026 - MASTER ENGINE WEB
# CT: Fabrizio Massa | Tactical Dashboard V-FINAL
# ==========================================

st.set_page_config(page_title="Global Commander 2026", layout="wide", initial_sidebar_state="collapsed")

# --- CSS STYLING (FM DARK MODE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;700;800&display=swap');
    :root { --neon-blue: #38bdf8; --green: #10b981; --gold: #fbbf24; --red: #ef4444; }
    body, .stApp { background-color: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; }
    .header-box { background: linear-gradient(90deg, #0f172a, #1e3a8a); padding: 20px; border-bottom: 3px solid var(--neon-blue); border-radius: 10px; margin-bottom: 10px; text-align: center;}
    .logo-title { font-family: 'Bebas Neue', sans-serif; font-size: 45px; letter-spacing: 3px; color: white; margin:0; }
    .logo-title span { color: var(--neon-blue); }
    .status-bar { background: #1e293b; padding: 10px 20px; display: flex; justify-content: space-between; border-radius: 8px; margin-bottom: 20px; font-weight: 700; border: 1px solid rgba(255,255,255,0.1); }
    .content-card { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; margin-bottom: 20px; backdrop-filter: blur(10px); }
    .card-title { font-family: 'Bebas Neue', sans-serif; font-size: 24px; color: var(--neon-blue); border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; padding-bottom: 5px; }
    /* Tactical Pitch FM Style */
    .football-pitch { background: #0f172a; border: 3px solid rgba(255,255,255,0.2); border-radius: 8px; position: relative; display: flex; justify-content: space-between; min-height: 500px; padding: 15px; box-shadow: inset 0 0 50px black; }
    .pitch-line-center { position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; background: rgba(255,255,255,0.15); transform: translateX(-50%); }
    .pitch-card { background: #1e293b; border-left: 4px solid var(--neon-blue); border-radius: 4px; padding: 8px; width: 110px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
    .pitch-card .name { font-size: 11px; font-weight: 700; color: white; display: block; margin: 4px 0; }
    .voto-badge { background: var(--green); color: white; padding: 2px 5px; border-radius: 3px; font-size: 11px; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# --- FUNZIONI DI CARICAMENTO ---
def parse_db():
    db = {}
    csv_files = glob.glob("*.csv")
    for file in csv_files:
        try:
            with open(file, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                naz_k = next((k for k in reader.fieldnames if 'naz' in k.lower()), None)
                gioc_k = next((k for k in reader.fieldnames if 'gioc' in k.lower()), None)
                if not naz_k or not gioc_k: continue
                for row in reader:
                    naz = row.get(naz_k)
                    if naz not in db: db[naz] = []
                    db[naz].append({"nome": row.get(gioc_k), "ruolo": row.get('Ruolo', 'CEN'), "ovr": int(row.get('Overall', 75)), "club": row.get('Squadra', 'Club'), "forma": 95, "morale": 95})
        except: pass
    return db

# --- LOGICA DI STATO (SESSION STATE) ---
if 'stato' not in st.session_state:
    db = parse_db()
    st.session_state.stato = {
        "fase": "CONVOCAZIONI", "data": "2026-04-15", "db": db, 
        "rosa_ita": [], "morale": 75, "coesione": 65, "evento": "Inizio Ritiro a Coverciano."
    }

s = st.session_state.stato

# --- RENDERING UI ---
st.markdown(f'<div class="header-box"><h1 class="logo-title">GLOBAL <span>COMMANDER</span></h1><div class="logo-sub">CT: Fabrizio Massa | World Cup 2026</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="status-bar"><div>{s["data"].upper()}</div><div>MORALE: <span class="status-val">{s["morale"]}%</span></div><div>COESIONE: <span class="status-val">{s["coesione"]}%</span></div></div>', unsafe_allow_html=True)

if s["fase"] == "CONVOCAZIONI":
    st.markdown('<div class="content-card"><div class="card-title">SELEZIONE 26 CONVOCATI</div>', unsafe_allow_html=True)
    if not s["db"]:
        st.warning("Carica i file CSV nel repository GitHub per vedere i giocatori reali!")
    else:
        ita_players = s["db"].get("Italia", [])
        scelte = st.multiselect("Scegli i tuoi campioni:", [p["nome"] for p in ita_players])
        if st.button("CONFERMA LISTA"):
            if len(scelte) == 26:
                s["fase"] = "HUB"
                s["rosa_ita"] = scelte
                st.rerun()
            else:
                st.error(f"Devi scegliere 26 giocatori. Attuali: {len(scelte)}")
    st.markdown('</div>', unsafe_allow_html=True)

elif s["fase"] == "HUB":
    st.sidebar.title("Menu")
    if st.sidebar.button("🏠 HUB"): pass
    
    st.markdown(f'<div class="content-card"><div class="card-title">🚨 DIARIO DI BORDO</div><div class="evt-box">{s["evento"]}</div></div>', unsafe_allow_html=True)
    
    st.text_area("Incolla output Gemini qui:")
    if st.button("AVANZA GIORNO"):
        st.success("Giorno avanzato!")
