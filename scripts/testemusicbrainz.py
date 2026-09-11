import requests

url = "https://musicbrainz.org/ws/2/artist"
#url muda por tipo de recurso (/artist, /release, /recording)

parametros = {
    "query": "Olivia Rodrigo",
    "fmt": "json" #por padrão, a resposta vem em xml
}
#não utiliza uma chave, mas identifica seu app por meio do user-agent
headers = {
    "User-Agent": "music-data-analysis/1.0 (brenda.luanacb@gmail.com)"

}

response = requests.get(url, params=parametros, headers=headers)
print(response.status_code)
print(response.json())