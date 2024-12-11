import datetime as dt


class Slot:
    def __init__(self):
        self.id = None
        self.fecha_inicial = None
        self.fecha_final = None

    def asigna_vuelo(self, id, fecha_llegada, fecha_despegue):
        self.id = id
        self.fecha_inicial = fecha_llegada
        self.fecha_final = fecha_despegue

    def slot_esta_libre_fecha_determinada(self, fecha):
        if self.fecha_final is None  or self.fecha_final <fecha:
            return 0
        elif self.fecha_inicial <= fecha <= self.fecha_final :
            time_to_wait = self.fecha_final - fecha
            
            return time_to_wait
    