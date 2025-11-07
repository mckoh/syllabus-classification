from json import loads

def load_curriculum(file_name):
    """Loads the content of a curriculum JSON
    :param file_name: The file to be loaded
    :return: The curriculum as dictionary
    :rtype: dict
    """
    with open(file_name, "r") as file:
        content = file.read()
    return loads(content)

def transform_curriculum(dictionary):
    """Concatenates dictionary values into string.
    :param syllabus_dictionary: The dictionary with data
    :return: Curriculum as string
    :rtype: str
    """
    output = ""
    for key, value in dictionary.items():
        output += str(key) + ": " + str(value) + "\n"
    return output