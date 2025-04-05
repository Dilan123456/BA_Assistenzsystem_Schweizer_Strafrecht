import xml.etree.ElementTree as ET
import pandas as pd

# Lade die XML-Datei
xml_file = "SR-311.0-01012025-DE.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Namespace definieren
namespace = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}

# Liste zur Speicherung der Artikel
gesetze = []

# Hilfsfunktion zum Extrahieren von Text aus Listen
def extract_blocklist(blocklist_element):
    texts = []
    # Einführungstext
    list_intro = blocklist_element.find("akn:listIntroduction", namespace)
    if list_intro is not None and list_intro.text:
        texts.append(list_intro.text.strip())

    for item in blocklist_element.findall("akn:item", namespace):
        num = item.find("akn:num", namespace)
        p = item.find("akn:p", namespace)

        num_text = num.text.strip() if num is not None and num.text else ""
        p_text = p.text.strip() if p is not None and p.text else ""

        combined = f"{num_text} {p_text}".strip()
        if combined:
            texts.append(combined)

    return texts


# Durch alle Artikel
for artikel in root.findall(".//akn:article", namespace):
    artikel_id = artikel.get("eId", "Unbekannt")

    # Artikelnummer
    artikel_num_element = artikel.find(".//akn:num", namespace)
    if artikel_num_element is not None:
        b_element = artikel_num_element.find(".//akn:b", namespace)
        if b_element is not None and b_element.text:
            artikel_nummer = b_element.text.strip()
        elif artikel_num_element.text:
            artikel_nummer = artikel_num_element.text.strip()
        else:
            artikel_nummer = "Unbekannt"
    else:
        artikel_nummer = "Unbekannt"


    # Text sammeln
    texte = []

    # Alle Paragraphen
    for para in artikel.findall(".//akn:paragraph", namespace):
        # Text direkt in <p>
        for p in para.findall(".//akn:content/akn:p", namespace):
            if p.text:
                texte.append(p.text.strip())

        # Blocklisten
        for blocklist in para.findall(".//akn:content/akn:blockList", namespace):
            texte.extend(extract_blocklist(blocklist))

    artikel_text = " ".join(texte) if texte else "Kein Inhalt"
    gesetze.append({"Artikel-ID": artikel_id, "Artikel": artikel_nummer, "Text": artikel_text})

# Speichern als CSV
df = pd.DataFrame(gesetze)
csv_filename = "schweizer_strafrecht_komplett.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8")
print(f"Scraping abgeschlossen! Die Daten wurden als '{csv_filename}' gespeichert.")
