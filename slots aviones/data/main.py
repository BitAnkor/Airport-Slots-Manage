import os
import pandas as pd
import datetime as dt
from entities import lector, aeropuerto


def preprocess_data(df_list): 
   
    df = pd.concat([df_list[i] for i in range(len(df_list))], axis=0, ignore_index=True)
    df = df.sort_values(["fecha_llegada"],ignore_index= True)
    
    return df


if __name__ == '__main__':
    path_1 = os.path.abspath('./data/vuelos_1.txt')
    path_2 = os.path.abspath('./data/vuelos_2.csv')
    path_3 = os.path.abspath('./data/vuelos_3.json')

df_list = []

l_txt= lector.LectorTXT(path_1).lee_archivo()
df_txt = lector.Lector.convierte_dict_a_csv(l_txt)
df_list.append(df_txt)


df_csv = lector.LectorCSV(path_2).lee_archivo()
df_list.append(df_csv)

l_json = lector.LectorJSON(path_3).lee_archivo()
df_json = lector.Lector.convierte_dict_a_csv(l_json)
df_list.append(df_json)

df =preprocess_data(df_list)


mi_aeropuerto = aeropuerto.Aeropuerto(df,3, 30, 60)
for row in df.iterrows():
    fecha_llegada = dt.datetime.strptime(row[1]["fecha_llegada"], "%d/%m/%Y %H:%M")
    slot_check= mi_aeropuerto.encuentra_slot(fecha_llegada)
    
    if slot_check != -1:
        vuelo_updated = mi_aeropuerto.asigna_slot(row[1])

    else:
        while slot_check == -1:
            fecha_llegada = fecha_llegada + dt.timedelta(minutes=10)
            slot_check= mi_aeropuerto.encuentra_slot(fecha_llegada)
        
        row[1]["fecha_llegada"] = fecha_llegada.strftime("%d/%m/%Y %H:%M")
        vuelo_updated = mi_aeropuerto.asigna_slot(row[1])

    print(f"El vuelo {vuelo_updated["id"]} con fecha de llegada y despegue {vuelo_updated["fecha_llegada"]} {vuelo_updated["fecha_despegue"]}, ha sido asignado al slot {vuelo_updated["slot"]}")   
        


        

        
