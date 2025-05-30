# Installation (einmalig ausführen)
# pip install bert-score rouge-score nltk

from bert_score import score
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# === Dateipfade anpassen ===
system_output_path = "system_output.txt"
musterloesung_path = "musterloesung.txt"

# === Texte einlesen ===
with open(system_output_path, "r", encoding="utf-8") as f:
    system_output = f.read().strip()

with open(musterloesung_path, "r", encoding="utf-8") as f:
    musterloesung = f.read().strip()

# === BERTScore berechnen ===
P, R, F1 = score([system_output], [musterloesung], lang="de", verbose=False)

# === ROUGE berechnen ===
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
rouge = scorer.score(musterloesung, system_output)

# === BLEU berechnen ===
smoothie = SmoothingFunction().method4
bleu = sentence_bleu([musterloesung.split()], system_output.split(), smoothing_function=smoothie)

# === Ergebnisse ausgeben ===
print("📊 Evaluationsergebnisse:")
print(f"BERTScore F1:  {F1[0].item():.4f}")
print(f"ROUGE-1 F1:    {rouge['rouge1'].fmeasure:.4f}")
print(f"ROUGE-L F1:    {rouge['rougeL'].fmeasure:.4f}")
print(f"BLEU Score:    {bleu:.4f}")
