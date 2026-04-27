import streamlit as st
import random
import re
import glob
import csv
from datetime import datetime, timedelta

# ==========================================
# SIMULATORE MONDIALE 2026 - MASTER ENGINE V69
# CT: Fabrizio Massa | NATIVE MOBILE & ONE-TAP PROMPTS
# ==========================================

st.set_page_config(page_title="Global Commander 2026", layout="wide", initial_sidebar_state="collapsed")

GIORNALISTI = ["Fabrizio Romano", "Gianluca Di Marzio", "Paolo Condò", "Tancredi Palmeri", "Luca Marchetti", "Matteo Marani", "Sandro Piccinini", "Fabio Caressa", "Ivan Zazzaroni", "Lele Adani"]
TESTATE = ["Gazzetta dello Sport", "Corriere dello Sport", "Tuttosport", "Sky Sport", "DAZN", "Rai Sport", "The Athletic"]

def _j(): return random.choice(GIORNALISTI)
def _t(): return random.choice(TESTATE)

# --- CSS PREMIUM MOBILE-FRIENDLY ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;700;800&display=swap');
    :root { --neon-blue: #38bdf8; --green: #10b981; --gold: #fbbf24; --red: #ef4444; }
    body, .stApp { background-color: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    header {visibility: hidden;} .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    
    .header-box { background: linear-gradient(90deg, #0f172a, #1e3a8a); padding: 20px; border-bottom: 3px solid var(--neon-blue); border-radius: 10px 10px 0 0; text-align: center;}
    .logo-title { font-family: 'Bebas Neue', sans-serif; font-size: 40px; letter-spacing: 2px; color: white; margin:0; text-shadow: 0 0 15px var(--neon-blue);}
    .logo-title span { color: var(--neon-blue); }
    .status-bar { background: #1e293b; padding: 12px 20px; display: flex; justify-content: space-between; border-radius: 0 0 10px 10px; margin-bottom: 20px; font-weight: 700; font-size: 14px; border: 1px solid rgba(255,255,255,0.1); }
    .status-val { color: var(--neon-blue); }
    
    .content-card { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
    .card-title { font-family: 'Bebas Neue', sans-serif; font-size: 26px; color: var(--neon-blue); border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; padding-bottom: 5px; letter-spacing: 1px;}
    
    .evt-box { background: rgba(239,68,68,0.15); border-left: 4px solid var(--red); padding: 15px; border-radius: 4px; margin-bottom: 15px; color: #fca5a5; font-weight: 600;}
    
    .data-table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; background: rgba(0,0,0,0.3); border-radius: 6px; overflow: hidden; margin-bottom: 10px;}
    .data-table th { background: #0f172a; padding: 10px; color: var(--neon-blue); font-weight: 700; border-bottom: 2px solid var(--neon-blue);}
    .data-table td { padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); }
    
    .badge-role { background: rgba(255,255,255,0.1); color: var(--neon-blue); padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 11px;}
    .badge-ovr { background: var(--green); color: white; padding: 2px 6px; border-radius: 4px; font-weight: 800; font-size: 12px;}
    .delta-p { color: var(--green); font-size: 11px; font-weight: 800; margin-left: 4px;}
    .delta-n { color: var(--red); font-size: 11px; font-weight: 800; margin-left: 4px;}
    
    /* PITCH TACTICAL FM STYLE */
    .football-pitch { background: repeating-linear-gradient(0deg, #064e3b, #064e3b 30px, #14532d 30px, #14532d 60px); border: 3px solid rgba(255,255,255,0.5); border-radius: 10px; position: relative; display: flex; justify-content: space-between; min-height: 400px; padding: 10px; box-shadow: inset 0 0 30px black; overflow-x: auto;}
    .pitch-line-center { position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; background: rgba(255,255,255,0.3); transform: translateX(-50%); }
    .pitch-circle { position: absolute; left: 50%; top: 50%; width: 80px; height: 80px; border: 2px solid rgba(255,255,255,0.3); border-radius: 50%; transform: translate(-50%, -50%); }
    
    .pitch-half { width: 48%; display: flex; justify-content: space-around; z-index: 2; height: 100%; }
    .left-half { flex-direction: row; } .right-half { flex-direction: row-reverse; }
    .pitch-line { display: flex; flex-direction: column; justify-content: space-around; align-items: center; width: 25%;}
    
    .pitch-card { background: rgba(15,23,42,0.9); border-left: 3px solid var(--neon-blue); border-radius: 6px; padding: 6px; width: 95px; text-align: left; box-shadow: 0 4px 8px rgba(0,0,0,0.5); font-size: 10px; border-top: 1px solid rgba(255,255,255,0.1); margin: 2px 0;}
    .pitch-card .role { color: var(--neon-blue); font-weight: 800;}
    .pitch-card .cond { color: var(--green); font-weight: 800; float: right;}
    .pitch-card .name { font-size: 11px; font-weight: 700; color: white; display: block; margin: 4px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
    .voto-badge { background: var(--green); color: white; padding: 2px 5px; border-radius: 3px; font-weight: 800; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { padding: 10px 15px; background: rgba(30,41,59,0.5); border-radius: 8px; font-weight: 700; color: var(--text-muted); }
    .stTabs [aria-selected="true"] { background: var(--accent) !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

MODULI_TATTICI = {
    '4-3-3': ['POR', 'TD', 'DCD', 'DCS', 'TS', 'MED', 'CCD', 'CCS', 'AD', 'ATT', 'AS'],
    '4-2-3-1': ['POR', 'TD', 'DCD', 'DCS', 'TS', 'MED_D', 'MED_S', 'ED', 'COC', 'ES', 'ATT'],
    '3-5-2': ['POR', 'DCD', 'DC', 'DCS', 'ED', 'MED', 'CCD', 'CCS', 'ES', 'ATD', 'ATS']
}

RANKING = {"Francia": 1, "Spagna": 2, "Argentina": 3, "Inghilterra": 4, "Portogallo": 5, "Brasile": 6, "Olanda": 7, "Marocco": 8, "Belgio": 9, "Germania": 10, "Croazia": 11, "Italia": 12, "USA": 16, "Uruguay": 17}

# --- FUNZIONI CORE ---
def formatta_delta(val):
    if val > 0: return f"<span class='delta-p'>+{val}</span>"
    if val < 0: return f"<span class='delta-n'>{val}</span>"
    return ""

def genera_prompt(contesto):
    loc = "Coverciano, Italia" if datetime.strptime(st.session_state.s['data'], "%Y-%m-%d") < datetime.strptime("2026-05-20", "%Y-%m-%d") else "Nord America"
    return f"Sei l'Executive Coach nei Mondiali 2026. Io sono Fabrizio Massa, CT dell'Italia. Vice 'Oronzo Canà'.\nDATI: {st.session_state.s['data']} | {loc} | Morale: {st.session_state.s['morale_team']}%\n{contesto}\nISTRUZIONI: Analizza e consiglia. Chiudi OBBLIGATORIAMENTE con:\nOUTPUT PYTHON:\nRiassunto: [1 frase]\nMorale Team: +/- X\nCoesione: +/- Y\n[CognomeGiocatore]: Forma +/- X, Morale +/- Y, Infortunio: [Stato o Nessuno]\n(USA DELTA AMPI DA +/-3 A +/-10)"

def parse_db():
    db = {}
    visti = set()
    for file in glob.glob("*.csv") + glob.glob("/content/*.csv"):
        try:
            with open(file, mode='r', encoding='utf-8-sig', errors='replace') as f:
                content = f.read()
                if not content.strip(): continue
                sep = ',' if content.count(',') > content.count(';') else ';'
                f.seek(0)
                reader = csv.DictReader(f, delimiter=sep)
                naz_k = next((k for k in reader.fieldnames if k and 'naz' in k.lower()), None)
                gioc_k = next((k for k in reader.fieldnames if k and 'gioc' in k.lower()), None)
                if not naz_k or not gioc_k: continue
                for row in reader:
                    naz = row.get(naz_k, '').strip()
                    nome = row.get(gioc_k, '').strip()
                    if not naz or not nome: continue
                    if (naz.lower(), nome.lower()) in visti: continue
                    visti.add((naz.lower(), nome.lower()))
                    r_raw = row.get(next((k for k in reader.fieldnames if 'ruol' in k.lower()), ''), 'CEN').upper()
                    r = 'POR' if r_raw in ['GK','PT'] else ('DIF' if r_raw in ['CB','RB','LB','TD','TS','DC'] else ('ATT' if r_raw in ['RW','LW','ST','AD','AS'] else 'CEN'))
                    ovr = int(row.get(next((k for k in reader.fieldnames if 'over' in k.lower()), ''), 75) or 75)
                    if naz not in db: db[naz] = []
                    db[naz].append({"nome": nome, "ruolo": r, "ovr": ovr, "club": "Club", "forma": random.randint(85, 95), "morale": random.randint(85, 95), "infortunio": "Nessuno", "d_f":0, "d_m":0})
        except: pass
    return db

def init_calendario():
    cal = {
        "2026-04-20": {"is_ita": True, "tipo": "AMICHEVOLE", "avv": "Francia", "note": "Test Pre-Mondiale", "partite": [("Italia", "Francia"), ("Olanda", "Germania")], "risultati": {}},
        "2026-05-28": {"is_ita": True, "tipo": "AMICHEVOLE", "avv": "Uruguay", "note": "Ritiro USA", "partite": [("Italia", "Uruguay"), ("USA", "Brasile")], "risultati": {}},
        "2026-06-04": {"is_ita": True, "tipo": "AMICHEVOLE", "avv": "Messico", "note": "Ultimo Test Match", "partite": [("Italia", "Messico"), ("Spagna", "Portogallo")], "risultati": {}}
    }
    gironi = {
        'A': ['Messico', 'Sudafrica', 'Corea del Sud', 'Polonia'], 'B': ['Canada', 'Italia', 'Qatar', 'Svizzera'],
        'C': ['Brasile', 'Marocco', 'Jamaica', 'Scozia'], 'D': ['USA', 'Perù', 'Australia', 'Turchia'],
        'E': ['Germania', 'Venezuela', "Costa d'Avorio", 'Ecuador'], 'F': ['Olanda', 'Giappone', 'Danimarca', 'Serbia'],
        'G': ['Belgio', 'Egitto', 'Iran', 'Nuova Zelanda'], 'H': ['Spagna', 'Costa Rica', 'Arabia Saudita', 'Uruguay']
    }
    md_dates = {1: ["2026-06-11", "2026-06-12", "2026-06-13", "2026-06-14"], 2: ["2026-06-18", "2026-06-19", "2026-06-20", "2026-06-21"], 3: ["2026-06-24", "2026-06-25", "2026-06-26", "2026-06-27"]}
    
    for phase in md_dates.values():
        for d in phase: cal[d] = {"is_ita": False, "tipo": "MONDIALE", "avv": "", "note": "Fase a Gironi", "partite": [], "risultati": {}}
            
    for let, sq in gironi.items():
        matches = [(1, [(sq[0], sq[1]), (sq[2], sq[3])]), (2, [(sq[0], sq[2]), (sq[3], sq[1])]), (3, [(sq[3], sq[0]), (sq[1], sq[2])])]
        for md, m_list in matches:
            target_date = md_dates[md][(ord(let)-65) % len(md_dates[md])]
            for m in m_list:
                cal[target_date]['partite'].append(m)
                if "Italia" in m: cal[target_date].update({"is_ita": True, "avv": m[1] if m[0]=="Italia" else m[0]})
    return cal, gironi

def processa_gemini(testo, avanza=True):
    s = st.session_state.s
    try:
        m_r = re.search(r'Riassunto:\s*(.*)', testo, re.IGNORECASE)
        s['report_vice'] = m_r.group(1).strip() if m_r else "Dati aggiornati."
        
        m_m = re.search(r'Morale Team:\s*([+-]\d+)', testo, re.IGNORECASE)
        if m_m: s['morale_team'] = max(10, min(100, s['morale_team'] + int(m_m.group(1))))
        
        m_c = re.search(r'Coesione:\s*([+-]\d+)', testo, re.IGNORECASE)
        if m_c: s['coesione'] = max(10, min(100, s['coesione'] + int(m_c.group(1))))
        
        for p in s.get('rosa_ita', []):
            p['d_f'] = 0; p['d_m'] = 0
            ln = p['nome'].split()[-1].lower()
            for line in testo.split('\n'):
                if ln in line.lower() or p['nome'].lower() in line.lower():
                    m_f = re.search(r'Forma\s*([+-]\d+)', line, re.IGNORECASE)
                    m_mo = re.search(r'Morale\s*([+-]\d+)', line, re.IGNORECASE)
                    m_i = re.search(r'Infortunio:\s*([a-zA-Z0-9\s\(\)]+)', line, re.IGNORECASE)
                    if m_f: p['d_f'] = int(m_f.group(1)); p['forma'] = max(10, min(99, p['forma'] + p['d_f']))
                    if m_mo: p['d_m'] = int(m_mo.group(1)); p['morale'] = max(10, min(99, p['morale'] + p['d_m']))
                    if m_i: val = m_i.group(1).strip(); p['infortunio'] = val if val.lower() != "nessuno" else "Nessuno"
                    break
    except: pass
    
    if avanza:
        oggi = s['data']
        # Simula partite bot
        if oggi in s['calendario']:
            cal = s['calendario'][oggi]
            for m in cal['partite']:
                p1, p2 = m
                if p1 != "Italia" and p2 != "Italia":
                    diff = RANKING.get(p2, 50) - RANKING.get(p1, 50)
                    g1 = max(0, int(random.gauss(1.6 + (diff*0.02), 1.2)))
                    g2 = max(0, int(random.gauss(1.6 - (diff*0.02), 1.2)))
                    pen1, pen2 = None, None
                    if cal['tipo'] == 'ELIMINATORIE' and g1 == g2:
                        pen1, pen2 = 4, 3 # Semplificato
                    cal['risultati'][f"{p1}-{p2}"] = (g1, g2, pen1, pen2)
                    
                    if cal['tipo'] == 'MONDIALE':
                        for let, sq in s['gironi'].items():
                            if p1 in sq:
                                sq[p1]['pg']+=1; sq[p2]['pg']+=1; sq[p1]['gf']+=g1; sq[p2]['gf']+=g2; sq[p1]['gs']+=g2; sq[p2]['gs']+=g1
                                if g1>g2: sq[p1]['pt']+=3; sq[p1]['v']+=1; sq[p2]['p']+=1
                                elif g2>g1: sq[p2]['pt']+=3; sq[p2]['v']+=1; sq[p1]['p']+=1
                                else: sq[p1]['pt']+=1; sq[p2]['pt']+=1; sq[p1]['n']+=1; sq[p2]['n']+=1
                                
        s['data'] = (datetime.strptime(oggi, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        if len(s['rosa_ita']) > 1:
            g1 = random.choice(s['rosa_ita'])['nome']
            s['evento'] = random.choice([f"La stampa critica aspramente {g1} per il rendimento.", f"{g1} accusa un fastidio in allenamento.", f"Gossip su {g1}: paparazzato in un locale.", f"Tensione nello spogliatoio tra i senatori e {g1}."])

# --- INIT STATE ---
if 's' not in st.session_state:
    db = parse_db()
    ita_fall = [{"nome": f"Ita_{i}", "ruolo": r, "ovr": 80, "club": "Serie A", "forma": 90, "morale": 90, "infortunio": "Nessuno", "d_f":0, "d_m":0} for i, r in enumerate(['POR']*3 + ['DIF']*8 + ['CEN']*8 + ['ATT']*7)]
    if "Italia" not in db or len(db["Italia"]) < 20: db["Italia"] = ita_fall
    cal, g_base = init_calendario()
    g_stato = {let: {sq: {"pt":0,"gf":0,"gs":0, "pg":0, "v":0, "n":0, "p":0} for sq in sq_list} for let, sq_list in g_base.items()}
    
    st.session_state.s = {
        "fase": "CONVOCAZIONI", "data": "2026-04-15", "db": db, "papabili": db["Italia"], "rosa_ita": [],
        "morale_team": 75, "coesione": 65, "evento": "Benvenuto Mister. Seleziona i 26.", "report_vice": "Pronto agli ordini.",
        "calendario": cal, "gironi": g_stato, "tabellone": {}
    }
    st.session_state.match = None

s = st.session_state.s

# --- HEADER UI ---
st.markdown(f'<div class="header-box"><h1 class="logo-title">GLOBAL <span>COMMANDER</span></h1><div class="logo-sub">CT: Fabrizio Massa | World Cup 2026</div><div class="meta-date" style="margin-left:auto;">{s["data"]}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="status-bar"><div>MORALE TEAM: <span class="status-val">{s["morale_team"]}%</span></div><div>COESIONE: <span class="status-val">{s["coesione"]}%</span></div></div>', unsafe_allow_html=True)

# ==========================================
# ROUTER
# ==========================================
if s["fase"] == "CONVOCAZIONI":
    st.markdown('<div class="content-card"><div class="card-title">LISTA PAPABILI (SELEZIONA 26)</div>', unsafe_allow_html=True)
    giocatori = [f"{p['ruolo']} | {p['nome']} (OVR {p['ovr']})" for p in s['papabili']]
    scelti = st.multiselect("Scegli i tuoi 26 campioni (assicurati di avere 3 POR):", giocatori, default=giocatori[:26])
    
    if st.button("✓ CONFERMA E APRI IL MONDIALE", type="primary", use_container_width=True):
        if len(scelti) == 26:
            nomi = [n.split("| ")[1].split(" (")[0] for n in scelti]
            s["rosa_ita"] = [p for p in s['papabili'] if p['nome'] in nomi]
            s["fase"] = "HUB"
            st.rerun()
        else: st.error(f"Devi scegliere 26 giocatori. Ne hai scelti {len(scelti)}.")
    st.markdown("</div>", unsafe_allow_html=True)

elif s["fase"] == "HUB":
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 HUB", "🇮🇹 ROSA", "📊 GIRONI", "📅 CALENDARIO"])
    
    with tab1:
        st.markdown(f'<div class="content-card"><div class="card-title">🚨 DIARIO DI BORDO</div><div class="evt-box">{s["evento"]}</div><div style="background:rgba(56,189,248,0.1); padding:15px; border-left:4px solid var(--neon-blue); border-radius:4px; font-size:13px;">{s["report_vice"]}</div></div>', unsafe_allow_html=True)
        oggi = s["data"]
        
        if oggi in s["calendario"] and s["calendario"][oggi].get("is_ita"):
            m = s["calendario"][oggi]
            st.markdown(f'<div class="content-card" style="text-align:center; border:2px solid var(--neon-blue);"><h1 style="color:var(--green); font-family:\'Bebas Neue\'; font-size:50px; margin:0;">MATCH DAY <span style="color:red; font-size:20px; vertical-align:middle;">●</span></h1><div style="font-size:30px; font-weight:800;">ITALIA VS {m["avv"].upper()}</div><p style="color:var(--gold); font-weight:700; margin-top:5px;">{m["note"]}</p></div>', unsafe_allow_html=True)
            if st.button("🚨 VAI ALLA LAVAGNA TATTICA", type="primary", use_container_width=True):
                st.session_state.match = {
                    "avv": m["avv"], "step": "PRE", "tipo": m["tipo"], "minuto": 0, "score_ita": 0, "score_avv": 0,
                    "stats": {"poss_ita": 50, "poss_avv": 50, "tiri_ita": 0, "tiri_in_ita": 0, "tiri_avv": 0, "tiri_in_avv": 0, "pass_ita":0, "pass_avv":0},
                    "eventi": [], "status": "PLAYING", "status_lbl": ""
                }
                s["fase"] = "MATCHDAY"
                st.rerun()
        else:
            st.info("Copia questo prompt per ottenere l'analisi dal Vice (Gemini):")
            txt_prompt = genera_prompt(f"Evento: {s['evento']}\nRosa: " + ", ".join([f"{p['nome']} (F:{p['forma']} M:{p['morale']} I:{p['infortunio']})" for p in s['rosa_ita'][:5]]))
            st.code(txt_prompt, language="text")
            
            a_gem = st.text_area("Incolla qui la risposta di Gemini (OUTPUT PYTHON):", height=100)
            if st.button("PROCESSA E AVANZA GIORNO", type="primary", use_container_width=True):
                processa_gemini(a_gem, avanza=True)
                st.rerun()

    with tab2:
        html = '<table class="data-table"><tr><th>NOME</th><th>R</th><th>OVR</th><th>CLUB</th><th>FORMA</th><th>MORALE</th><th>INF</th></tr>'
        for p in s['rosa_ita']:
            inf = "<span style='color:var(--green);'>Nessuno</span>" if p['infortunio'] == "Nessuno" else f"<span style='color:var(--red); font-weight:800;'>{p['infortunio']}</span>"
            html += f"<tr><td><strong>{p['nome']}</strong></td><td><span class='badge-role'>{p['ruolo']}</span></td><td><span class='badge-ovr'>{p['ovr']}</span></td><td>{p['club']}</td><td><strong>{p['forma']}</strong>{formatta_delta(p['d_f'])}</td><td><strong>{p['morale']}</strong>{formatta_delta(p['d_m'])}</td><td>{inf}</td></tr>"
        st.markdown('<div class="content-card"><div class="card-title">ROSA ITALIA</div>' + html + '</table></div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="content-card"><div class="card-title">GIRONI MONDIALI</div>', unsafe_allow_html=True)
        for let, sq in sorted(s['gironi'].items()):
            html = f'<div style="font-weight:800; color:var(--neon-blue); font-size:16px; margin:15px 0 5px 0;">GRUPPO {let}</div><table class="data-table"><tr><th>SQUADRA</th><th>PT</th><th>PG</th><th>V</th><th>N</th><th>P</th><th>GF</th><th>GS</th></tr>'
            for n, d in sorted(sq.items(), key=lambda x: (-x[1]['pt'], -(x[1]['gf']-x[1]['gs']))):
                bg = "background:rgba(16,185,129,0.2);" if n == "Italia" else ""
                html += f"<tr style='{bg}'><td><strong>{n}</strong></td><td><strong>{d['pt']}</strong></td><td>{d['pg']}</td><td>{d['v']}</td><td>{d['n']}</td><td>{d['p']}</td><td>{d['gf']}</td><td>{d['gs']}</td></tr>"
            st.markdown(html + '</table>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        html = '<table class="data-table"><tr><th>DATA</th><th>PARTITA</th><th>RISULTATO</th></tr>'
        for d, info in sorted(s['calendario'].items()):
            bg = "background:rgba(255,255,255,0.05);" if d == s['data'] else ""
            for match in info.get('partite', []):
                p1, p2 = match
                b = "color:var(--neon-blue); font-weight:800;" if "Italia" in [p1, p2] else ""
                res_str = ""
                if 'risultati' in info and f"{p1}-{p2}" in info['risultati']:
                    res = info['risultati'][f"{p1}-{p2}"]
                    if len(res) == 4 and res[2] is not None: res_str = f" <b style='color:var(--green);'>[{res[0]}-{res[1]} ({res[2]}-{res[3]} dcr)]</b>"
                    else: res_str = f" <b style='color:var(--green);'>[{res[0]} - {res[1]}]</b>"
                html += f"<tr style='{bg}'><td>{d}</td><td style='{b}'>{p1} - {p2}</td><td>{res_str}</td></tr>"
        st.markdown('<div class="content-card"><div class="card-title">CALENDARIO & RISULTATI</div>' + html + '</table></div>', unsafe_allow_html=True)

elif s["fase"] == "MATCHDAY":
    md = st.session_state.match
    avv = md["avv"]
    
    if md["step"] == "PRE":
        st.markdown(f'<div class="content-card" style="text-align:center;"><h2 style="font-family:\'Bebas Neue\'; font-size:36px; color:var(--neon-blue); margin:0;">LAVAGNA TATTICA: ITALIA VS {avv.upper()}</h2></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        mod = c1.selectbox("Modulo:", list(MODULI_TATTICI.keys()))
        ment = c2.selectbox("Mentalità:", ["Equilibrata", "Offensiva", "Difensiva"])
        
        req = MODULI_TATTICI[mod]
        titolari = sorted(s['rosa_ita'], key=lambda x: -x['ovr'])[:11]
        
        st.info("Copia il prompt pre-partita:")
        st.code(genera_prompt(f"Spogliatoio pre-match Italia vs {avv}. Modulo: {mod}. Qualche consiglio tattico?"), language="text")
        a_gem = st.text_area("Incolla risposta Gemini:", height=80)
        
        if st.button("⚽ CONFERMA E SCENDI IN CAMPO", type="primary", use_container_width=True):
            if a_gem.strip(): processa_gemini(a_gem, avanza=False)
            
            avv_ros = s['db'].get(avv, [])
            if not avv_ros: avv_ros = [{"nome": f"{avv} Gioc {i}", "ruolo": r, "ovr": 75, "forma": 90, "morale": 90} for i, r in enumerate(req)]
            t_avv = sorted(avv_ros, key=lambda x: -x['ovr'])[:11]
            
            md.update({
                "step": "LIVE", "mentality": ment,
                "lineup_ita": [{"nome": p['nome'], "ruolo": req[i], "ruolo_gen": p['ruolo'], "cond": p['forma'], "voto": 6.0, "g":0} for i, p in enumerate(titolari)],
                "bench_ita": [p for p in s['rosa_ita'] if p not in titolari],
                "lineup_avv": [{"nome": p['nome'], "ruolo": req[i], "ruolo_gen": p['ruolo'], "cond": p['forma'], "voto": 6.0, "g":0} for i, p in enumerate(t_avv)],
            })
            st.rerun()

    elif md["step"] == "LIVE":
        def r_card(p, is_ita):
            v_cl = "v-high" if p['voto']>=7.0 else ('v-low' if p['voto']<6.0 else 'v-mid')
            g_str = f"<div style='color:var(--gold);'>{'⚽'*p['g']}</div>" if p['g']>0 else ""
            b_col = "var(--neon-blue)" if is_ita else "var(--red)"
            return f"<div class='pitch-card' style='border-top-color:{b_col};'><div style='display:flex; justify-content:space-between;'><span style='color:{b_col}; font-weight:800; font-size:9px;'>{p['ruolo']}</span><span style='color:var(--green); font-weight:800; font-size:9px;'>⚡{int(p['cond'])}%</span></div><div class='name'>{p['nome'][:12]}</div><div style='display:flex; justify-content:space-between; align-items:center;'><span class='voto-badge' style='background:var(--{v_cl});'>{p['voto']:.1f}</span>{g_str}</div></div>"
        
        def r_half(lineup, is_ita):
            html = f"<div class='pitch-half {'left-half' if is_ita else 'right-half'}'>"
            for r_t in ['POR', 'DIF', 'CEN', 'ATT']:
                html += "<div class='pitch-line'>" + "".join([r_card(p, is_ita) for p in lineup if p['ruolo_gen'] == r_t]) + "</div>"
            return html + "</div>"

        st.markdown(f"""
        <div style="background:#020617; padding:15px; border-radius:8px; border:1px solid var(--neon-blue); display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
            <div style="font-family:'Bebas Neue'; font-size:30px;">ITALIA</div>
            <div style="font-family:'Bebas Neue'; font-size:45px; color:var(--green);"><span style="color:red; font-size:15px; vertical-align:middle;">●</span> {md['score_ita']} - {md['score_avv']}</div>
            <div style="font-family:'Bebas Neue'; font-size:30px;">{avv.upper()}</div>
        </div>
        <div style="text-align:center; margin-bottom:15px;"><span style="background:var(--red); color:white; padding:5px 15px; border-radius:20px; font-weight:700; font-size:18px;">{md['minuto']}' {md['status_lbl']}</span></div>
        <div class="football-pitch"><div class="pitch-line-center"></div><div class="pitch-circle"></div>{r_half(md['lineup_ita'], True)}{r_half(md['lineup_avv'], False)}</div>
        <div style="background:rgba(0,0,0,0.5); padding:15px; border-radius:6px; font-size:12px; height:120px; overflow-y:auto; border:1px solid rgba(255,255,255,0.1); margin-top:15px; line-height:1.8;">{"<br>".join(md['eventi'])}</div>
        """, unsafe_allow_html=True)
        
        if md['status'] in ["PLAYING", "PLAYING_ET"]:
            c1, c2 = st.columns(2)
            mins = 1 if c1.button("▶️ 1 MIN", use_container_width=True) else (5 if c2.button("⏩ 5 MIN", use_container_width=True) else 0)
            
            if mins > 0:
                for _ in range(mins):
                    if md['minuto'] < 90 and md['status'] == "PLAYING":
                        md['minuto'] += 1
                        for p in md['lineup_ita'] + md['lineup_avv']: p['cond'] = max(10, p['cond'] - 0.3); p['voto'] = max(4.0, min(9.0, p['voto'] + random.uniform(-0.05, 0.05)))
                        if random.random() < 0.04:
                            p = random.choice([x for x in md['lineup_ita'] if x['ruolo_gen'] != 'POR'])
                            p['g'] += 1; p['voto'] = min(10.0, max(7.5, p['voto'] + 1.5)); md['score_ita'] += 1
                            md['eventi'].insert(0, f"<span style='color:var(--green); font-weight:800;'>{md['minuto']}' - GOL ITALIA! Segna {p['nome']}!</span>")
                        if random.random() < 0.04:
                            p = random.choice([x for x in md['lineup_avv'] if x['ruolo_gen'] != 'POR'])
                            p['g'] += 1; p['voto'] = min(10.0, max(7.5, p['voto'] + 1.5)); md['score_avv'] += 1
                            md['eventi'].insert(0, f"<span style='color:var(--red); font-weight:800;'>{md['minuto']}' - GOL {avv.upper()}! Segna {p['nome']}!</span>")
                if md['minuto'] >= 90: md['status'] = "FINISHED"; md['status_lbl'] = "(Finale)"
                st.rerun()
                
            st.markdown("<hr>", unsafe_allow_html=True)
            c3, c4 = st.columns(2)
            d_out = c3.selectbox("Esce:", [p['nome'] for p in md['lineup_ita']])
            d_in = c4.selectbox("Entra:", [p['nome'] for p in md['bench_ita']])
            if st.button("🔄 EFFETTUA CAMBIO", use_container_width=True):
                idx_out = next(i for i, p in enumerate(md['lineup_ita']) if p['nome'] == d_out)
                idx_in = next(i for i, p in enumerate(md['bench_ita']) if p['nome'] == d_in)
                po = md['lineup_ita'].pop(idx_out); pi = md['bench_ita'].pop(idx_in)
                md['lineup_ita'].insert(idx_out, {"nome": pi['nome'], "ruolo": po['ruolo'], "ruolo_gen": pi['ruolo_gen'], "cond": pi['forma'], "voto": 6.0, "g":0})
                md['bench_ita'].append({"nome": po['nome'], "ruolo_gen": po['ruolo_gen'], "forma": po['cond']})
                md['eventi'].insert(0, f"<span style='color:var(--neon-blue); font-style:italic;'>{md['minuto']}' - CAMBIO ITA: {pi['nome']} per {po['nome']}</span>")
                st.rerun()

        elif md['status'] == "FINISHED":
            if st.button("✓ CONCLUDI PARTITA E TORNA ALL'HUB", type="primary", use_container_width=True):
                oggi = s['data']
                if oggi in s['calendario']: s['calendario'][oggi]['risultati'][f"Italia-{avv}"] = (md['score_ita'], md['score_avv'], None, None)
                s['data'] = (datetime.strptime(oggi, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
                s['evento'] = f"Partita finita: Italia {md['score_ita']} - {md['score_avv']} {avv}."
                s['fase'] = "HUB"
                st.rerun()
