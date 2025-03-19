import xml.etree.ElementTree as ET
import pandas as pd

# Lade die XML-Datei
xml_file = "SR-311.0-01012025-DE.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Namespace der XML definieren (wichtig für die Suche!)
namespace = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}

# Liste zur Speicherung der Artikel
gesetze = []

# Durch alle <article>-Elemente navigieren
for artikel in root.findall(".//akn:article", namespace):
    artikel_id = artikel.get("eId", "Unbekannt")  # Artikel-ID aus Attribut eId

    artikel_num_element = artikel.find(".//akn:num", namespace)
    if artikel_num_element is not None:
        artikel_b_element = artikel_num_element.find(".//akn:b", namespace)
        if artikel_b_element is not None and artikel_b_element.text:
            artikel_nummer = artikel_b_element.text.strip()  # Text aus <b> holen
        else:
            artikel_nummer = artikel_num_element.text.strip()  # Falls kein <b>, dann <num>-Text nutzen
    else:
        artikel_nummer = "Unbekannt"  # Falls kein <num>-Element existiert

    # Paragraphen extrahieren
    absatz_list = [p.text.strip() for p in artikel.findall(".//akn:content/akn:p", namespace) if p.text]
    artikel_text = " ".join(absatz_list) if absatz_list else "Kein Inhalt"

    gesetze.append({"Artikel-ID": artikel_id, "Artikel": artikel_nummer, "Text": artikel_text})

# Speichern als CSV
df = pd.DataFrame(gesetze)
csv_filename = "schweizer_strafrecht.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8")

print(f"Scraping abgeschlossen! Die Daten wurden als '{csv_filename}' gespeichert.")
