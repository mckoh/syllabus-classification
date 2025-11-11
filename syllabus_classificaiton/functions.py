"""
Syllabus Classification Functions

Author: Michael Kohlegger
Date: November 2025
"""


from json import loads
from ollama import chat
from datetime import datetime as dt
from requests import get
from .prompt import prompt


def get_framework() -> str:
    """Retrieves DigiComp 2.2 data from the web.
    :return: DigiComp framework as json
    :rtype: str
    """
    url = "https://raw.githubusercontent.com/mckoh/digicomp2-2/refs/heads/main/competences.json"
    json = get(url).content.decode("utf-8")
    json = json.replace("\n ", "").replace("\t ", "")
    json = json.replace("\n", "").replace("\t", "")
    json = json.strip()
    for _ in range(10):
        json = json.replace("  ", " ")
    return json


def debug_print(start) -> None:
    """Adds a print statement to a given Function.
    :return: None
    """
    time = dt.now() - start
    print(f"--> Time needed for this step: {time}\n")


def load_curriculum(file_path, verbose:int=1):
    """Loads the content of a curriculum JSON
    :param file_path: The file to be loaded
    :type file_path: str
    :param verbose: Set to 1 to activate debug printing
    :type verbose: int
    :return: The curriculum as dictionary
    :rtype: dict
    """

    start = dt.now()

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    if verbose > 0:
        print(f"Loading curriculum data from {file_path}.")
        debug_print(start)
    return loads(content)


def transform_curriculum(json_curriculum:dict, verbose:int=1) -> str:
    """Concatenates dictionary values into string.
    :param json_curriculum: Curriculum data as dictionary
    :type json_curriculum: dict
    :param verbose: Set to 1 to activate debug printing
    :type verbose: int
    :return: Curriculum as string
    :rtype: str
    """

    start = dt.now()

    output = ""
    for key, value in json_curriculum.items():
        output += str(key) + ": " + str(value) + "\n"

    if verbose > 0:
        print(f"Transforming curriculum data to String format.")
        debug_print(start)
    return output


def classify_curriculum(txt_curriculum:str, verbose:int=1, framework=None) -> str:
    """Classifies a curriculum according to DigiComp2.2.
    :param txt_curriculum: Curriculum data as string
    :type txt_curriculum: str
    :param verbose: Set to 1 to activate debug printing
    :type verbose: int
    return: Classification of curriculum
    rtype: str
    """

    start = dt.now()

    if framework is not None:
        print("Use this framework:", framework)
        txt_framework = framework
    else:
        print("Using default framework.")
        txt_framework = get_framework()

    content = prompt.replace("**lvbeschreibung**", txt_curriculum)
    content = content.replace("**digicompraster**", txt_framework)

    response = chat(
        model='digicomp',
        messages=[{
        'role': 'user',
        'content': content}],
        stream=False,
    )

    if verbose > 0:
        print(f"Classifying curriculum data.")
        debug_print(start)
    return response.message.content


def save_classification(output_path:str, txt_classification:str, verbose:int=1) -> bool:
    """Saves classification result to disk.
    :param output_path: Path to save to including file name
    :type output_path: str
    :param txt_classification: Curriculum classification
    :type txt_classification: str
    :param verbose: Set to 1 to activate debug printing
    :type verbose: int
    :return: Boolean success flag
    :rtype: bool
    """

    start = dt.now()

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(txt_classification)

    if verbose > 0:
        print(f"Saving classification to {output_path}.")
        debug_print(start)
    return True