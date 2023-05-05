from linkml_runtime.utils.schemaview import SchemaView
import os
import requests
import csv
from typing import List

INFORES_TSV = os.path.join('../infores_catalog_nodes.tsv')


def is_valid_urls(url: str) -> bool:
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(response.status_code)
            return False
        return True
    except requests.exceptions.RequestException:
        print("Exception:" + url)
        return False


class InformationResource:

    def __init__(self) -> None:
        self.sv = SchemaView('../biolink-model.yaml')

    def dump(self):
        raise NotImplementedError

    def validate(self):
        infores_map = {}
        with open(INFORES_TSV, 'r') as tsv_file:
            reader = csv.reader(tsv_file, delimiter='\t')
            for line in reader:
                print(line)
                if line[2] == 'id' or line[3] == '':
                    continue
                if line[2] == 'infores:athena' \
                        or line[0] == 'deprecated' \
                        or line[2] == 'infores:isb-incov' \
                        or is_valid_urls(line[3]):
                    infores_map[line[2]] = {
                        "status": line[0],
                        "name": line[1],
                        "url": line[3],
                        "synonyms": line[4],
                        "description": line[5],
                    }
                else:
                    print("Invalid infores URL:" + line[3] + " for " + line[2])
                    raise ValueError("Invalid infores URL")


if __name__ == "__main__":
    InformationResource().validate()
