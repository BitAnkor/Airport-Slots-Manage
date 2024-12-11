import pandas as pd
from datetime import datetime, timedelta
from entities.slot import Slot


class Aeropuerto:
    def __init__(self, vuelos: pd.DataFrame, slots: int, t_embarque_nat: int, t_embarque_internat: int):
        self.df_vuelos = vuelos
        self.n_slots = slots
        self.slots = {}
        self.tiempo_embarque_nat = t_embarque_nat
        self.tiempo_embarque_internat = t_embarque_internat

        for i in range(1, self.n_slots + 1):
            self.slots[i] = Slot()

        self.df_vuelos['fecha_despegue'] = pd.NaT
        self.df_vuelos['slot'] = 0

    def calcula_fecha_despegue(self, row) -> pd.Series:   
      
        nueva_fecha_despegue = datetime.strptime(row["fecha_llegada"], "%d/%m/%Y %H:%M" )
        if row["retraso"] != "-":
            retraso = int(row["retraso"][-2:])
            nueva_fecha_despegue += timedelta(minutes = retraso)
        if row["tipo_vuelo"] == "NAT":
            nueva_fecha_despegue += timedelta(minutes = self.tiempo_embarque_nat)
        elif row["tipo_vuelo"] == "INTERNAT":
            nueva_fecha_despegue += timedelta(minutes = self.tiempo_embarque_internat)

        fecha_despegue = datetime.strptime(nueva_fecha_despegue.strftime("%d/%m/%Y %H:%M" ),"%d/%m/%Y %H:%M")

        return fecha_despegue
    

    def encuentra_slot(self, fecha_vuelo) -> int:
        
        for num in range(1, self.n_slots +1):
            if self.slots[num].slot_esta_libre_fecha_determinada(fecha_vuelo) == 0:
                position = num
                break
            else:
                position = -1
        return position    

    def asigna_slot(self, vuelo) -> pd.Series:
        fecha_despegue = self.calcula_fecha_despegue(vuelo)
        fecha_llegada = datetime.strptime(vuelo["fecha_llegada"], "%d/%m/%Y %H:%M")
        position = self.encuentra_slot(fecha_llegada)
        #asigna vuelo de Slot
        
        self.slots[position].asigna_vuelo(vuelo["id"], fecha_llegada , fecha_despegue)
        vuelo["fecha_despegue"] = fecha_despegue
        vuelo["slot"] = position
        return vuelo
    
    def asigna_slots(self):
        pass







