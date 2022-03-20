import math

def calcularDistancia(lt1, ln1, lt2, ln2):
    radio_terrestre = 6373.0

    lat1 = math.radians(float(lt1))
    lat2 = math.radians(float(lt2))
    lon1 = math.radians(float(ln1))
    lon2 = math.radians(float(ln2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return radio_terrestre*c #km


if __name__ == "__main__":
    #43.365838426899984, -8.417328628622382
    #43.00866463099592, -7.555649819479831
    print(calcularDistancia('-33.885643', '151.187424', '-7.417328628622382', '43.365838426899984'))
