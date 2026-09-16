from dotenv import load_dotenv
import os, requests

load_dotenv()

api_key = os.getenv('LASTFM_API_KEY')
# processo pra pegar minha key do last.fm

url = "http://ws.audioscrobbler.com/2.0/"
# endereço fixo pra onde toda requisição é enviada; endpoint unico

parametros = {
    "method": "user.getrecenttracks",
    "user": "brendaluuc",
    "api_key": api_key,
    "format": "json",
    "limit": 5

}

response = requests.get(url, params=parametros)

#testando
print(response.status_code) #retorna 200 se deu certo
print(response.json()) #mostra o conteúdo da resposta em formato json