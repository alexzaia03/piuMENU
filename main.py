"""
Tutorial: Come usare l'IA in Python con chiave API da .env

Questo è un esempio generico che mostra come:
1. Caricare una chiave API da un file .env
2. Usare Google Gemini per generare contenuto
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# ============================================================
# PASSO 1: Carica le variabili d'ambiente dal file .env
# ============================================================
# Il file .env deve contenere: GOOGLE_API_KEY=tua_chiave_qui

load_dotenv()  # Carica automaticamente il file .env

# Recupera la chiave API
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Errore: non hai impostato GOOGLE_API_KEY nel file .env")
    print("Crea un file .env con il contenuto: GOOGLE_API_KEY=la_tua_chiave")
    exit(1)

print(f"✅ Chiave API caricata: {api_key[:10]}...")

# ============================================================
# PASSO 2: Configura l'IA con la tua chiave
# ============================================================
genai.configure(api_key=api_key)

# Scegli il modello da usare
model = genai.GenerativeModel('gemini-1.5-flash')

# ============================================================
# PASSO 3: Invia una richiesta all'IA
# ============================================================

# Esempio 1: Domanda semplice
print("\n--- Esempio 1: Domanda semplice ---")
response = model.generate_content("Ciao! Come stai?")
print(f"🤖 IA risponde: {response.text}")

# ============================================================
# Esempio 2: Generazione di testo creativo
print("\n--- Esempio 2: Testo creativo ---")
prompt = "Scrivi una breve poesia sul mare in italiano"
response = model.generate_content(prompt)
print(f"🤖 IA risponde:\n{response.text}")

# ============================================================
# Esempio 3: Analisi di dati (es. lista ingredienti)
print("\n--- Esempio 3: Analisi ingredienti ---")
ingredienti = ["pomodori", "mozzarella", "basilico", "olio d'oliva"]
prompt = f"Data questa lista di ingredienti: {ingredienti}. Che piatto consiglieresti di preparare? Rispondi in italiano."
response = model.generate_content(prompt)
print(f"🤖 IA consiglia: {response.text}")

# ============================================================
# Esempio 4: Menu giornaliero con vincoli
print("\n--- Esempio 4: Menu con vincoli ---")
prompt = """
Crea un menu giornaliero completo (colazione, pranzo, cena) 
per un ristorante italiano. Ogni piatto deve:
- Usare ingredienti di stagione
- Essere adatto a vegetariani
- Avere un prezzo tra 10-20€

Rispondi in formato JSON.
"""
response = model.generate_content(prompt)
print(f"🤖 Menu generato:\n{response.text}")

# ============================================================
# Esempio 5: Gestione errori
print("\n--- Esempio 5: Gestione errori ---")
try:
    response = model.generate_content("")  # Prompt vuoto per generare errore
except Exception as e:
    print(f"❌ Errore gestito: {e}")

print("\n✅ Tutorial completato!")