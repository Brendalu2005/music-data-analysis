import requests, json, time
dados_artistas = {}
lista_tracks = []
lista_artista = set() # declaração de uma lista que não aceita itens repetidos
url = "https://musicbrainz.org/ws/2/artist"
#url muda por tipo de recurso (/artist, /release, /recording)
print("pegando dados do last.fm...\n")
with open("data/raw/lastfm_scrobbles.json", "r", encoding="utf-8") as arquivo:
    lista_tracks = json.load(arquivo)
    
print("selecionando artistas...\n")
for faixa in lista_tracks:
    nome_artista = faixa["artist"]["#text"]
    lista_artista.add(nome_artista) # jeito certo de adicionar uma lista com set

print("extraindo dados do musicBrainz...\n")
for artista in lista_artista:

    parametros = {
        "query": artista,
        "fmt": "json" #por padrão, a resposta vem em xml
    }
    #não utiliza uma chave, mas identifica seu app por meio do user-agent
    headers = {
        "User-Agent": "music-data-analysis/1.0 (brenda.luanacb@gmail.com)"

    }

    response = requests.get(url, params=parametros, headers=headers)
    if response.status_code == 200:
        dados_artistas[artista] = response.json() # musicBrainz retorna um dicionário com infos de varios artistas

    time.sleep(1.00)

print("criando arquivo...\n")
with open("data/raw/musicbrainz_data.json", "w", encoding="utf-8") as arquivo:
    json.dump(dados_artistas, arquivo, ensure_ascii=False, indent=2)

print("arquivo criado com sucesso!\n")