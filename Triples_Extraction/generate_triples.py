import requests
import csv
import re
import time
import pandas as pd

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

PROMPT_TEMPLATE = """
Du bist ein juristischer NLP-Assistent. Extrahiere Triples im Knowledge Graph Format.

Format GENAU: Subject | Predicate | Object

Regeln:
- Täter begeht immer Tat
- Die Tat heisst immer: Verbrechen oder Vergehen
- Zeitpunkte immer eigenes Triple:
Beispiel: Tat | Zeitpunkt | vor Inkrafttreten
- Beurteilung ist eigene Entität. Prädikat: erfolgt
Beispiel: Beurteilung | erfolgt | nach Inkrafttreten
- Das Gesetz heisst: StGB
- Art. 2 ist KEIN Akteur und darf NIEMALS Subjekt sein
- Das Prädikat "wird angewendet auf" gilt nur für: StGB | wird angewendet auf | Täter
- Bedingungen immer als eigene Triples:
1. StGB | ist milder als | vorheriges Gesetz
2. Anwendung | gilt wenn | StGB ist milder
- KEINE Bedingungen im Objekt
- KEINE Klammern
- KEINE Nummerierungen

Gesetzesartikel:
\"\"\"{article_text}\"\"\"
"""

def call_ollama(prompt):
    for attempt in range(3):
        try:
            response = requests.post(OLLAMA_API_URL, json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            })
            if response.status_code == 200:
                return response.json()["response"]
            else:
                time.sleep(5)
        except Exception:
            time.sleep(5)
    return None

def extract_triples(text):
    triples = []
    lines = text.split("\n")
    for line in lines:
        if "|" in line:
            parts = [x.strip() for x in line.split("|")]
            if len(parts) == 3:
                triples.append(parts)
    return triples

def main():
    df = pd.read_csv('../Data_Scraping/schweizer_strafrecht_komplett.csv')

    with open("all_triples.csv", mode="w", newline='', encoding="utf-8") as csv_file, open("triples_log.txt", mode="w", encoding="utf-8") as log_file:
        writer = csv.writer(csv_file)
        writer.writerow(["subject", "predicate", "object", "artikel_id", "artikel_nummer"])

        for idx, row in df.iterrows():
            artikel_id = row["Artikel-ID"]
            artikel_nummer = row["Artikel"]
            artikel_text = row["Text"]

            prompt = PROMPT_TEMPLATE.format(article_text=artikel_text)
            log_file.write(f"Verarbeite {artikel_id} - {artikel_nummer}\n")

            result = call_ollama(prompt)

            if result:
                triples = extract_triples(result)
                if triples:
                    for triple in triples:
                        writer.writerow(triple + [artikel_id, artikel_nummer])
                else:
                    log_file.write(f"KEINE Triples gefunden in {artikel_id}\n")
            else:
                log_file.write(f"FEHLER bei {artikel_id} nach 3 Versuchen\n")

    print("✔️ Verarbeitung abgeschlossen.")

if __name__ == "__main__":
    main()
