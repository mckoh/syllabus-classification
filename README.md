# Syllabus Classification Demonstrator

Dieses Projekt demonstriert die automatische Klassifikation von Kurs-Syllabi mithilfe von Large Language Models (LLMs). Ziel ist es, Bildungsinhalte effizient zu analysieren und zu kategorisieren – ein wertvoller Beitrag zur digitalen Transformation im Bildungsbereich.

## 🚀 Features

Klassifikation von Kursbeschreibungen basierend auf Textinhalten
Einsatz moderner LLMs zur semantischen Analyse
Einfache Erweiterbarkeit für verschiedene Klassifikationsschemata
Minimalistisches Setup für schnelle Demonstrationen

## 🧠 Motivation

Kurs-Syllabi enthalten wertvolle Informationen über Lernziele, Inhalte und Kompetenzen. Die manuelle Analyse ist jedoch zeitaufwendig und fehleranfällig. Mit diesem Demonstrator zeigst du, wie LLMs diese Aufgabe automatisieren und strukturierte Einblicke liefern können.

## Use

Prepare code execution by pulling the `llama3.1:8b` model using `ollama` by proceeding as follows:

```bash
ollama pull llama3.1:8b
```

After that, setup the agent that is intended to do classification. This is done by executing the following on your terminal:

```bash
ollama create digicomp -f ./Modelfile
```

Finally, you can rely on this agent doing your classification in python. This is a minimal code example that you can use:

```python
from syllabus_classificaiton.functions import load_curriculum
from syllabus_classificaiton.functions import transform_curriculum
from syllabus_classificaiton.functions import classify_curriculum
from syllabus_classificaiton.functions import save_classification
from os.path import join

src_file = "01_machine_learning.json"
dst_file = "01_machine_learning.md"

in_path = join("input", src_file)
out_path = join("output", dst_file)

x = load_curriculum(file_path=in_path)
x = transform_curriculum(json_curriculum=x)
c = classify_curriculum(txt_curriculum=x)
s = save_classification(output_path=out_path, txt_classification=c)
```

## 🧭 Kontext Token Problem

Die vollständige Klassifizierung eines Curriculums dauert in etwa 0:11:51 mit einer Kontext-Länge von 4096 tokens. Für die Klassifikation von Syllabus-Dokumenten benötigen wir aber deutlich mehr Kontext (Prompt + Curriculum + Framework kommen gemeinsam auf eine Länge von ~ 80.000 Worten).

Konversion from words to tokens (Daumenregel mit 130 % Faktor):

$$80.000 \cdot 1.3 = 104.000$$

Darum  wurde die Kontext-Länge im ModelFile während eines Experiments auf 90.000 angepasst. Damit dauert die Klassifikation einer LV mit einer `RTX 2080 Ti` (GPU) aber bereits weit länger als ein Stunde.

Um Syllabi im großen Stil zu klassifizieren muss demnach auf eine leistungsfähigere Infrastruktur umgestiegen werden. Hier einige Benchmarks aus den Versuchen zur Syllabusklassifikation:

Kontext size | Runtime per LV | Runtime für DSIA
-- | -- | --
4.000 | ~0.25 min | 11 min
20.000 | ~1 min | 180 min
80.000 | ~60+ min | zu lange

## 💡 Lösung RAG

Könnte dieses Problem gelöst werden, indem der Framework-Kontext geteilt und über einen Vektor-Space bereitgestellt wird um nur die relevanten Kompetenzen zu verwenden.
