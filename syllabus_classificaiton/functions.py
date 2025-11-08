"""
Syllabus Classification Functions

Author: Michael Kohlegger
Date: November 2025
"""


from json import loads
from ollama import chat
from .prompt import prompt


def load_curriculum(file_name):
    """Loads the content of a curriculum JSON
    :param file_name: The file to be loaded
    :return: The curriculum as dictionary
    :rtype: dict
    """
    with open(file_name, "r") as file:
        content = file.read()
    return loads(content)


def transform_curriculum(json_curriculum:dict) -> str:
    """Concatenates dictionary values into string.
    :param json_curriculum: Curriculum data as dictionary
    :type json_curriculum: dict
    :return: Curriculum as string
    :rtype: str
    """
    output = ""
    for key, value in json_curriculum.items():
        output += str(key) + ": " + str(value) + "\n"
    return output


def classify_curriculum(txt_curriculum:str) -> str:
    """Classifies a curriculum according to DigiComp2.2.
    :param txt_curriculum: Curriculum data as string
    :type txt_curriculum: str
    return: Classification of curriculum
    rtype: str
    """
    response = chat(
        model='digicomp',
        messages=[{
        'role': 'user',
        'content': prompt + txt_curriculum}],
        stream=False,
    )
    return response.message.content
