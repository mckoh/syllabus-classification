"""
Syllabus Classification Functions

Author: Michael Kohlegger
Date: November 2025
"""


from json import loads
from ollama import chat
from datetime import datetime as dt
from requests import get
from transformers import AutoTokenizer
import json
import re

from json import loads
from ollama import chat
from difflib import SequenceMatcher
from typing import Literal
from difflib import get_close_matches

from .templates import Extraction
from .constant import EXTRACT_TEMPERATURE, EXTRACTION_PROMPT
from .constant import LANG_MODEL, INFERENCE_LENGTH, CONTEXT_SIZE


def get_framework(reference="digicomp3-0") -> str:
    """Retrieves DigiComp Framework from github.

    :param reference: The compentence framework to load
    :type reference: str
    :default reference: digicomp3-0
    :return: DigiComp framework as json
    :rtype: str
    """

    url = f"https://raw.githubusercontent.com/mckoh/{reference}/refs/heads/main/digital_compenteces.json"
    json = get(url).content.decode("utf-8")
    json = json.replace("\n ", "").replace("\t ", "")
    json = json.replace("\n", "").replace("\t", "")
    json = json.strip()
    json = " ".join(json.split())
    return json


def extract_valid_names(framework: str) -> list[str]:
    """Forms a list of valid competences from a dictiona

    :param framework: The competence framework
    :type framework: str
    :returns: List of competence names
    :rtype: list of str
    """
    nested_list = [[c["Competence Title"] for c in i["Competences"]] for i in loads(framework)]
    return [item for sublist in nested_list for item in sublist]


def is_valid_evidence(evidence: str, source_text: str, threshold: float = 0.80) -> bool:
    """Validates evidence strings against the source text.

    :param evidence: Found evidence reported by a model
    :type evidence: str
    :param source_text: The original text that the evidence was extracted from
    :type source_text: str
    :param threshold: The threshold value used to check similarity
    :type threshold: float
    :returns: Boolean flag
    :rtype: bool
    """

    # Clean the text
    norm_evidence = " ".join(evidence.lower().split())
    norm_source = " ".join(source_text.lower().split())

    # Check if there is a string to compare
    if not norm_evidence:
        return False

    # 1. Fast-Path: Exakter Treffer (spart Rechenzeit)
    if norm_evidence in norm_source:
        return True

    # 2. Fuzzy-Matching via Sliding Window
    ev_len = len(norm_evidence)
    src_len = len(norm_source)

    if ev_len > src_len:
        return SequenceMatcher(None, norm_evidence, norm_source).ratio() >= threshold

    # Fenster etwas größer wählen (+15 %), falls das Modell beim Zitieren ein Wort ausgelassen hat
    window_size = min(src_len, int(ev_len * 1.15))
    step = max(1, ev_len // 4)  # Viertel-Schritte machen die Suche schnell

    best_ratio = 0.0
    for i in range(0, src_len - window_size + 1, step):
        window = norm_source[i : i + window_size]
        # find_longest_match prüft lokal, wie gut das Zitat in dieses Textfenster passt
        matcher = SequenceMatcher(None, norm_evidence, window)
        # Verhältnis der übereinstimmenden Zeichen zur Länge des Zitats
        matched_chars = sum(block.size for block in matcher.get_matching_blocks())
        ratio = matched_chars / ev_len

        if ratio >= threshold:
            return True
        if ratio > best_ratio:
            best_ratio = ratio

    return False


def is_valid_competence(competence: str, valid_competences: list[str], threshold: float = 0.85) -> str | None:
    """Checks if an extracted competence is a valid competence label.

    Checks if raw_name that has been extracted by a language model
    is a true valid competence from the competence framework. The check
    also justifies minor differences (e.g. 1.1) in the extracted name.
    If the extraction is plausible, it will return the exact name from the
    framework.

    :param competence: The extracted competence.
    :type competence: str
    :param valid_competences: The valid competence names
    :type valid_competences: list of str
    :param threshold: The cutoff value used for similarity matching
    :type threshold: float
    :default threshold: 0.85
    :returns: Valid competence Name
    :rtype: str or None
    """
    if not competence or not valid_competences:
        return None

    # 1. Exakter Treffer (Fast-Path)
    if competence in valid_competences:
        return competence

    # Lookup-Dictionary: bereinigter Name (klein, ohne "1.1 ") -> Originalname aus JSON
    cleaned_to_canonical = {
        re.sub(r"^\d+(\.\d+)*\s*", "", name).strip().lower(): name
        for name in valid_competences
    }
    cleaned_input = re.sub(r"^\d+(\.\d+)*\s*", "", competence).strip().lower()

    # 2. Exakter Treffer nach Bereinigung von Groß-/Kleinschreibung und Nummerierung
    if cleaned_input in cleaned_to_canonical:
        return cleaned_to_canonical[cleaned_input]

    # 3. Fuzzy-Matching für Tippfehler (z. B. "Browsing, searching and filtering data")
    matches = get_close_matches(
        cleaned_input,
        list(cleaned_to_canonical.keys()),
        n=1,
        cutoff=threshold
    )
    if matches:
        return cleaned_to_canonical[matches[0]]

    # Kein ausreichender Treffer -> erfundenes Label verwerfen
    return None


def extract(text: str) -> Extraction:
    framework = get_framework()
    valid_names = extract_valid_names(framework)
    framework_str = framework if isinstance(framework, str) else json.dumps(framework, ensure_ascii=False, indent=2)

    system_content = (
        f"{EXTRACTION_PROMPT}\n\n"
        f"KOMPETENZRAHMEN (Englisch):\n```json\n{framework_str}\n```"
    )

    user_content = (
        f"KURSBESCHREIBUNG (Deutsch):\n```text\n{text}\n```"
    )

    resp = chat(
        model=LANG_MODEL,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
        format=Extraction.model_json_schema(),
        options={
            "temperature": EXTRACT_TEMPERATURE,
            "num_ctx": CONTEXT_SIZE,
            "num_predict": INFERENCE_LENGTH
        }
    )

    result = Extraction.model_validate_json(resp.message.content)

    verified_competences = []
    seen_names = set()

    for c in result.competences:
        # Guardrail 1: Steht das Zitat wirklich im Kurstext?
        if not is_valid_evidence(c.evidence, text, threshold=0.80):
            continue

        # Guardrail 2: Existiert die Kompetenz im Rahmen (inkl. Auto-Korrektur)?
        canonical_name = is_valid_competence(c.name, valid_names, threshold=0.85)
        if not canonical_name:
            continue

        # Duplikate vermeiden (falls 2 Textstellen auf dieselbe Kompetenz zeigen)
        if canonical_name not in seen_names:
            c.name = canonical_name  # Tippfehler mit dem exakten JSON-Wert überschreiben
            verified_competences.append(c)
            seen_names.add(canonical_name)

    result.competences = verified_competences
    return result
