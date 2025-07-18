# utils.py
def leer_visitas():
    try:
        with open("visitas.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def guardar_visitas(valor):
    with open("visitas.txt", "w") as f:
        f.write(str(valor))
