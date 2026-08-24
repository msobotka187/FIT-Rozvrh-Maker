import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import io
import uuid

# --- KONFIGURACE A PŘÍPRAVA DAT ---

# Nastavení stránky Streamlit
st.set_page_config(page_title="Tvorba rozvrhu", layout="wide")

# Inicializace session_state pro ukládání předmětů
if 'subjects' not in st.session_state:
    st.session_state.subjects = []

# Konstanty
DAYS = ["PO", "ÚT", "ST", "ČT", "PÁ"]
TYPES = ["Přednáška", "Cvičení", "Proseminář"]
COLORS = {
    "Přednáška": "orange",
    "Cvičení": "limegreen",
    "Proseminář": "dodgerblue"
}

# Časové sloty (celé i půlené)
TIME_SLOTS = [
    "07:30", "08:15", "09:00", 
    "09:15", "10:00", "10:45", 
    "11:00", "11:45", "12:30", 
    "12:45", "13:30", "14:15", 
    "14:30", "15:15", "16:00", 
    "16:15", "17:00", "17:45", 
    "18:00", "18:45", "19:30"
]

def time_to_float(time_str):
    '''Převede čas ve formátu HH:MM na desetinné číslo (např. 07:30 -> 7.5)'''
    h, m = map(int, time_str.split(':'))
    return h + m / 60.0

# --- SIDEBAR: FORMULÁŘ PRO PŘIDÁNÍ PŘEDMĚTU ---
st.sidebar.header("Přidat nový předmět")

with st.sidebar.form(key="add_subject_form"):
    name = st.text_input("Název předmětu (např. Matematika)")
    day = st.selectbox("Den", DAYS)
    type_ = st.selectbox("Typ hodiny", TYPES)
    
    start_time = st.selectbox("Čas od", TIME_SLOTS[:-1])
    end_time = st.selectbox("Čas do", TIME_SLOTS[1:])
    
    room = st.text_input("Místnost (max 10 znaků)", max_chars=10)
    
    submit_button = st.form_submit_button(label="Přidat do rozvrhu")
    
    if submit_button:
        # Validace časů
        if time_to_float(start_time) >= time_to_float(end_time):
            st.sidebar.error("Čas 'do' musí být větší než čas 'od'!")
        elif not name:
            st.sidebar.error("Zadejte název předmětu.")
        else:
            st.session_state.subjects.append({
                "id": str(uuid.uuid4()),
                "name": name,
                "day": day,
                "type": type_,
                "start_time": start_time,
                "end_time": end_time,
                "room": room
            })
            st.sidebar.success(f"Předmět {name} přidán!")

# --- HLAVNÍ OBSAH: VIZUALIZACE A SPRÁVA ---
st.title("Interaktivní školní rozvrh")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Náhled rozvrhu")
    
    # Vykreslení pomocí Matplotlib
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Nastavení os
    ax.set_xlim(7.25, 19.75)
    ax.set_ylim(-0.5, 4.5)
    
    # Nastavení osy Y (Dny)
    ax.set_yticks(range(5))
    ax.set_yticklabels(DAYS[::-1]) # PO nahoře (index 4), PÁ dole (index 0)
    
    # Nastavení osy X (Čas)
    xticks = [7.5, 9, 10.75, 12.5, 14.25, 16, 17.75, 19.5]
    ax.set_xticks([time_to_float(t) for t in TIME_SLOTS if t.endswith("00") or t.endswith("30")])
    ax.set_xticklabels([t for t in TIME_SLOTS if t.endswith("00") or t.endswith("30")], rotation=45)
    
    # Mřížka
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    
    # Vykreslení předmětů
    for sub in st.session_state.subjects:
        # Y pozice: PO=4, ÚT=3, ST=2, ČT=1, PÁ=0
        y_pos = 4 - DAYS.index(sub['day']) 
        
        x_start = time_to_float(sub['start_time'])
        x_end = time_to_float(sub['end_time'])
        width = x_end - x_start
        
        color = COLORS.get(sub['type'], 'gray')
        
        # Vytvoření obdélníku
        rect = patches.Rectangle(
            (x_start, y_pos - 0.4), width, 0.8, 
            linewidth=1, edgecolor='black', facecolor=color, alpha=0.8, zorder=3
        )
        ax.add_patch(rect)
        
        # Text uvnitř obdélníku
        text_lines = [sub['name']]
        if sub['room']:
            text_lines.append(sub['room'])
        
        ax.text(
            x_start + width/2, y_pos, 
            "\n".join(text_lines), 
            ha='center', va='center', fontsize=9, color='white', weight='bold',
            clip_on=True, zorder=4
        )

    plt.tight_layout()
    st.pyplot(fig)
    
    # Export do PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    buf.seek(0)
    
    st.download_button(
        label="📥 Stáhnout rozvrh jako PNG",
        data=buf,
        file_name="rozvrh.png",
        mime="image/png"
    )

with col2:
    st.subheader("Správa předmětů")
    
    if not st.session_state.subjects:
        st.info("Zatím nebyly přidány žádné předměty. Použijte formulář vlevo.")
    else:
        for index, sub in enumerate(st.session_state.subjects):
            with st.expander(f"{sub['name']} ({sub['day']} {sub['start_time']}-{sub['end_time']})", expanded=False):
                st.write(f"**Typ:** {sub['type']}")
                st.write(f"**Místnost:** {sub['room']}")
                
                # Tlačítko pro odstranění
                if st.button("🗑️ Smazat", key=f"del_{sub['id']}"):
                    st.session_state.subjects.pop(index)
                    st.rerun()

st.markdown("---")
st.markdown("💡 **Legenda:** <span style='color:orange;font-weight:bold'>Přednáška</span> | <span style='color:limegreen;font-weight:bold'>Cvičení</span> | <span style='color:dodgerblue;font-weight:bold'>Proseminář</span>", unsafe_allow_html=True)
