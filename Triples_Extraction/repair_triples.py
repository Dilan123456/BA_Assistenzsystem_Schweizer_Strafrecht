import pandas as pd
import re

INPUT_FILE = 'all_triples_clean.csv'
OUTPUT_FILE = 'all_triples_repaired.csv'

# Mapping Prädikate
PREDICATE_MAPPING = {
    'unter Strafe gestellt': 'verboten',
    'begangen von': 'begeht',
    'milder als': 'ist milder als',
    'unterliegt': 'verboten',
    'erfolgt nach': 'erfolgt',
}

# Triples die gedreht werden müssen
INVERT_PREDICATES = ['begangen von']

def clean_condition(obj):
    # Wenn Objekt ein ganzer Satz ist → reduzieren
    if 'unter Strafe gestellt' in obj:
        return 'Tat ist verboten'
    return obj

def repair_triple(subj, pred, obj):
    pred = pred.strip().lower()

    # Mapping Prädikate
    for key, val in PREDICATE_MAPPING.items():
        if pred == key.lower():
            pred = val

    # Prädikat Inversion
    if pred in INVERT_PREDICATES:
        subj, obj = obj, subj
        pred = 'begeht'

    # "Gesetz" → "StGB"
    obj = obj.replace('Gesetz', 'StGB')
    subj = subj.replace('Gesetz', 'StGB')

    # Conditions bereinigen
    obj = clean_condition(obj)

    return subj.strip(), pred.strip(), obj.strip()

def main():
    df = pd.read_csv(INPUT_FILE)

    repaired_triples = []

    for idx, row in df.iterrows():
        subj, pred, obj = row['subject'], row['predicate'], row['object']
        artikel_id, artikel_nummer = row['artikel_id'], row['artikel_nummer']

        subj, pred, obj = repair_triple(subj, pred, obj)

        repaired_triples.append([subj, pred, obj, artikel_id, artikel_nummer])

    repaired_df = pd.DataFrame(repaired_triples, columns=['subject', 'predicate', 'object', 'artikel_id', 'artikel_nummer'])

    repaired_df.drop_duplicates(inplace=True)

    repaired_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f'✔️ Repair abgeschlossen: {len(repaired_df)} Triples gespeichert in {OUTPUT_FILE}')

if __name__ == "__main__":
    main()
