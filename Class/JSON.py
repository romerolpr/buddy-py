import json, re
from os import listdir

class JSON:

    def __init__(self):
        super(JSON, self).__init__()

    def write(self, data, pathfile, method="w"):
        with open(pathfile, method, encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def read(self, pathfile, method="r"):
        with open(pathfile, method, encoding="utf-8") as f:
            dados = f.read()
            return json.loads(dados)

    def list(self, pathfile, ext="json"):
        listFiles = listdir(pathfile)
        for keys, file in enumerate(listFiles):
            if ext not in file:
                del listFiles[keys]
        return listFiles