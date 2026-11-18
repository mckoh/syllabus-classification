from os import getenv

# Models in Use
LANG_MODEL = "llama3.1:latest"
EMBED_MODEL = "qwen3-embedding:0.6b"

# Model Parameters
CONTEXT_SIZE = 8192
EXTRACT_TEMPERATURE = 0
INFERENCE_TEMPERATUR = 0.2

EXTRACTION_PROMPT = """Extrahiere aus der Kursbeschreibung unter Zuhilfenahme des
gegebenen Kompetenzrasters jene digitalen Kompetenzen, die vom gegeben Kurs
entwickelt werden. Beachte dabei nicht das Niveau der Kompetenzentwicklung,
sondern nur entwickelt/nicht entwickelt. Gib die extrahierten Kompetenzen
als Liste aus. Benutze ausschließlich die Kompetenz-Bezeichnungen aus dem
Raster. Erfinde nichts dazu."""