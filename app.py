import streamlit as st
import random
import re
import glob
import csv
import html as htmllib
from datetime import datetime, timedelta

# ==========================================
# SIMULATORE MONDIALE 2026 - V68 FULL WEB EDITION
# CT: Fabrizio Massa | Nessun taglio, 100% features
# ==========================================

st.set_page_config(page_title="Global Commander 2026", layout="wide", initial_sidebar_state="collapsed")

GIORNALISTI = ["Fabrizio Romano", "Gianluca Di Marzio", "Paolo Condò", "Tancredi Palmeri", "Luca Marchetti", "Matteo Marani", "Sandro Piccinini", "Fabio Caressa", "Ivan Zazzaroni", "Tony Damascelli", "Massimo Marianella", "Lele Adani", "Marco Barzaghi", "Peppe Di Stefano", "Nicolò Schira", "Claudio Raimondi"]
TESTATE = ["Gazzetta dello Sport", "Corriere dello Sport", "Tuttosport", "Sky Sport", "DAZN", "Rai Sport", "The Athletic"]

def _j(): return random.choice(GIORNALISTI)
def _t(): return random.choice(TESTATE)

# --- CSS PREMIUM DARK FM ---
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700;800&display=swap');
  :root { --bg-main: #090e17; --bg-card: rgba(15, 23, 42, 0.85); --border: rgba(56, 189, 248, 0.2); --accent: #3b82f6; --text-main: #f8fafc; --text-muted: #94a3b8; --green: #10b981; --red: #ef4444; --gold: #fbbf24; --neon-blue: #38bdf8; }
  
  /* Nascondi default UI Streamlit */
  header {visibility: hidden;} .block-container {padding-top: 1rem;}
  
  body, .stApp { background-color: var(--bg-main); color: var(--text-main); font-family: 'Inter', sans-serif; }
  .header-box { background: linear-gradient(90deg, #0f172a, #1e3a8a); padding: 25px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid var(--neon-blue); border-radius: 12px 12px 0 0; margin-bottom: 0px;}
  .logo-title { font-family: 'Bebas Neue', sans-serif; font-size: 42px; letter-spacing: 4px; color: #ffffff; line-height: 1; margin:0;}
  .logo-title span { color: var(--neon-blue); }
  .logo-sub { font-size: 13px; color: var(--text-muted); letter-spacing: 2px; font-weight: 700; text-transform: uppercase; margin-top: 4px;}
  .meta-date { font-size: 24px; font-weight: 700; color: white; margin:0; font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px;}
  
  .status-bar { background: #1e293b; padding: 15px 30px; display: flex; justify-content: space-between; color: var(--text-main); font-size: 13px; font-weight: 600; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px; border-radius: 0 0 12px 12px;}
  .status-val { color: #ffffff; background: rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-weight: 800;}
  
  .content-card { background: var(--bg-card); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 25px; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.3);}
  .card-title { font-family: 'Bebas Neue', sans-serif; font-size: 24px; letter-spacing: 2px; color: var(--neon-blue); margin-bottom: 20px; border-bottom: 2px solid rgba(255,255,255,0.1); padding-bottom: 8px; display: inline-block;}
  
  .data-table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; background: rgba(0,0,0,0.4); border-radius: 8px; overflow: hidden; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);}
  .data-table th { background: #0f172a; padding: 12px 14px; color: var(--neon-blue); font-weight: 700; text-transform: uppercase; letter-spacing: 1px; border-bottom: 2px solid var(--neon-blue);}
  .data-table td { padding: 12px 14px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc; font-weight: 500;}
  
  .badge-role { background: rgba(255,255,255,0.1); color: var(--neon-blue); padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 11px; letter-spacing: 1px; border: 1px solid rgba(56, 189, 248, 0.3);}
  .badge-ovr { background: var(--green); color: white; padding: 4px 8px; border-radius: 4px; font-weight: 800; font-size: 13px;}
  .evt-box { background: rgba(239,68,68,0.15); border-left: 5px solid var(--red); padding: 18px 25px; border-radius: 0 8px 8px 0; margin-bottom: 25px; color: #fca5a5; font-weight: 600; font-size: 15px;}
  
  /* PITCH TACTICAL FM VIEW */
  .match-screen { background: #0f172a; border-radius: 12px; padding: 25px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1); box-shadow: inset 0 0 20px rgba(0,0,0,0.8); }
  .score-board { display: flex; justify-content: space-between; align-items: center; background: #020617; padding: 25px; border-radius: 8px; margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.05);}
  .team-name { font-size: 36px; font-weight: 700; width: 35%; color: white; text-transform: uppercase; font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px;}
  .team-name.right { text-align: right; }
  .score-digits { font-family: 'Bebas Neue', sans-serif; font-size: 60px; color: var(--green); letter-spacing: 4px; margin:0; line-height: 1;}
  .live-dot { color: var(--red); font-size: 16px; margin-right: 8px;}
  .match-time { text-align: center; font-size: 24px; color: #ffffff; font-weight: 700; margin-bottom: 20px; background: #ef4444; padding: 6px 20px; border-radius: 6px; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.3);}
  
  .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; background: rgba(0,0,0,0.4); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 25px; box-shadow: inset 0 0 20px rgba(0,0,0,0.5);}
  .stat-box { display: flex; flex-direction: column; align-items: center; background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);}
  .stat-label { font-size: 11px; color: var(--text-muted); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 5px; font-weight: 600;}
  .stat-value { font-size: 18px; font-weight: 700; color: var(--neon-blue); font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px;}

  .football-pitch { background: #0f172a; background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px); background-size: 20px 20px; border: 2px solid rgba(255,255,255,0.2); border-radius: 8px; position: relative; display: flex; flex-direction: row; justify-content: space-between; margin-bottom: 25px; min-height: 520px; padding: 15px; box-shadow: inset 0 0 50px rgba(0,0,0,0.8);}
  .pitch-line-center { position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; background: rgba(255,255,255,0.2); transform: translateX(-50%);}
  .pitch-circle { position: absolute; left: 50%; top: 50%; width: 100px; height: 100px; border: 2px solid rgba(255,255,255,0.2); border-radius: 50%; transform: translate(-50%, -50%); }
  .pitch-penalty-box { position: absolute; top: 22%; bottom: 22%; width: 14%; border: 2px solid rgba(255,255,255,0.2); z-index: 1;}
  .left-box { left: 0; border-left: none; } .right-box { right: 0; border-right: none; }
  
  .pitch-half { width: 48%; display: flex; justify-content: space-around; z-index: 2; height: 100%; }
  .left-half { flex-direction: row; } .right-half { flex-direction: row-reverse; }
  .pitch-line { display: flex; flex-direction: column; justify-content: space-around; align-items: center; width: 25%; height: 100%; padding: 5px 0;}
  
  .pitch-card { background: rgba(15, 23, 42, 0.95); color: white; border-radius: 4px; padding: 6px; text-align: left; width: 105px; box-shadow: 0 4px 10px rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.1); border-top: 3px solid; transition: transform 0.2s;}
  .pitch-card:hover { transform: scale(1.1); z-index: 10; background: #1e293b;}
  .pitch-card .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px; }
  .pitch-card .role { font-size: 9px; font-weight: 700; opacity: 0.8; letter-spacing: 0.5px;}
  .pitch-card .cond-txt { font-size: 9px; font-weight: 800; }
  .pitch-card .name { font-size: 10px; font-weight: 700; white-space: normal; line-height: 1.2; margin: 3px 0;}
  .pitch-card .card-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 4px;}
  .pitch-card .voto { font-size: 11px; font-weight: 800; padding: 2px 5px; border-radius: 3px; display: inline-block; text-align: center; min-width: 24px;}
  .v-high { background: var(--green); color: white;} .v-mid { background: var(--gold); color: #000; } .v-low { background: var(--red); color: white;}
  .cond-bar-bg { width: 100%; background: rgba(255,255,255,0.1); height: 4px; border-radius: 2px; margin-top: 4px; overflow: hidden;}
  .cond-bar-fg { height: 100%; border-radius: 2px; }
  
  .event-log { background: #020617; padding: 15px; height: 180px; overflow-y: auto; border-radius: 6px; border: 1px solid rgba(255,255,255,0.1); font-size: 13px; font-weight: 500;}
  .evt-gol { color: #ffffff; font-weight: 800; background: rgba(16,185,129,0.2); padding: 4px 10px; border-radius: 4px; display: inline-block; margin: 3px 0; border-left: 3px solid var(--green);}
  
  /* BRACKET */
  .bracket-container { display:flex; flex-direction:row; justify-content:space-between; min-width:900px; padding:20px 0; gap:12px; overflow-x: auto;}
  .bracket-col { display:flex; flex-direction:column; justify-content:space-around; flex:1;}
  .bracket-title { text-align:center; font-weight:700; color:white; background:rgba(0,0,0,0.6); padding:8px; border-radius:6px; margin-bottom:20px; font-family:'Bebas Neue'; font-size: 22px; border-bottom: 2px solid var(--neon-blue);}
  .bracket-match { background:rgba(2,6,23,0.9); color:white; border:1px solid rgba(255,255,255,0.1); border-radius:6px; font-size:12px; padding:8px; margin:12px 0; box-shadow: 0 4px 10px rgba(0,0,0,0.4);}
  .bracket-team { padding:6px 8px; display:flex; justify-content:space-between; font-weight:600; border-radius:4px;}
  .bracket-team.winner { background: rgba(56, 189, 248, 0.15); border-left: 3px solid var(--neon-blue);}
  .bracket-ita { background: rgba(16,185,129,0.2) !important; border-left: 3px solid var(--green) !important;}
  .gold-final { background: rgba(251,191,36,0.1); border-color: var(--gold);}
</style>
""", unsafe_allow_html=True)

MODULI_TATTICI = {
    '4-3-3': ['POR', 'TD', 'DCD', 'DCS', 'TS', 'MED', 'CCD', 'CCS', 'AD', 'ATT', 'AS'],
    '4-2-3-1': ['POR', 'TD', 'DCD', 'DCS', 'TS', 'MED_D', 'MED_S', 'ED', 'COC', 'ES', 'ATT'],
    '3-5-2': ['POR', 'DCD', 'DC', 'DCS', 'ED', 'MED', 'CCD', 'CCS', 'ES', 'ATD', 'ATS']
}

RANKING_FIFA = {"Francia": 1, "Spagna": 2, "Argentina": 3, "Inghilterra": 4, "Portogallo": 5, "Brasile": 6, "Olanda": 7, "Marocco": 8, "Belgio": 9, "Germania": 10, "Croazia": 11, "Italia": 12, "Senegal": 14, "Messico": 15, "USA": 16, "Uruguay": 17, "Giappone": 18}

# --- FUNZIONI DI CARICAMENTO E SETUP ---
def _get_75_papabili():
    data = [
        ("Gianluigi Donnarumma", "POR", 89, "Paris SG"), ("Guglielmo Vicario", "POR", 85, "Tottenham"), ("Alex Meret", "POR", 83, "Napoli"), 
        ("Ivan Provedel", "POR", 83, "Lazio"), ("Marco Carnesecchi", "POR", 82, "Atalanta"), ("Michele Di Gregorio", "POR", 82, "Juventus"),
        ("Wladimiro Falcone", "POR", 80, "Lecce"), ("Elia Caprile", "POR", 78, "Empoli"),
        ("Alessandro Bastoni", "DIF", 87, "Inter"), ("Federico Dimarco", "DIF", 86, "Inter"), ("Giovanni Di Lorenzo", "DIF", 85, "Napoli"), 
        ("Alessandro Buongiorno", "DIF", 85, "Napoli"), ("Riccardo Calafiori", "DIF", 84, "Arsenal"), ("Giorgio Scalvini", "DIF", 83, "Atalanta"),
        ("Destiny Udogie", "DIF", 83, "Tottenham"), ("Gianluca Mancini", "DIF", 82, "Roma"), ("Andrea Cambiaso", "DIF", 83, "Juventus"), 
        ("Raoul Bellanova", "DIF", 82, "Atalanta"), ("Matteo Darmian", "DIF", 81, "Inter"), ("Federico Gatti", "DIF", 81, "Juventus"),
        ("Alessio Romagnoli", "DIF", 81, "Lazio"), ("Francesco Acerbi", "DIF", 82, "Inter"), ("Cristiano Biraghi", "DIF", 80, "Fiorentina"), 
        ("Leonardo Spinazzola", "DIF", 80, "Napoli"), ("Davide Calabria", "DIF", 80, "Milan"), ("Rafael Toloi", "DIF", 79, "Atalanta"),
        ("Nicolò Casale", "DIF", 79, "Bologna"), ("Fabiano Parisi", "DIF", 78, "Fiorentina"), ("Michael Kayode", "DIF", 78, "Fiorentina"), 
        ("Caleb Okoli", "DIF", 78, "Leicester"), ("Matteo Ruggeri", "DIF", 79, "Atalanta"), ("Matteo Gabbia", "DIF", 80, "Milan"),
        ("Lorenzo Pirola", "DIF", 77, "Olympiacos"),
        ("Nicolò Barella", "CEN", 88, "Inter"), ("Sandro Tonali", "CEN", 86, "Newcastle"), ("Lorenzo Pellegrini", "CEN", 84, "Roma"), 
        ("Davide Frattesi", "CEN", 84, "Inter"), ("Manuel Locatelli", "CEN", 83, "Juventus"), ("Bryan Cristante", "CEN", 82, "Roma"),
        ("Jorginho", "CEN", 82, "Arsenal"), ("Samuele Ricci", "CEN", 82, "Torino"), ("Nicolò Fagioli", "CEN", 81, "Juventus"), 
        ("Nicolò Rovella", "CEN", 81, "Lazio"), ("Giacomo Bonaventura", "CEN", 80, "Al-Shabab"), ("Matteo Pessina", "CEN", 80, "Monza"),
        ("Michael Folorunsho", "CEN", 79, "Napoli"), ("Andrea Colpani", "CEN", 80, "Fiorentina"), ("Edoardo Bove", "CEN", 79, "Fiorentina"), 
        ("Fabio Miretti", "CEN", 77, "Genoa"), ("Rolando Mandragora", "CEN", 78, "Fiorentina"), ("Marco Verratti", "CEN", 83, "Al-Arabi"),
        ("Gaetano Castrovilli", "CEN", 77, "Lazio"), ("Giovanni Fabbian", "CEN", 79, "Bologna"), ("Matteo Prati", "CEN", 76, "Cagliari"),
        ("Federico Chiesa", "ATT", 85, "Liverpool"), ("Mateo Retegui", "ATT", 84, "Atalanta"), ("Gianluca Scamacca", "ATT", 83, "Atalanta"), 
        ("Giacomo Raspadori", "ATT", 82, "Napoli"), ("Mattia Zaccagni", "ATT", 83, "Lazio"), ("Matteo Politano", "ATT", 82, "Napoli"),
        ("Riccardo Orsolini", "ATT", 82, "Bologna"), ("Moise Kean", "ATT", 81, "Fiorentina"), ("Stephan El Shaarawy", "ATT", 80, "Roma"), 
        ("Domenico Berardi", "ATT", 82, "Sassuolo"), ("Ciro Immobile", "ATT", 81, "Besiktas"), ("Lorenzo Lucca", "ATT", 80, "Udinese"),
        ("Wilfried Gnonto", "ATT", 78, "Leeds"), ("Nicolò Zaniolo", "ATT", 79, "Atalanta"), ("Andrea Pinamonti", "ATT", 79, "Genoa"), 
        ("Andrea Belotti", "ATT", 78, "Como"), ("Daniel Maldini", "ATT", 78, "Monza"), ("Lorenzo Colombo", "ATT", 77, "Empoli"),
        ("Pietro Pellegri", "ATT", 76, "Empoli"), ("Nicolò Cambiaghi", "ATT", 78, "Bologna"), ("Sebastiano Esposito", "ATT", 76, "Empoli")
    ]
    return [{"nome": d[0], "ruolo": d[1], "ovr": d[2], "club": d[3], "forma": random.randint(75, 95), "morale": random.randint(75, 95), "infortunio": random.choice(["Nessuno"]*15 + ["Affaticamento"])} for d in data]

def _carica_db_reale():
    db = {}; visti = set()
    for file in glob.glob("*.csv"):
        try:
            with open(file, mode='r', encoding='utf-8-sig', errors='replace') as f:
                content = f.read()
                if not content.strip(): continue
                sep = ',' if content.count(',') > content.count(';') else ';'
                f.seek(0)
                reader = csv.DictReader(f, delimiter=sep)
                naz_k = next((k for k in reader.fieldnames if k and 'naz' in k.lower()), None)
                gioc_k = next((k for k in reader.fieldnames if k and 'gioc' in k.lower()), None)
                ruolo_k = next((k for k in reader.fieldnames if k and 'ruol' in k.lower()), None)
                ovr_k = next((k for k in reader.fieldnames if k and 'over' in k.lower()), None)
                club_k = next((k for k in reader.fieldnames if k and ('squad' in k.lower() or 'club' in k.lower())), None)
                if not naz_k or not gioc_k: continue
                for row in reader:
                    naz = row.get(naz_k, '').strip(); nome = row.get(gioc_k, '').strip()
                    if not naz or not nome: continue
                    if (naz.lower(), nome.lower()) in visti: continue
                    visti.add((naz.lower(), nome.lower()))
                    r_raw = row.get(ruolo_k, 'CEN').upper() if ruolo_k else 'CEN'
                    r = 'CEN'
                    if r_raw in ['GK', 'POR', 'PT']: r = 'POR'
                    elif r_raw in ['CB', 'RB', 'LB', 'DIF', 'TD', 'TS', 'DC']: r = 'DIF'
                    elif r_raw in ['RW', 'LW', 'ST', 'ATT', 'AD', 'AS', 'ATD', 'ATS']: r = 'ATT'
                    try: ovr = int(row.get(ovr_k, 75)) if ovr_k else 75
                    except: ovr = 75
                    club = row.get(club_k, 'Sconosciuta').strip() if club_k else 'Sconosciuta'
                    if naz not in db: db[naz] = []
                    db[naz].append({"nome": nome, "ruolo": r, "ovr": ovr, "club": club, "forma": random.randint(85, 99), "morale": random.randint(85, 99), "infortunio": "Nessuno"})
        except: pass
    return db

def _get_gironi_base():
    return {
        'A': ['Messico', 'Sudafrica', 'Corea del Sud', 'Polonia'], 'B': ['Canada', 'Italia', 'Qatar', 'Svizzera'],
        'C': ['Brasile', 'Marocco', 'Jamaica', 'Scozia'], 'D': ['USA', 'Perù', 'Australia', 'Turchia'],
        'E': ['Germania', 'Venezuela', "Costa d'Avorio", 'Ecuador'], 'F': ['Olanda', 'Giappone', 'Danimarca', 'Serbia'],
        'G': ['Belgio', 'Egitto', 'Iran', 'Nuova Zelanda'], 'H': ['Spagna', 'Costa Rica', 'Arabia Saudita', 'Uruguay'],
        'I': ['Francia', 'Senegal', 'Iraq', 'Guinea'], 'J': ['Argentina', 'Algeria', 'Austria', 'Giordania'],
        'K': ['Portogallo', 'Camerun', 'Nigeria', 'Colombia'], 'L': ['Inghilterra', 'Croazia', 'Ghana', 'Panama']
    }

def _crea_calendario():
    cal = {}
    gironi = _get_gironi_base()
    md_dates = {
        1: ["2026-06-11", "2026-06-12", "2026-06-13", "2026-06-14", "2026-06-15", "2026-06-16", "2026-06-17"],
        2: ["2026-06-18", "2026-06-19", "2026-06-20", "2026-06-21", "2026-06-22", "2026-06-23"],
        3: ["2026-06-24", "2026-06-25", "2026-06-26", "2026-06-27"]
    }
    for phase in md_dates.values():
        for d in phase: cal[d] = {"is_ita": False, "tipo": "MONDIALE", "avv": "", "note": "Gironi", "partite": [], "risultati": {}}
    for let, sq in gironi.items():
        t1, t2, t3, t4 = sq
        matches = [(1, [(t1, t2), (t3, t4)]), (2, [(t1, t3), (t4, t2)]), (3, [(t4, t1), (t2, t3)])]
        for md, match_list in matches:
            offset = ord(let) - 65
            target_date = md_dates[md][offset % len(md_dates[md])]
            for m in match_list:
                cal[target_date]['partite'].append(m)
                if "Italia" in m:
                    cal[target_date]['is_ita'] = True
                    cal[target_date]['avv'] = m[1] if m[0] == "Italia" else m[0]
    return cal

def _genera_evento_casuale(s):
    if len(s.get('rosa_ita', [])) < 2: return "Allenamento standard a Coverciano."
    g1 = random.choice(s['rosa_ita'])['nome']
    categoria = random.choice([
        "STAMPA", "INFORTUNIO", "SPOGLIATOIO", "WAGS", "TIFOSI"
    ])
    if categoria == "STAMPA": t = [f"La Gazzetta titola: 'Italia senza idee, {g1} irriconoscibile'.", f"Intervista bomba di {g1}: 'Non gioco nel mio ruolo'."]
    elif categoria == "INFORTUNIO": t = [f"{g1} scivola in doccia. Fastidio alla caviglia.", f"Affaticamento muscolare per {g1} in allenamento."]
    elif categoria == "SPOGLIATOIO": t = [f"Tensione in spogliatoio, {g1} ripreso dai senatori.", f"{g1} arriva in ritardo alla riunione tecnica."]
    elif categoria == "WAGS": t = [f"La compagna di {g1} critica le scelte del mister su Instagram.", f"{g1} fotografato in un locale notturno."]
    else: t = [f"Bagno di folla per {g1} fuori dall'hotel.", f"Polemica sui social per un vecchio post di {g1}."]
    return random.choice(t)

# --- INIZIALIZZAZIONE SESSION STATE ---
if 's' not in st.session_state:
    db = _carica_db_reale()
    papabili = _get_75_papabili()
    
    # Riempi squadre bot
    req = ['POR']*3 + ['DIF']*8 + ['CEN']*8 + ['ATT']*7
    mappa_nomi = {"netherlands": "olanda", "stati uniti": "usa", "united states": "usa"}
    db_norm = {k.lower(): v for k, v in db.items()}
    gironi = _get_gironi_base()
    gironi_stato = {}
    
    for let, sq_list in gironi.items():
        gironi_stato[let] = {sq: {"pt":0,"gf":0,"gs":0, "pg":0, "v":0, "n":0, "p":0} for sq in sq_list}
        for t in sq_list:
            if t != 'Italia':
                t_low = t.lower()
                mapped = mappa_nomi.get(t_low, t_low)
                roster = db_norm.get(mapped, db_norm.get(t_low, []))
                rp = [p['ruolo'] for p in roster]
                mancanti = []
                for r in req:
                    if r in rp: rp.remove(r)
                    else: mancanti.append(r)
                for i, r in enumerate(mancanti):
                    roster.append({"nome": f"{t[:3]}_{r}{i}", "ruolo": r, "ovr": random.randint(70, 85), "club": "Naz", "forma": 90, "morale": 90, "infortunio": "Nessuno"})
                db[t] = roster

    st.session_state.s = {
        "fase": "CONVOCAZIONI", "data": "2026-06-10", "db": db, "papabili": papabili, "rosa_ita": [],
        "morale": 75, "coesione": 65, "evento": "Benvenuto Mister. Il database è caricato. Scegli i 26 convocati.",
        "calendario": _crea_calendario(), "gironi": gironi_stato, "tabellone": {}, "marcatori": {}
    }

s = st.session_state.s

# --- HEADER UI ---
st.markdown(f'<div class="header-box"><h1 class="logo-title">GLOBAL <span>COMMANDER</span></h1><div class="logo-sub">CT: Fabrizio Massa | World Cup 2026</div><div class="meta-date">{s["data"]}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="status-bar"><div>MORALE: <span class="status-val">{s["morale"]}%</span></div><div>COESIONE: <span class="status-val">{s["coesione"]}%</span></div></div>', unsafe_allow_html=True)

# ==========================================
# VIEWS
# ==========================================
if s["fase"] == "CONVOCAZIONI":
    st.markdown('<div class="content-card"><div class="card-title">LISTA 75 PAPABILI (SELEZIONA 26)</div>', unsafe_allow_html=True)
    giocatori = [f"{p['ruolo']} | {p['nome']} ({p['ovr']} - {p['club']})" for p in s['papabili']]
    scelti = st.multiselect("Scegli i tuoi 26 campioni (assicurati di avere 3 POR):", giocatori)
    
    if st.button("✓ CONFERMA E APRI IL MONDIALE", type="primary"):
        if len(scelti) == 26:
            nomi_scelti = [n.split("| ")[1].split(" (")[0] for n in scelti]
            s["rosa_ita"] = [p for p in s['papabili'] if p['nome'] in nomi_scelti]
            s["db"]["Italia"] = s["rosa_ita"]
            s["fase"] = "HUB"
            st.rerun()
        else: st.error(f"Devi scegliere esattamente 26 giocatori. Attuali: {len(scelti)}")
    st.markdown('</div>', unsafe_allow_html=True)

elif s["fase"] in ["HUB", "ROSA", "GIRONI", "CALENDARIO", "MARCATORI"]:
    cols = st.columns(5)
    if cols[0].button("🏠 HUB", use_container_width=True): s["fase"] = "HUB"; st.rerun()
    if cols[1].button("🇮🇹 ROSA", use_container_width=True): s["fase"] = "ROSA"; st.rerun()
    if cols[2].button("📊 GIRONI/TABELLONE", use_container_width=True): s["fase"] = "GIRONI"; st.rerun()
    if cols[3].button("📅 CALENDARIO", use_container_width=True): s["fase"] = "CALENDARIO"; st.rerun()
    if cols[4].button("⚽ MARCATORI", use_container_width=True): s["fase"] = "MARCATORI"; st.rerun()

    if s["fase"] == "HUB":
        st.markdown(f'<div class="content-card"><div class="card-title">🚨 DIARIO DI BORDO</div><div class="evt-box">{s["evento"]}</div></div>', unsafe_allow_html=True)
        
        oggi = s["data"]
        if oggi in s["calendario"] and s["calendario"][oggi].get("is_ita"):
            m = s["calendario"][oggi]
            st.markdown(f'<div class="content-card" style="text-align:center; background:linear-gradient(135deg, #0f172a, #1e293b); border: 2px solid var(--neon-blue);"><h1 style="color:var(--green); font-family:\'Bebas Neue\'; font-size:60px; margin:0;">MATCH DAY <span style="color:red; font-size:30px;">●</span></h1><div style="font-size:32px; font-weight:800;">ITALIA VS {m["avv"].upper()}</div><p style="color:var(--gold); font-weight:700;">{m["note"]}</p></div>', unsafe_allow_html=True)
            if st.button("🚨 VAI ALLA LAVAGNA TATTICA", type="primary", use_container_width=True):
                st.session_state.match = {
                    "avv": m["avv"], "step": "PRE", "tipo": m["tipo"], "minuto": 0, "score_ita": 0, "score_avv": 0,
                    "stats": {"poss_ita": 50, "poss_avv": 50, "tiri_ita": 0, "tiri_in_ita": 0, "tiri_out_ita":0, "tiri_avv": 0, "tiri_in_avv": 0, "tiri_out_avv":0, "pass_ita":0, "pass_avv":0, "contr_ita":0, "contr_avv":0, "falli_ita":0, "falli_avv":0},
                    "eventi": [], "scorers": [], "status": "PLAYING", "status_lbl": ""
                }
                s["fase"] = "MATCHDAY"
                st.rerun()
        else:
            st.markdown("<p>Incolla qui l'output di Gemini per processare le statistiche e avanzare al giorno successivo.</p>", unsafe_allow_html=True)
            a_gem = st.text_area("Risposta del Vice (OUTPUT PYTHON):", height=100)
            if st.button("PROCESSA E AVANZA GIORNO", type="primary", use_container_width=True):
                # Simula le partite del bot per oggi
                if oggi in s["calendario"]:
                    for match in s["calendario"][oggi]["partite"]:
                        if "Italia" not in match:
                            p1, p2 = match
                            g1 = max(0, int(random.gauss(1.6, 1.2)))
                            g2 = max(0, int(random.gauss(1.6, 1.2)))
                            
                            p1_pen, p2_pen = None, None
                            is_ko = s["calendario"][oggi].get("tipo") == "ELIMINATORIE"
                            if is_ko and g1 == g2:
                                if random.random() < 0.2: g1 += 1
                                if random.random() < 0.2: g2 += 1
                                if g1 == g2:
                                    p1_pen, p2_pen = 3, 2 # Semplificato
                                    
                            s["calendario"][oggi]["risultati"][f"{p1}-{p2}"] = (g1, g2, p1_pen, p2_pen)
                            
                            # Aggiorna Classifica Gironi
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
                
                d = datetime.strptime(s['data'], "%Y-%m-%d") + timedelta(days=1)
                s['data'] = d.strftime("%Y-%m-%d")
                s['evento'] = _genera_evento_casuale(s)
                st.rerun()

    elif s["fase"] == "ROSA":
        html = '<div class="content-card"><div class="card-title">ROSA ITALIA UFFICIALE</div><table class="data-table"><tr><th>NOME</th><th>R</th><th>OVR</th><th>CLUB</th><th>FORMA</th><th>MORALE</th><th>INFORTUNIO</th></tr>'
        for p in s['rosa_ita']:
            inf = "<span style='color:var(--green);'>Nessuno</span>" if p['infortunio'] == "Nessuno" else f"<span style='color:var(--red); font-weight:800;'>{p['infortunio']}</span>"
            html += f"<tr><td><strong>{p['nome']}</strong></td><td><span class='badge-role'>{p['ruolo']}</span></td><td><span class='badge-ovr'>{p['ovr']}</span></td><td>{p['club']}</td><td>{p['forma']}</td><td>{p['morale']}</td><td>{inf}</td></tr>"
        st.markdown(html + '</table></div>', unsafe_allow_html=True)

    elif s["fase"] == "GIRONI":
        html = '<div class="content-card"><div class="card-title">GIRONI MONDIALI 2026</div>'
        for let, sq in sorted(s['gironi'].items()):
            html += f'<div style="font-weight:800; margin:20px 0 5px 0; color:var(--neon-blue); font-size: 18px; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:4px;">GRUPPO {let}</div><table class="data-table"><tr><th style="width:35%;">SQUADRA</th><th>PT</th><th>PG</th><th>V</th><th>N</th><th>P</th><th>GF</th><th>GS</th></tr>'
            for n, d in sorted(sq.items(), key=lambda x: (-x[1]['pt'], -(x[1]['gf']-x[1]['gs']), -x[1]['gf'])):
                bg = "background:rgba(16,185,129,0.15);" if n == "Italia" else ""
                html += f"<tr style='{bg}'><td><strong>{n}</strong></td><td><strong>{d.get('pt', 0)}</strong></td><td>{d.get('pg', 0)}</td><td>{d.get('v', 0)}</td><td>{d.get('n', 0)}</td><td>{d.get('p', 0)}</td><td>{d.get('gf', 0)}</td><td>{d.get('gs', 0)}</td></tr>"
            html += '</table>'
        st.markdown(html + '</div>', unsafe_allow_html=True)

    elif s["fase"] == "CALENDARIO":
        html = '<div class="content-card"><div class="card-title">CALENDARIO GLOBALE & RISULTATI</div><table class="data-table"><tr><th>DATA</th><th>COMPETIZIONE</th><th>PARTITA</th></tr>'
        for d, info in sorted(s['calendario'].items()):
            bg = "background:rgba(255,255,255,0.05);" if d == s['data'] else ""
            for match in info.get('partite', []):
                p1, p2 = match
                b = "font-weight:900; color:var(--neon-blue);" if "Italia" in [p1, p2] else ""
                res_str = ""
                if 'risultati' in info and f"{p1}-{p2}" in info['risultati']:
                    res = info['risultati'][f"{p1}-{p2}"]
                    if len(res) == 4 and res[2] is not None:
                        res_str = f" <b style='color:var(--green);'>[{res[0]} - {res[1]} ({res[2]}-{res[3]} dcr)]</b>"
                    else:
                        res_str = f" <b style='color:var(--green);'>[{res[0]} - {res[1]}]</b>"
                html += f"<tr style='{bg}'><td><strong>{d}</strong></td><td>{info.get('tipo', 'MATCH')} - {info.get('note', '')}</td><td style='{b}'>{p1} vs {p2}{res_str}</td></tr>"
        st.markdown(html + '</table></div>', unsafe_allow_html=True)

elif s["fase"] == "MATCHDAY":
    md = st.session_state.match
    avv = md["avv"]
    
    if md["step"] == "PRE":
        st.markdown(f'<div class="content-card" style="text-align:center;"><h2 style="font-family:\'Bebas Neue\'; font-size:38px; color:var(--neon-blue);">LAVAGNA TATTICA: ITALIA VS {avv.upper()}</h2></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        mod = col1.selectbox("Modulo:", list(MODULI_TATTICI.keys()))
        ment = col2.selectbox("Mentalità:", ["Equilibrata", "Offensiva", "Difensiva"])
        
        if st.button("⚽ SCENDI IN CAMPO", type="primary", use_container_width=True):
            # Inizializza formazioni
            titolari = sorted(s['rosa_ita'], key=lambda x: -x['ovr'])[:11]
            panchina_ita = [p for p in s['rosa_ita'] if p not in titolari]
            
            avv_ros = s['db'].get(avv, [])
            if not avv_ros: avv_ros = [{"nome": f"Giocatore {i}", "ruolo": r, "ovr": 75, "forma": 90, "g":0} for i, r in enumerate(['POR']*1 + ['DIF']*4 + ['CEN']*3 + ['ATT']*3)]
            titolari_avv = sorted(avv_ros, key=lambda x: -x['ovr'])[:11]
            panchina_avv = [p for p in avv_ros if p not in titolari_avv]
            
            md.update({
                "step": "LIVE", "mentality": ment,
                "lineup_ita": [{"nome": p['nome'], "ruolo": p['ruolo'], "ruolo_gen": p['ruolo'], "cond": p.get('forma', 90), "voto": 6.0, "g":0} for p in titolari],
                "bench_ita": panchina_ita,
                "lineup_avv": [{"nome": p['nome'], "ruolo": p['ruolo'], "ruolo_gen": p['ruolo'], "cond": p.get('forma', 90), "voto": 6.0, "g":0} for p in titolari_avv],
                "bench_avv": panchina_avv
            })
            st.rerun()

    elif md["step"] == "LIVE":
        def render_pitch_card(p, is_ita):
            voto_cl = "v-high" if p['voto']>=7.0 else ('v-low' if p['voto']<6.0 else 'v-mid')
            gol_str = f"<span style='color:var(--gold);'>{'⚽'*p['g']}</span>" if p['g']>0 else ""
            border_col = "var(--neon-blue)" if is_ita else "var(--red)"
            cond_color = "var(--green)" if p['cond']>75 else ("var(--gold)" if p['cond']>50 else "var(--red)")
            return f"""
            <div class='pitch-card' style='border-left-color:{border_col};'>
                <div style='display:flex; justify-content:space-between; margin-bottom:2px;'>
                    <span style='font-size:9px; font-weight:700; color:{border_col};'>{p['ruolo']}</span>
                    <span style='font-size:9px; font-weight:800; color:{cond_color};'>⚡ {int(p['cond'])}%</span>
                </div>
                <div class='name'>{p['nome'][:12]}</div>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-top:4px;'>
                    <span class='voto-badge' style='background:{voto_cl};'>{p['voto']:.1f}</span>
                    {gol_str}
                </div>
            </div>
            """
            
        def render_half(lineup, is_ita):
            lines = [
                [p for p in lineup if p['ruolo_gen'] == 'POR'],
                [p for p in lineup if p['ruolo_gen'] == 'DIF'],
                [p for p in lineup if p['ruolo_gen'] == 'CEN'],
                [p for p in lineup if p['ruolo_gen'] == 'ATT']
            ]
            html = f"<div class='pitch-half {'left-half' if is_ita else 'right-half'}'>"
            for line in lines:
                html += "<div class='pitch-line'>"
                for p in line: html += render_pitch_card(p, is_ita)
                html += "</div>"
            html += "</div>"
            return html

        st.markdown(f"""
        <div class="content-card" style="margin-bottom:10px; padding:15px; display:flex; justify-content:space-between; align-items:center; background:#020617; border:1px solid var(--neon-blue);">
            <div style="font-family:'Bebas Neue'; font-size:36px;">ITALIA</div>
            <div style="font-family:'Bebas Neue'; font-size:50px; color:var(--green);"><span style="color:var(--red); font-size:20px; vertical-align:middle; margin-right:10px;">●</span>{md['score_ita']} - {md['score_avv']}</div>
            <div style="font-family:'Bebas Neue'; font-size:36px;">{avv.upper()}</div>
        </div>
        <div style="text-align:center; margin-bottom:15px;"><span style="background:var(--red); color:white; padding:5px 20px; border-radius:20px; font-weight:bold; font-size:20px;">{md['minuto']}' {md['status_lbl']}</span></div>
        
        <div style="display:flex; justify-content:space-around; background:rgba(0,0,0,0.4); padding:10px; border-radius:8px; margin-bottom:15px; font-size:12px; font-weight:700;">
            <div>POSSESSO: <span style="color:var(--neon-blue);">{md['stats']['poss_ita']}% - {md['stats']['poss_avv']}%</span></div>
            <div>TIRI (IN PORTA): <span style="color:var(--neon-blue);">{md['stats']['tiri_ita']} ({md['stats']['tiri_in_ita']}) - {md['stats']['tiri_avv']} ({md['stats']['tiri_in_avv']})</span></div>
            <div>PASSAGGI: <span style="color:var(--neon-blue);">{md['stats']['pass_ita']} - {md['stats']['pass_avv']}</span></div>
        </div>
        
        <div class="football-pitch">
            <div class="pitch-line-center"></div>
            <div class="pitch-circle"></div>
            {render_half(md['lineup_ita'], True)}
            {render_half(md['lineup_avv'], False)}
        </div>
        
        <div style="background:#020617; padding:15px; height:150px; overflow-y:auto; border-radius:8px; border:1px solid rgba(255,255,255,0.1); font-size:13px; margin-top:15px;">
            {"<br>".join(md['eventi'])}
        </div>
        """, unsafe_allow_html=True)
        
        if md['status'] in ["PLAYING", "PLAYING_ET"]:
            col1, col2 = st.columns(2)
            if col1.button("▶️ 1 MIN", use_container_width=True): mins = 1
            elif col2.button("⏩ 5 MIN", use_container_width=True): mins = 5
            else: mins = 0
            
            if mins > 0:
                for _ in range(mins):
                    if md['minuto'] < 90 and md['status'] == "PLAYING":
                        md['minuto'] += 1
                        # Logica stats semplificata web
                        md['stats']['poss_ita'] = random.randint(40, 60); md['stats']['poss_avv'] = 100 - md['stats']['poss_ita']
                        md['stats']['pass_ita'] += random.randint(3, 8); md['stats']['pass_avv'] += random.randint(3, 8)
                        for p in md['lineup_ita'] + md['lineup_avv']:
                            p['cond'] = max(10, p['cond'] - random.uniform(0.2, 0.4))
                            p['voto'] = max(4.0, min(9.0, p['voto'] + random.uniform(-0.1, 0.1)))
                        
                        if random.random() < 0.04:
                            md['stats']['tiri_ita'] += 1
                            if random.random() < 0.5:
                                md['stats']['tiri_in_ita'] += 1
                                p = random.choice([x for x in md['lineup_ita'] if x['ruolo_gen'] != 'POR'])
                                p['g'] += 1; p['voto'] += 1.5; md['score_ita'] += 1
                                md['eventi'].insert(0, f"<span style='color:var(--green); font-weight:bold;'>{md['minuto']}' - GOL ITALIA! {p['nome']}</span>")
                        
                        if random.random() < 0.04:
                            md['stats']['tiri_avv'] += 1
                            if random.random() < 0.5:
                                md['stats']['tiri_in_avv'] += 1
                                p = random.choice([x for x in md['lineup_avv'] if x['ruolo_gen'] != 'POR'])
                                p['g'] += 1; p['voto'] += 1.5; md['score_avv'] += 1
                                md['eventi'].insert(0, f"<span style='color:var(--red); font-weight:bold;'>{md['minuto']}' - GOL {avv.upper()}! {p['nome']}</span>")
                
                if md['minuto'] >= 90:
                    md['status'] = "FINISHED"; md['status_lbl'] = "(Finale)"
                st.rerun()

        elif md['status'] == "FINISHED":
            if st.button("✓ CONCLUDI PARTITA E TORNA ALL'HUB", type="primary", use_container_width=True):
                oggi = s['data']
                if oggi in s['calendario']:
                    s['calendario'][oggi]['risultati'][f"Italia-{avv}"] = (md['score_ita'], md['score_avv'], None, None)
                d = datetime.strptime(s['data'], "%Y-%m-%d") + timedelta(days=1)
                s['data'] = d.strftime("%Y-%m-%d")
                s['evento'] = f"Partita finita: Italia {md['score_ita']} - {md['score_avv']} {avv}."
                s['fase'] = "HUB"
                st.rerun()
