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


def get_framework(reference="digicomp3-0") -> str:
    """Retrieves DigiComp 2.2 data from the web.
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