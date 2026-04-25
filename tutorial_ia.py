"""
Tutorial: Come usare l'IA in Python con chiave API da .env

Questo è un esempio generico che mostra come:
1. Caricare una chiave API da un file .env
2. Usare Google Gemini per generare contenuto
"""

import google.generativeai as genai

# ============================================================
# PASSO 1: Carica le variabili d'ambiente dal file .env
# ============================================================
# Il file .env deve contenere: GOOGLE_API_KEY=tua_chiave_qui



# Recupera la chiave API
API_KEY="AIzaSyARm012hn274AeO24zGrTVCwf_qVq8ZNf8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') 
if not api_key: # type: ignore
    print("❌ Errore: non hai impostato GOOGLE_API_KEY nel file .env")
    print("Crea un file .env con il contenuto: GOOGLE_API_KEY=la_tua_chiave")
    exit(1)


# ============================================================
# Esempio 3: Analisi di dati (es. lista ingredienti)
print("\n--- Esempio 3: Analisi ingredienti ---")
ingredienti = ["pomodori", "mozzarella", "basilico", "olio d'oliva"]
prompt = f"Data questa lista di ingredienti: {ingredienti}. Che piatto consiglieresti di preparare? Rispondi in italiano."
response = model.generate_content(prompt)
print(f"🤖 IA consiglia: {response.text}")



# ============================================================
# Esempio 5: Gestione errori
print("\n--- Esempio 5: Gestione errori ---")
try:
    response = model.generate_content("")  # Prompt vuoto per generare errore
except Exception as e:
    print(f"❌ Errore gestito: {e}")

print("\n✅ Tutorial completato!")



#ciao leo qua
#xxxxxxxxxxxx