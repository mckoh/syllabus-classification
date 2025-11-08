"""
Syllabus Classification Functions

Author: Michael Kohlegger
Date: November 2025
"""


from json import loads
from ollama import chat
from datetime import datetime as dt
from .prompt import prompt


def debug_print(start):
    time = dt.now() - start
    print(f"--> Time needed for this step: {time}\n")


def load_curriculum(file_path):
    """Loads the content of a curriculum JSON
    :param file_path: The file to be loaded
    :return: The curriculum as dictionary
    :rtype: dict
    """

    start = dt.now()
    print(f"Loading curriculum data from {file_path}.")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    debug_print(start)
    return loads(content)


def transform_curriculum(json_curriculum:dict) -> str:
    """Concatenates dictionary values into string.
    :param json_curriculum: Curriculum data as dictionary
    :type json_curriculum: dict
    :return: Curriculum as string
    :rtype: str
    """

    start = dt.now()
    print(f"Transforming curriculum data to String format.")

    output = ""
    for key, value in json_curriculum.items():
        output += str(key) + ": " + str(value) + "\n"

    debug_print(start)
    return output


def classify_curriculum(txt_curriculum:str) -> str:
    """Classifies a curriculum according to DigiComp2.2.
    :param txt_curriculum: Curriculum data as string
    :type txt_curriculum: str
    return: Classification of curriculum
    rtype: str
    """

    start = dt.now()
    print(f"Classifying curriculum data.")

    response = chat(
        model='digicomp',
        messages=[{
        'role': 'user',
        'content': prompt + txt_curriculum}],
        stream=False,
    )

    debug_print(start)
    return response.message.content


def save_classification(output_path:str, txt_classification:str) -> bool:
    """Saves classification result to disk.
    :param output_path: Path to save to including file name
    :type output_path: str
    :param txt_classification: Curriculum classification
    :type txt_classification: str
    :return: Boolean success flag
    :rtype: bool
    """

    start = dt.now()
    print(f"Saving classification to {output_path}.")

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(txt_classification)

    debug_print(start)
    return True