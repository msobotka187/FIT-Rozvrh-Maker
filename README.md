# Vibe-coded Rozvrh editor - WIP
**Je to komplet vibe-coded i tohle readme z většiny xd, můžete dělat issues s nápady popř. forky.**

Simple UI na plánování rozvrhu. 

## Co aplikace umí:
- **Tvorba rozvrhu**: Přidávání předmětů s vlastním časem (od-do), typem (Přednáška, Cvičení, Proseminář) a místností.
- **Vizualizace**: Automatické vykreslování přehledného kalendáře do mřížky.
- **Ukládání dat**: Rozvrh se automaticky ukládá do lokálního souboru `rozvrh_data.json`. Po restartu aplikace nepřijdete o data.
- **Úpravy a mazání**: Každý přidaný předmět můžete zpětně editovat nebo smazat přímo v aplikaci.
- **Export do PNG**: Vygenerovaný rozvrh lze jedním kliknutím stáhnout jako obrázek.

## Jak aplikaci spustit:
1. Ujistěte se, že máte nainstalovaný Python (ideálně 3.8+).
2. Nainstalujte potřebné knihovny:
   ```bash
   pip install streamlit matplotlib pandas
   ```
3. Spusťte aplikaci v terminálu ze složky, kde máte soubor app.py:
   ```bash
   streamlit run app.py
   ```
4. Aplikace se automaticky otevře v prohlížeči (obvykle na adrese `http://localhost:8501`).
