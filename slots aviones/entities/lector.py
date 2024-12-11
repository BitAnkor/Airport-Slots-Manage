import os
import json
import pandas as pd

class Lector:
    def __init__(self, path: str):
        self.path = path

    def _comprueba_extension(self, extension):
        file_extension = os.path.splitext(self.path)[1]
        if file_extension != extension:
            raise Exception("Extension no reconocida")
        else:
            return True
        
    def lee_archivo(self):
        pass

    @staticmethod
    def convierte_dict_a_csv(data: dict):
        df = pd.DataFrame.from_dict(data)
        return df


class LectorCSV(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self):
        if super()._comprueba_extension(".csv"):
            df = pd.read_csv(self.path)          
            return df 
                    

class LectorJSON(Lector):
    def __init__(self, path: str):
        super().__init__(path)
        

    def lee_archivo(self):
        with open(self.path, "r") as json_file:
            my_data = json.load(json_file)
        return my_data



class LectorTXT(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self):
        if super()._comprueba_extension(".txt"):
            with open(self.path, "r", encoding="utf-8") as txt_file:
                lines = txt_file.readlines()
                keys = lines[0].strip().split(", ")
                list_vuelos = [dict(zip(keys, line.rstrip().split(", "))) for line in lines[1:]]
                
                for fecha in range(len(list_vuelos)):
                    correct = list_vuelos[fecha]["fecha_llegada"].replace("T"," ")
                    list_vuelos[fecha]["fecha_llegada"] = correct
        return list_vuelos

            



