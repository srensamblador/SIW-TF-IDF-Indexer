import json
from inverse_file import InverseFile


def dump_inverse_file(filename, inverse_file):
    json_data = json.dumps(inverse_file.to_json())
    try:
        f = open(filename, "w")
        f.write(json_data)
    except:
        print("An error has occuring serializing the inverse file")


def load_inverse_file(filename):
    """
    Reads an inverse file fromt he disk and returns an InverseFile object
    :param filename: input file
    :return: InverseFile object
    """
    inverse_file = InverseFile()
    try:
        f = open(filename)
        json_data = json.loads(f.read())
        for term in json_data["terms"]:
            for doc in term["post_list"]:
                inverse_file.add_document(term["term"], doc["id"], doc["tf"])
            inverse_file.set_idf(term["term"], term["idf"])
        return inverse_file
    except:
        print("An error has ocurring retrieving the inverse file")

