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
    inverse_file = InverseFile()
    try:
        f = open(filename)
        json_data = json.loads(f.read())
        for term in json_data["terms"]:
            for doc in term["post_list"]:
                inverse_file.add_document(term["term"], doc["id"], doc["tf"])
        print(inverse_file)
        #TODO finish
    except:
        print("An error has ocurring retrieving the inverse file")

