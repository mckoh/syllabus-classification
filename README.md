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
