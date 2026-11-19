from os import getenv

# Models in Use
LANG_MODEL = "llama3.1:latest"
EMBED_MODEL = "qwen3-embedding:0.6b"

# Model Parameters
CONTEXT_SIZE = 8192
EXTRACT_TEMPERATURE = 0.1  # 0 lets SMLs often go into greedy endless inferencing loops
INFERENCE_TEMPERATUR = 0.2
INFERENCE_LENGTH = 1024

EXTRACTION_PROMPT = """
# AUFGABE
Analysiere die deutsche Kursbeschreibung und prüfe, welche Kompetenzen aus dem englischen DigComp-Kompetenzrahmen darin tatsächlicher Lerninhalt sind.

# KRITISCHE REGELN
1. **ZITAT-PFLICHT AUS DEM KURSTEXT:** Das Feld `evidence` MUSS ein exaktes, wörtliches Zitat aus der **Kursbeschreibung** (dem deutschen Text) sein. Kopiere NIEMALS Text oder Nummern (wie "1.1 ...") aus dem Kompetenzrahmen in das Feld `evidence`! Kopiere einen exakten Substring 1:1 aus dem Kurstext, ohne ein einziges Wort zu verändern
2. **LEERE LISTE BEI KEINEM TREFFER:** Wenn der Kurs keine digitalen Kompetenzen vermittelt (z. B. rein analoge Methoden wie Flipcharts, Moderation ohne Technik) oder explizit "ohne digitale Medien" arbeitet, gib zwingend eine leere Liste `competences: []` zurück.
3. **KEINE SPEKULATION:** Ordne eine Kompetenz nur zu, wenn sie aktiv gelehrt oder angewendet wird.

# BEISPIEL FÜR EINEN NICHT-DIGITALEN KURS
Kursbeschreibung: "Lehrziele: Rhetorik und Körpersprache trainieren. Lehrinhalt: Atemübungen, freies Sprechen im Raum."
Korrekte Ausgabe:
{
  "course_name": "Rhetorik und Körpersprache",
  "competences": []
}"""

AGENTS = [
    {
        "name": "Didaktik-Experte",
        "description": "Bewertet die Lehrveranstaltung hinsichtlich didaktischer Qualität, Methodeneinsatz und Lernzielorientierung. Achtet besonders darauf, ob die Lehrmethoden zum Inhalt und zur Zielgruppe passen."
    },
    {
        "name": "Studierendenvertreter",
        "description": "Analysiert die Beschreibung aus Sicht der Studierenden. Prüft, ob die Inhalte verständlich formuliert sind, ob die Erwartungen realistisch sind und ob die Veranstaltung einen klaren Mehrwert für das Studium bietet."
    },
    {
        "name": "Forschungsorientierter Gutachter",
        "description": "Fokussiert sich auf den wissenschaftlichen Anspruch der Veranstaltung. Bewertet, ob aktuelle Forschung integriert wird, ob kritisches Denken gefördert wird und ob die Inhalte zur Forschungskompetenz beitragen."
    },
    {
        "name": "Berufsbezogener Evaluator",
        "description": "Beurteilt die Lehrveranstaltung im Hinblick auf berufliche Relevanz. Untersucht, ob praxisnahe Kompetenzen vermittelt werden und ob die Inhalte auf typische Berufsfelder vorbereiten."
    },
    {
        "name": "Interdisziplinärer Analyst",
        "description": "Prüft, ob die Lehrveranstaltung Bezüge zu anderen Fachbereichen herstellt und interdisziplinäres Denken fördert. Achtet auf Querverbindungen und Transfermöglichkeiten."
    },
    {
        "name": "Sprach- und Stilprüfer",
        "description": "Analysiert die sprachliche Qualität der Beschreibung. Achtet auf Klarheit, Verständlichkeit, konsistente Terminologie und angemessenen akademischen Stil."
    },
    {
        "name": "Inklusionsbeauftragter",
        "description": "Bewertet die Lehrveranstaltung hinsichtlich Barrierefreiheit und Diversität. Prüft, ob unterschiedliche Lernbedürfnisse berücksichtigt werden und ob die Veranstaltung inklusiv gestaltet ist."
    },
    {
        "name": "Curriculum-Manager",
        "description": "Untersucht die Passung der Lehrveranstaltung zum Gesamtcurriculum. Achtet darauf, ob die Inhalte sinnvoll eingebettet sind, ob sie Anschlussfähigkeit bieten und ob sie zur Studienstruktur passen."
    },
    {
        "name": "Technologie-Scout",
        "description": "Bewertet den Einsatz digitaler Tools und Technologien. Prüft, ob innovative Lehrformate genutzt werden und ob die Veranstaltung medienpädagogisch sinnvoll gestaltet ist."
    },
    {
        "name": "Qualitätssicherungsbeauftragter",
        "description": "Fokussiert sich auf formale Kriterien wie Lernziele, Prüfungsformate, Workload und Transparenz. Achtet auf Konsistenz mit hochschuldidaktischen Standards und Akkreditierungsvorgaben."
    }
]