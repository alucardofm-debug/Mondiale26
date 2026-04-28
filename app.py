import streamlit as st
import random
import re
import glob
import csv
from datetime import datetime, timedelta

# ==========================================
# SIMULATORE MONDIALE 2026 - MASTER ENGINE V70
# CT: Fabrizio Massa | Reality Check, Full Groups, CSS Fixes
# ==========================================

st.set_page_config(page_title="Global Commander 2026", layout="wide", initial_sidebar_state="collapsed")

# --- CSS PREMIUM (ANTI-OVERLAP & CLARITY) ---
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
    
    .content-card { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
    .card-title { font-family: 'Bebas Neue', sans-serif; font-size: 26px; color: var(--neon-blue); border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; padding-bottom: 5px; letter-spacing: 1px;}
    
    .data-table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; background: rgba(0,0,0,0.3); border-radius: 6px; overflow: hidden; margin-bottom: 10px;}
    .data-table th { background: #0f172a; padding: 10px; color: var(--neon-blue); font-weight: 700; border-bottom: 2px solid var(--neon-blue);}
    .data-table td { padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); }
    
    .badge-role { background: rgba(255,255,255,0.1); color: var(--neon-blue); padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 11px;}
    
    /* PITCH TACTICAL - ANTI OVERLAP FIX */
    .football-pitch { 
        background: repeating-linear-gradient(0deg, #064e3b, #064e3b 40px, #14532d 40px, #14532d 80px); 
        border: 3px solid rgba(255,255,255,0.5); border-radius: 10px; position: relative; 
        display: flex; justify-content: space-between; 
        min-height: 600px; /* ALTEZZA AUMENTATA PER EVITARE SOVRAPPOSIZIONI */
        padding: 10px; box-shadow: inset 0 0 30px black; overflow-x: auto;
    }
    .pitch-line-center { position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; background: rgba(255,255,255,0.3); transform: translateX(-50%); }
    .pitch-circle { position: absolute; left: 50%; top: 50%; width: 80px; height: 80px; border: 2px solid rgba(255,255,255,0.3); border-radius: 50%; transform: translate(-50%, -50%); }
    
    .pitch-half { width: 48%; display: flex; justify-content: space-around; z-index: 2; height: 100%; align-items: stretch;}
    .left-half { flex-direction: row; } .right-half { flex-direction: row-reverse; }
    .pitch-line { display: flex; flex-direction: column; justify-content: space-around; align-items: center; width: 25%; min-height: 100%;}
    
    .pitch-card { 
        background: rgba(15,23,42,0.95); border-left: 3px solid var(--neon-blue); border-radius: 6px; 
        padding: 8px; width: 100px; text-align: left; box-shadow: 0 4px 8px rgba(0,0,0,0.5); 
        font-size: 11px; border-top: 1px solid rgba(255,255,255,0.1); margin: 5px 0;
        display: flex; flex-direction: column; justify-content: center;
    }
    .pitch-card.avv-card { border-left: 3px solid var(--red); }
    .pitch-card .name { font-size: 11px; font-weight: 700; color: white; display: block; margin: 4px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
    .voto-badge { background: var(--green); color: white; padding: 2px 5px; border-radius: 3px; font-weight: 800; font-size:10px;}
    
    details > summary { padding: 10px; background: rgba(30,41,59,0.8); border-radius: 6px; font-weight: 700; cursor: pointer; list-style: none;}
    details > summary::-webkit-details-marker { display: none; }
</style>
""", unsafe_allow_html=True)

# --- COSTANTI E DATI ---
MODULI_TATTICI = {
    '4-3-3': ['POR', 'TD', 'DCD', 'DCS', 'TS', 'MED', 'CCD', 'CCS', 'AD', 'ATT', 'AS'],
    '4-2-3-1': ['POR', 'TD', 'DCD', 'DCS', 'TS', 'MED_D', 'MED_S', 'ED', 'COC', 'ES', 'ATT'],
    '3-5-2': ['POR', 'DCD', 'DC', 'DCS', 'ED', 'MED', 'CCD', 'CCS', 'ES', 'ATD', 'ATS']
}

RANKING = {"Francia": 1, "Spagna": 2, "Argentina": 3, "Inghilterra": 4, "Portogallo": 5, "Brasile": 6, "Olanda": 7, "Marocco": 8, "Belgio": 9, "Germania": 10, "Croazia": 11, "Italia": 12, "USA": 16, "Uruguay": 17}

ITALIA_75 = [
    ("Gianluigi Donnarumma", "POR", 89), ("Guglielmo Vicario", "POR", 85), ("Alex Meret", "POR", 83), ("Ivan Provedel", "POR", 83), ("Marco Carnesecchi", "POR", 82),
    ("Alessandro Bastoni", "DIF", 87), ("Federico Dimarco", "DIF", 86), ("Giovanni Di Lorenzo", "DIF", 85), ("Alessandro Buongiorno", "DIF", 85), ("Riccardo Calafiori", "DIF", 84), ("Giorgio Scalvini", "DIF", 83), ("Destiny Udogie", "DIF", 83), ("Gianluca Mancini", "DIF", 82), ("Andrea Cambiaso", "DIF", 83),
    ("Nicolò Barella", "CEN", 88), ("Sandro Tonali", "CEN", 86), ("Lorenzo Pellegrini", "CEN", 84), ("Davide Frattesi", "CEN", 84), ("Manuel Locatelli", "CEN", 83), ("Samuele Ricci", "CEN", 82), ("Federico Chiesa", "ATT", 85), ("Mateo Retegui", "ATT", 84), ("Gianluca Scamacca", "ATT", 83), ("Giacomo Raspadori", "ATT", 82), ("Mattia Zaccagni", "ATT", 83), ("Moise Kean", "ATT", 81)
]

GIRONI_FULL = {
    'A': ['Messico', 'Sudafrica', 'Corea del Sud', 'Polonia'], 'B': ['Canada', 'Italia', 'Qatar', 'Svizzera'],
    'C': ['Brasile', 'Marocco', 'Jamaica', 'Scozia'], 'D': ['USA', 'Perù', 'Australia', 'Turchia'],
    'E': ['Germania', 'Venezuela', "Costa d'Avorio", 'Ecuador'], 'F': ['Olanda', 'Giappone', 'Danimarca', 'Serbia'],
    'G': ['Belgio', 'Egitto', 'Iran', 'Nuova Zelanda'], 'H': ['Spagna', 'Costa Rica', 'Arabia Saudita', 'Uruguay'],
    'I': ['Francia', 'Senegal', 'Iraq', 'Guinea'], 'J': ['Argentina', 'Algeria', 'Austria', 'Giordania'],
    'K': ['Portogallo', 'Camerun', 'Nigeria', 'Colombia'], 'L': ['Inghilterra', 'Croazia', 'Ghana', 'Panama']
}

def parse_and_fill_db():
    db = {}
    visti = set()
    # 1. Carica da CSV se presente
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
                    naz = row.get(naz_k, '').strip(); nome = row.get(gioc_k, '').strip()
                    if not naz or not nome: continue
                    if (naz.lower(), nome.lower()) in visti: continue
                    visti.add((naz.lower(), nome.lower()))
                    r_raw = row.get(next((k for k in reader.fieldnames if 'ruol' in k.lower()), ''), 'CEN').upper()
                    r = 'POR' if r_raw in ['GK','PT'] else ('DIF' if r_raw in ['CB','RB','LB','TD','TS','DC'] else ('ATT' if r_raw in ['RW','LW','ST','AD','AS'] else 'CEN'))
                    try: ovr = int(row.get(next((k for k in reader.fieldnames if 'over' in k.lower()), ''), 75) or 75)
                    except: ovr = 75
                    if naz not in db: db[naz] = []
                    db[naz].append({"nome": nome, "ruolo": r, "ovr": ovr, "club": "Club", "forma": random.randint(85, 95), "morale": random.randint(85, 95), "infortunio": "Nessuno"})
        except: pass
    
    # 2. Assicurati che TUTTE le 48 nazioni esistano
    req = ['POR']*3 + ['DIF']*8 + ['CEN']*8 + ['ATT']*7
    for sq_list in GIRONI_FULL.values():
        for t in sq_list:
            if t not in db: db[t] = []
            rp = [p['ruolo'] for p in db[t]]
            mancanti = []
            for r in req:
                if r in rp: rp.remove(r)
                else: mancanti.append(r)
            for i, r in enumerate(mancanti):
                db[t].append({"nome": f"Naz {t[:3]} {r}{i}", "ruolo": r, "ovr": random.randint(70, 85), "club": "Naz", "forma": 90, "morale": 90, "infortunio": "Nessuno"})
            
            ordine = {'POR': 1, 'DIF': 2, 'CEN': 3, 'ATT': 4}
            db[t] = sorted(db[t], key=lambda x: (ordine.get(x['ruolo'], 5), -x['ovr']))
            
    # Popola Italia Forzata
    if "Italia" not in db or len(db["Italia"]) < 26:
        db["Italia"] = [{"nome": n, "ruolo": r, "ovr": o, "club": "Serie A", "forma": random.randint(80,95), "morale": random.randint(80,95), "infortunio": "Nessuno"} for n, r, o in ITALIA_75]
        
    return db

def init_calendario():
    cal = {
        "2026-04-20": {"is_ita": True, "tipo": "AMICHEVOLE", "avv": "Francia", "note": "Test Pre-Mondiale", "partite": [("Italia", "Francia")], "risultati": {}},
        "2026-05-28": {"is_ita": True, "tipo": "AMICHEVOLE", "avv": "Uruguay", "note": "Ritiro USA", "partite": [("Italia", "Uruguay")], "risultati": {}},
        "2026-06-04": {"is_ita": True, "tipo": "AMICHEVOLE", "avv": "Messico", "note": "Ultimo Test", "partite": [("Italia", "Messico")], "risultati": {}}
    }
    md_dates = {
        1: ["2026-06-11", "2026-06-12", "2026-06-13", "2026-06-14"], 
        2: ["2026-06-18", "2026-06-19", "2026-06-20", "2026-06-21"], 
        3: ["2026-06-24", "2026-06-25", "2026-06-26", "2026-06-27"]
    }
    
    for phase in md_dates.values():
        for d in phase: cal[d] = {"is_ita": False, "tipo": "MONDIALE", "avv": "", "note": "Fase a Gironi", "partite": [], "risultati": {}}
            
    for let, sq in GIRONI_FULL.items():
        matches = [(1, [(sq[0], sq[1]), (sq[2], sq[3])]), (2, [(sq[0], sq[2]), (sq[3], sq[1])]), (3, [(sq[3], sq[0]), (sq[1], sq[2])])]
        for md, m_list in matches:
            target_date = md_dates[md][(ord(let)-65) % len(md_dates[md])]
            for m in m_list:
                cal[target_date]['partite'].append(m)
                if "Italia" in m: cal[target_date].update({"is_ita": True, "avv": m[1] if m[0]=="Italia" else m[0]})
    return cal

def formatta_delta(val):
    if val > 0: return f"<span class='delta-p'>+{val}</span>"
    if val < 0: return f"<span class='delta-n'>{val}</span>"
    return ""

# --- INIZIALIZZAZIONE SESSION STATE ---
if 's' not in st.session_state:
    db = parse_and_fill_db()
    cal = init_calendario()
    g_stato = {let: {sq: {"pt":0,"gf":0,"gs":0, "pg":0, "v":0, "n":0, "p":0} for sq in sq_list} for let, sq_list in GIRONI_FULL.items()}
    
    st.session_state.s = {
        "fase": "CONVOCAZIONI", "data": "2026-04-15", "db": db, "papabili": db["Italia"], "rosa_ita": [],
        "morale": 75, "coesione": 65, "evento": "Benvenuto Mister. Seleziona i 26.", "report_vice": "Attendo ordini, Mister.",
        "calendario": cal, "gironi": g_stato
    }
    st.session_state.match = None

s = st.session_state.s

# --- HEADER UI ---
st.markdown(f'<div class="header-box"><h1 class="logo-title">GLOBAL <span>COMMANDER</span></h1><div class="logo-sub">CT: Fabrizio Massa | World Cup 2026</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="status-bar"><div>{s["data"].upper()}</div><div>MORALE: <span class="status-val">{s["morale"]}%</span></div><div>COESIONE: <span class="status-val">{s["coesione"]}%</span></div></div>', unsafe_allow_html=True)

# ==========================================
# VIEWS
# ==========================================
if s["fase"] == "CONVOCAZIONI":
    st.markdown('<div class="content-card"><div class="card-title">LISTA PAPABILI (SELEZIONA 26)</div>', unsafe_allow_html=True)
    giocatori = [f"{p['ruolo']} | {p['nome']} (OVR {p['ovr']})" for p in s['papabili']]
    # Pre-seleziona i primi 26
    scelti = st.multiselect("Scegli i tuoi 26 campioni (assicurati di avere 3 POR):", giocatori, default=giocatori[:26])
    
    if st.button("✓ CONFERMA E APRI IL MONDIALE", type="primary", use_container_width=True):
        if len(scelti) == 26:
            nomi = [n.split("| ")[1].split(" (")[0] for n in scelti]
            s["rosa_ita"] = [p for p in s['papabili'] if p['nome'] in nomi]
            for p in s["rosa_ita"]: p['d_f'] = 0; p['d_m'] = 0
            s["fase"] = "HUB"
            st.rerun()
        else: st.error(f"Devi scegliere esattamente 26 giocatori. Attuali: {len(scelti)}")
    st.markdown("</div>", unsafe_allow_html=True)

elif s["fase"] in ["HUB", "ROSA", "GIRONI", "CALENDARIO"]:
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 HUB", "🇮🇹 ROSA", "📊 GIRONI", "📅 CAL"])
    
    with tab1:
        st.markdown(f'<div class="content-card"><div class="card-title">🚨 DIARIO DI BORDO</div><div class="evt-box">{s["evento"]}</div><div style="background:rgba(56,189,248,0.1); padding:15px; border-left:4px solid var(--neon-blue); border-radius:4px; font-size:13px;">{s["report_vice"]}</div></div>', unsafe_allow_html=True)
        oggi = s["data"]
        
        if oggi in s["calendario"] and s["calendario"][oggi].get("is_ita"):
            m = s["calendario"][oggi]
            st.markdown(f'<div class="content-card" style="text-align:center; border:2px solid var(--neon-blue);"><h1 style="color:var(--green); font-family:\'Bebas Neue\'; font-size:40px; margin:0;">MATCH DAY <span style="color:red; font-size:20px; vertical-align:middle;">●</span></h1><div style="font-size:24px; font-weight:800;">ITALIA VS {m["avv"].upper()}</div></div>', unsafe_allow_html=True)
            if st.button("🚨 VAI ALLA LAVAGNA TATTICA", type="primary", use_container_width=True):
                st.session_state.match = {
                    "avv": m["avv"], "step": "PRE", "tipo": m["tipo"], "minuto": 0, "score_ita": 0, "score_avv": 0,
                    "stats": {"poss_ita": 50, "poss_avv": 50, "tiri_ita": 0, "tiri_avv": 0}, "eventi": [], "status": "PLAYING", "status_lbl": ""
                }
                s["fase"] = "MATCHDAY"
                st.rerun()
        else:
            txt_prompt = f"Spogliatoio. Dati: {s['data']}. Morale: {s['morale']}%. Evento: {s['evento']}. Consiglia e chiudi con OUTPUT PYTHON: Riassunto, Morale Team, Coesione, Giocatore: Forma, Morale."
            st.info("Copia questo prompt e incollalo a Gemini:")
            st.code(txt_prompt, language="text")
            
            a_gem = st.text_area("Incolla qui la risposta di Gemini (OUTPUT PYTHON):", height=100)
            if st.button("PROCESSA E AVANZA GIORNO", type="primary", use_container_width=True):
                # 1. Parsing dei delta
                if a_gem.strip():
                    try:
                        m_r = re.search(r'Riassunto:\s*(.*)', a_gem, re.IGNORECASE)
                        s['report_vice'] = m_r.group(1).strip() if m_r else "Dati aggiornati."
                        for p in s['rosa_ita']:
                            p['d_f'] = 0; p['d_m'] = 0
                            ln = p['nome'].split()[-1].lower()
                            for line in a_gem.split('\n'):
                                if ln in line.lower() or p['nome'].lower() in line.lower():
                                    m_f = re.search(r'Forma\s*([+-]\d+)', line, re.IGNORECASE)
                                    m_mo = re.search(r'Morale\s*([+-]\d+)', line, re.IGNORECASE)
                                    if m_f: p['d_f'] = int(m_f.group(1)); p['forma'] = max(10, min(99, p['forma'] + p['d_f']))
                                    if m_mo: p['d_m'] = int(m_mo.group(1)); p['morale'] = max(10, min(99, p['morale'] + p['d_m']))
                                    break
                    except: pass

                # 2. Simulazione background CALIBRATA (Meno Gol)
                if oggi in s["calendario"]:
                    for match in s["calendario"][oggi]["partite"]:
                        if "Italia" not in match:
                            p1, p2 = match
                            diff = RANKING.get(p2, 50) - RANKING.get(p1, 50)
                            # Media base 1.1 gol invece di 1.6
                            g1 = max(0, int(random.gauss(1.1 + (diff*0.01), 1.0)))
                            g2 = max(0, int(random.gauss(1.1 - (diff*0.01), 1.0)))
                            s["calendario"][oggi]["risultati"][f"{p1}-{p2}"] = (g1, g2)
                            
                            if s["calendario"][oggi]["tipo"] == "MONDIALE":
                                for let, sq_dict in s['gironi'].items():
                                    if p1 in sq_dict:
                                        d1 = sq_dict[p1]; d2 = sq_dict[p2]
                                        d1['pg'] += 1; d2['pg'] += 1
                                        d1['gf'] += g1; d2['gf'] += g2
                                        d1['gs'] += g2; d2['gs'] += g1
                                        if g1 > g2: d1['pt'] += 3; d1['v'] += 1; d2['p'] += 1
                                        elif g2 > g1: d2['pt'] += 3; d2['v'] += 1; d1['p'] += 1
                                        else: d1['pt'] += 1; d2['pt'] += 1; d1['n'] += 1; d2['n'] += 1
                                        break
                
                # 3. Avanza Data
                d = datetime.strptime(s['data'], "%Y-%m-%d") + timedelta(days=1)
                s['data'] = d.strftime("%Y-%m-%d")
                s['evento'] = random.choice(["Allenamento tattico a Coverciano.", "Giornata di scarico muscolare.", "Riunione video per analizzare gli avversari."])
                st.rerun()

    with tab2:
        html = '<table class="data-table"><tr><th>NOME</th><th>R</th><th>OVR</th><th>FORMA</th></tr>'
        for p in s['rosa_ita']:
            html += f"<tr><td><strong>{p['nome']}</strong></td><td><span class='badge-role'>{p['ruolo']}</span></td><td><span class='badge-ovr'>{p['ovr']}</span></td><td><strong>{p['forma']}</strong> {formatta_delta(p.get('d_f', 0))}</td></tr>"
        st.markdown('<div class="content-card"><div class="card-title">ROSA ITALIA</div>' + html + '</table></div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="content-card"><div class="card-title">GIRONI MONDIALI E ROSE</div>', unsafe_allow_html=True)
        for let, sq in sorted(s['gironi'].items()):
            html = f'<div style="font-weight:800; color:var(--neon-blue); font-size:16px; margin:15px 0 5px 0;">GRUPPO {let}</div><table class="data-table"><tr><th style="width:40%;">SQUADRA</th><th>PT</th><th>PG</th><th>V</th><th>N</th><th>P</th></tr>'
            for n, d in sorted(sq.items(), key=lambda x: (-x[1]['pt'], -(x[1]['gf']-x[1]['gs']))):
                bg = "background:rgba(16,185,129,0.2);" if n == "Italia" else ""
                
                # Costruisci tendina rosa
                r_html = '<div style="background:#0f172a; padding:5px; border-radius:4px; margin-top:5px; font-size:11px;">'
                roster = s['db'].get(n, [])
                for p in roster:
                    r_html += f"<div><span style='color:var(--neon-blue); font-weight:bold;'>{p['ruolo']}</span> {p['nome']} <span style='color:var(--green); float:right;'>{p['ovr']}</span></div>"
                r_html += '</div>'
                
                det_html = f"<details><summary>{n}</summary>{r_html}</details>"
                html += f"<tr style='{bg}'><td>{det_html}</td><td><strong>{d['pt']}</strong></td><td>{d['pg']}</td><td>{d['v']}</td><td>{d['n']}</td><td>{d['p']}</td></tr>"
            st.markdown(html + '</table>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab4:
        html = '<table class="data-table"><tr><th>DATA</th><th>PARTITA</th><th>RISULTATO</th></tr>'
        for d, info in sorted(s['calendario'].items()):
            bg = "background:rgba(255,255,255,0.05);" if d == s['data'] else ""
            for match in info.get('partite', []):
                p1, p2 = match
                b = "color:var(--neon-blue); font-weight:800;" if "Italia" in [p1, p2] else ""
                res_str = f" <b style='color:var(--green);'>[{info['risultati'][f'{p1}-{p2}'][0]} - {info['risultati'][f'{p1}-{p2}'][1]}]</b>" if 'risultati' in info and f"{p1}-{p2}" in info['risultati'] else ""
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
        
        if st.button("⚽ CONFERMA E SCENDI IN CAMPO", type="primary", use_container_width=True):
            avv_ros = s['db'].get(avv, [])
            if not avv_ros: avv_ros = [{"nome": f"{avv} Gioc {i}", "ruolo": r, "ovr": 75, "forma": 90, "morale": 90} for i, r in enumerate(req)]
            t_avv = sorted(avv_ros, key=lambda x: -x['ovr'])[:11]
            
            md.update({
                "step": "LIVE", "mentality": ment,
                "lineup_ita": [{"nome": p['nome'], "ruolo": req[i], "ruolo_gen": p['ruolo'], "cond": p.get('forma', 90), "voto": 6.0, "g":0} for i, p in enumerate(titolari)],
                "bench_ita": [p for p in s['rosa_ita'] if p not in titolari],
                "lineup_avv": [{"nome": p['nome'], "ruolo": req[i], "ruolo_gen": p['ruolo'], "cond": p.get('forma', 90), "voto": 6.0, "g":0} for i, p in enumerate(t_avv)],
            })
            st.rerun()

    elif md["step"] == "LIVE":
        def r_card(p, is_ita):
            v_cl = "v-high" if p['voto']>=7.0 else ('v-low' if p['voto']<6.0 else 'v-mid')
            g_str = f"<div style='color:var(--gold); position:absolute; top:-5px; right:-5px; font-size:12px;'>{'⚽'*p['g']}</div>" if p['g']>0 else ""
            b_col = "var(--neon-blue)" if is_ita else "var(--red)"
            return f"<div class='pitch-card {'' if is_ita else 'avv-card'}' style='position:relative;'><div style='display:flex; justify-content:space-between;'><span style='color:{b_col}; font-weight:800; font-size:10px;'>{p['ruolo']}</span><span style='color:var(--green); font-weight:800; font-size:9px;'>⚡{int(p['cond'])}%</span></div><div class='name'>{p['nome']}</div><div style='display:flex; justify-content:flex-end;'><span class='voto-badge' style='background:var(--{v_cl});'>{p['voto']:.1f}</span></div>{g_str}</div>"
        
        def r_half(lineup, is_ita):
            html = f"<div class='pitch-half {'left-half' if is_ita else 'right-half'}'>"
            for r_t in ['POR', 'DIF', 'CEN', 'ATT']:
                html += "<div class='pitch-line'>" + "".join([r_card(p, is_ita) for p in lineup if p['ruolo_gen'] == r_t]) + "</div>"
            return html + "</div>"

        st.markdown(f"""
        <div style="background:#1e293b; padding:15px; border-radius:8px; border:1px solid var(--neon-blue); display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
            <div style="font-family:'Bebas Neue'; font-size:30px;">ITALIA</div>
            <div style="font-family:'Bebas Neue'; font-size:45px; color:var(--green);"><span style="color:red; font-size:15px; vertical-align:middle;">●</span> {md['score_ita']} - {md['score_avv']}</div>
            <div style="font-family:'Bebas Neue'; font-size:30px;">{avv.upper()}</div>
        </div>
        <div style="text-align:center; margin-bottom:15px;"><span style="background:var(--red); color:white; padding:5px 15px; border-radius:20px; font-weight:700; font-size:18px;">{md['minuto']}' {md['status_lbl']}</span></div>
        <div class="football-pitch"><div class="pitch-line-center"></div><div class="pitch-circle"></div>{r_half(md['lineup_ita'], True)}{r_half(md['lineup_avv'], False)}</div>
        <div style="background:rgba(0,0,0,0.5); padding:10px; border-radius:6px; font-size:11px; height:120px; overflow-y:auto; border:1px solid rgba(255,255,255,0.1); margin-top:15px;">{"<br>".join(md['eventi'])}</div>
        """, unsafe_allow_html=True)
        
        if md['status'] in ["PLAYING", "PLAYING_ET"]:
            c1, c2 = st.columns(2)
            mins = 1 if c1.button("▶️ 1 MIN", use_container_width=True) else (5 if c2.button("⏩ 5 MIN", use_container_width=True) else 0)
            
            if mins > 0:
                for _ in range(mins):
                    if md['minuto'] < 90 and md['status'] == "PLAYING":
                        md['minuto'] += 1
                        for p in md['lineup_ita'] + md['lineup_avv']: p['cond'] = max(10, p['cond'] - 0.3); p['voto'] = max(4.0, min(9.0, p['voto'] + random.uniform(-0.05, 0.05)))
                        
                        # Probabilità abbassata enormemente per score realistici
                        if random.random() < 0.015:
                            p = random.choice([x for x in md['lineup_ita'] if x['ruolo_gen'] != 'POR'])
                            p['g'] += 1; p['voto'] = min(10.0, max(7.5, p['voto'] + 1.5)); md['score_ita'] += 1
                            md['eventi'].insert(0, f"<span style='color:var(--green); font-weight:800;'>{md['minuto']}' - GOL ITALIA! Segna {p['nome']}!</span>")
                        if random.random() < 0.015:
                            p = random.choice([x for x in md['lineup_avv'] if x['ruolo_gen'] != 'POR'])
                            p['g'] += 1; p['voto'] = min(10.0, max(7.5, p['voto'] + 1.5)); md['score_avv'] += 1
                            md['eventi'].insert(0, f"<span style='color:var(--red); font-weight:800;'>{md['minuto']}' - GOL {avv.upper()}! Segna {p['nome']}!</span>")
                if md['minuto'] >= 90: md['status'] = "FINISHED"; md['status_lbl'] = "(Finale)"
                st.rerun()

        elif md['status'] == "FINISHED":
            if st.button("✓ CONCLUDI PARTITA E TORNA ALL'HUB", type="primary", use_container_width=True):
                oggi = s['data']
                if oggi in s['calendario']: s['calendario'][oggi]['risultati'][f"Italia-{avv}"] = (md['score_ita'], md['score_avv'], None, None)
                s['data'] = (datetime.strptime(oggi, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
                s['evento'] = f"Partita finita: Italia {md['score_ita']} - {md['score_avv']} {avv}."
                s['fase'] = "HUB"
                st.rerun()
