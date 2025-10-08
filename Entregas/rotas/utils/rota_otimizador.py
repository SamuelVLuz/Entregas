import requests
from geopy.geocoders import Nominatim
import itertools

def obter_coordenadas(endereco):
    geolocator = Nominatim(user_agent="rotas_app")
    location = geolocator.geocode(endereco)
    if location:
        return (location.longitude, location.latitude)
    return None

def calcular_distancia(ponto1, ponto2):
    url = f"https://router.project-osrm.org/route/v1/driving/{ponto1[0]},{ponto1[1]};{ponto2[0]},{ponto2[1]}?overview=false"
    r = requests.get(url)
    data = r.json()
    if 'routes' in data and len(data['routes']) > 0:
        return data['routes'][0]['distance']
    return float('inf')

def melhor_ordem_enderecos(enderecos):
    coordenadas = [obter_coordenadas(e) for e in enderecos]
    coordenadas = [c for c in coordenadas if c is not None]

    melhor_ordem = None
    menor_distancia = float('inf')

    for perm in itertools.permutations(coordenadas):
        distancia_total = sum(
            calcular_distancia(perm[i], perm[i+1])
            for i in range(len(perm)-1)
        )
        if distancia_total < menor_distancia:
            menor_distancia = distancia_total
            melhor_ordem = perm

    return melhor_ordem, menor_distancia
