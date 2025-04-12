import pandas as pd
import re

INPUT_FILE = 'all_triples.csv'
OUTPUT_FILE = 'all_triples_clean.csv'

# Mapping für vereinheitlichte Prädikate
PREDICATE_MAPPING = {
    'unter Strafe gestellt': 'verboten',
    'unterliegt': 'verboten',
    'beurteilung erfolgt': 'erfolgt',
    'zeitlich begrenzt': 'gilt in Zeitraum'
}

# Prädikate die komplett entfernt werden sollen
REMOVE_PREDICATES = [
    'keine Angabe',
    'unbekannt',
    'nicht definiert'
]

def clean_text(text):
    if pd.isna(text):
        return ""

    # Entferne Nummerierungen: "1. Tat" -> "Tat"
    text = re.sub(r'^\d+\.\s*', '', text)

    # Entferne Zusätze in Klammern: "Gesetz (StGB)" -> "StGB"
    text = re.sub(r'\(.*?\)', '', text)

    # Entferne mehrfach Whitespaces
    text = re.sub(r'\s+', ' ', text)

    # Unbekannte entfernen / ersetzen
    text = text.replace('Unbekannter Täter', 'Täter unbekannt')
    text = text.replace('unbekannt', '')

    return text.strip()

def map_predicate(pred):
    pred_clean = pred.lower().strip()
    if pred_clean in PREDICATE_MAPPING:
        return PREDICATE_MAPPING[pred_clean]
    return pred

def main():
    df = pd.read_csv(INPUT_FILE)

    cleaned_triples = []

    for idx, row in df.iterrows():
        subj = clean_text(row['subject'])
        pred = clean_text(row['predicate'])
        obj = clean_text(row['object'])

        pred = map_predicate(pred)

        # Entferne unerwünschte Prädikate
        if pred.lower() in REMOVE_PREDICATES:
            continue

        # Nur speichern wenn alle drei Werte da sind
        if subj and pred and obj:
            cleaned_triples.append([subj, pred, obj, row['artikel_id'], row['artikel_nummer']])

    # DataFrame erstellen
    clean_df = pd.DataFrame(cleaned_triples, columns=['subject', 'predicate', 'object', 'artikel_id', 'artikel_nummer'])

    # Doppelte Triples entfernen
    clean_df.drop_duplicates(inplace=True)

    # Speichern
    clean_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f'✔️ Cleaning abgeschlossen: {len(clean_df)} Triples gespeichert in {OUTPUT_FILE}')

if __name__ == "__main__":
    main()
