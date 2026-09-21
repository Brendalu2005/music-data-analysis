from dotenv import load_dotenv
import os, requests, time, json 


load_dotenv() # carrega variáveis de ambiente (.env) direto no programa python
pag_atual = 0
lista_tracks = [] # se declarar com "" - salva uma primeira string vazia
pag_total = 0
api_key = os.getenv('LASTFM_API_KEY')
# processo pra pegar minha key do last.fm

url = "http://ws.audioscrobbler.com/2.0/"
# endereço fixo pra onde toda requisição é enviada; endpoint unico

#  -- PEGANDO A LOCALIZAÇÃO DO TOTALPAGES --

# parametros = {
#     "method": "user.getrecenttracks",
#     "user": "brendaluuc",
#     "api_key": api_key,
#     "format": "json",
#     "limit": 200, # reduz a quantidade de requisições por página
#     "page": pag_atual
#     }

# response = requests.get(url, params=parametros)
# if response.status_code == 200:
#     resposta_json = response.json()

# print(json.dumps(resposta_json["recenttracks"]["@attr"], indent=2))

#print(json.dumps(resposta_json, indent=2)) 
# json.dumps traz a resposta formatada, podendo ver a hierarquia de arquivos

#   --- FIM ---

while(pag_atual<=pag_total):
    pag_atual+=1
    
    parametros = {
    "method": "user.getrecenttracks",
    "user": "brendaluuc",
    "api_key": api_key,
    "format": "json",
    "limit": 200, # reduz a quantidade de requisições por página
    "page": pag_atual
    
    }

    response = requests.get(url, params=parametros)
    if response.status_code == 200:
        resposta_json = response.json()
        pag_total = int(resposta_json["recenttracks"]["@attr"]["totalPages"])
        lista_tracks.extend(resposta_json["recenttracks"]["track"])
   

    time.sleep(0.25)

print(len(lista_tracks))

# criando arquivo json com a lista de tracks
with open("data/raw/lastfm_scrobbles.json", "w", encoding="utf-8") as arquivo:
    json.dump(lista_tracks, arquivo, ensure_ascii=False, indent=2)
#ensure_ascii=False → sem isso, o json.dump 
# converteria acentos em códigos escapados (tipo \u00e9) em vez de manter os caracteres legíveis