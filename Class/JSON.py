import json, re
from os import listdir

class JSON:

    def __init__(self):
        super(JSON, self).__init__()

    def set_pathfile(self, pathfile):
        self.pathfile = pathfile

    def get_pathfile(self):
        return self.pathfile

    def jwrite(self, config, method="w"):
        with open(self.get_pathfile(), method, encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    def jread(self, site=False, caminho="Projetos/JSON/"):
        with open(self.get_pathfile(), "r", encoding="utf-8") as f:
            dados = f.read()
            return json.loads(dados)

    def jlist(self, ext="json"):
        listFiles = listdir(self.get_pathfile())
        for keys, file in enumerate(listFiles):
            if ext not in file:
                del listFiles[keys]
        return listFiles