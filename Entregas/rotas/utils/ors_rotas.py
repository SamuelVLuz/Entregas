import openrouteservice
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="rotas_app")

# substitua pela sua key
ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImJjMDQ4YmM4MjQzNzQwNDJiMzRhYTk3YmM0ZmNhNjhhIiwiaCI6Im11cm11cjY0In0="
client = openrouteservice.Client(key=ORS_API_KEY)

def obter_coordenadas(endereco):
    try:
        location = geolocator.geocode(endereco, timeout=10)
        if location:
            return [location.longitude, location.latitude]
    except Exception as e:
        print("Erro geocode:", e)
    return None


def melhor_ordem_entregas_ors(entregas):
    """
    Retorna lista de entregas na ordem otimizada pelo ORS e distância total (m).
    """

    entregas_coords = []
    for e in entregas:
        endereco_completo = f"{e.endereco}, {e.cidade}, {e.uf}"
        coord = obter_coordenadas(endereco_completo)
        if coord:
            entregas_coords.append((e, coord))

    if len(entregas_coords) < 2:
        return [e for e, _ in entregas_coords], 0

    try:
        coords = [coord for _, coord in entregas_coords]
        jobs = [{"id": i + 1, "location": coord} for i, coord in enumerate(coords)]

        # Veículo que começa e termina no primeiro ponto
        vehicles = [{"id": 1, "start": coords[0], "end": coords[0]}]

        resp = client.optimization(jobs=jobs, vehicles=vehicles)

        # Debug opcional
        # import json; print(json.dumps(resp, indent=2))

        route = resp["routes"][0]
        steps = route.get("steps", [])
        distancia = route["summary"]["distance"]

        entregas_ordenadas = []
        for step in steps:
            job_id = step.get("job")
            if job_id:
                # IDs começam em 1, então ajusta o índice
                ent, _ = entregas_coords[job_id - 1]
                entregas_ordenadas.append(ent)

        return entregas_ordenadas, distancia

    except Exception as e:
        print("Erro ORS otimização:", e)
        return [e for e, _ in entregas_coords], 0
