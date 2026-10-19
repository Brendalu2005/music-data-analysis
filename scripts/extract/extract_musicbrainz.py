import requests, json, time, os
MAX_TENTATIVAS = 3

lista_tracks = []
lista_artista = set() # declaração de uma lista que não aceita itens repetidos
mbids_artistas = {}
url = "https://musicbrainz.org/ws/2/artist"
#url muda por tipo de recurso (/artist, /release, /recording)
print("pegando dados do last.fm...\n")

with open("data/raw/lastfm_scrobbles.json", "r", encoding="utf-8") as arquivo:
    lista_tracks = json.load(arquivo)
    
        
print("selecionando artistas...\n")
for faixa in lista_tracks:
    for faixa in lista_tracks:
        nome_artista = faixa["artist"]["#text"]
        mbid = faixa["artist"].get("mbid", "")
        # pega o identificador ou retorna uma string vazia caso o campo esteja ausente.

        lista_artista.add(nome_artista)

        if mbid:
            mbids_artistas.setdefault(nome_artista, set()).add(mbid)

print("extraindo dados do musicBrainz...\n")
if os.path.exists("data/raw/musicbrainz_data.json"):

    with open("data/raw/musicbrainz_data.json", "r", encoding="utf-8") as arquivo:
        dados_artistas = json.load(arquivo)

    
else:
    dados_artistas = {}


for artista in lista_artista:
    if artista in dados_artistas:
        continue

    ids = mbids_artistas.get(artista, set()) #set retorna por padrão, um conjunto vazio
    mbid = ""  # começa vazio para cada artista

    if len(ids) == 1:
        mbid = next(iter(ids)) # ele atribui à variável mbid o único ID encontrado para o artista atual.
        # iter(ids) cria um iterador: um objeto que permite percorrer os elementos do conjunto.
        # next(...) pede o próximo elemento desse percurso:

    elif len(ids) > 1:
        print(f"Revisar {artista}: há MBIDs diferentes.")
        continue

    # Aqui entra o if mbid que escolhe a URL e os parâmetros.

    parametros = {
        "query": artista,
        "fmt": "json", #por padrão, a resposta vem em xml
        "limit": 1 # musicBraiz retorna, por padrão, 25 artistas parecidos com o nome buscado
    }
    #não utiliza uma chave, mas identifica seu app por meio do user-agent
    headers = {
        "User-Agent": "music-data-analysis/1.0 (brenda.luanacb@gmail.com)"

    }

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        response = requests.get(url, params=parametros, headers=headers)
        if response.status_code == 200:
            resposta = response.json()

            if mbid:
                resposta = {
                    "created": None,
                    "count": 1,
                    "offset": 0,
                    "artists": [resposta]
                }

            dados_artistas[artista] = resposta
            break

        print(f"Falha em {artista} (status {response.status_code}), tentativa {tentativa}/{MAX_TENTATIVAS}")
        time.sleep(5) 
        #solicita json na API do musicBrainz a cada 5 segundos, para não sobrecarregar e gerar bloqueio de IP e falhas nos dados

    if artista not in dados_artistas:
        print(f"Não foi possível coletar {artista}")

    

    with open("data/raw/musicbrainz_data.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados_artistas, arquivo, ensure_ascii=False, indent=2) #se o script for interrompido no meio, os artistas já processados continuam salvos
        #salva os dados a cada passada do loop

    time.sleep(1.00)


print("arquivo criado com sucesso!\n")