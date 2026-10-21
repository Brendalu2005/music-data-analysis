import requests
import json
import time
import os

MAX_TENTATIVAS = 3

lista_artista = set()
mbids_artistas = {}

url = "https://musicbrainz.org/ws/2/artist"

headers = {
    "User-Agent": "music-data-analysis/1.0 (SEU_CONTATO)"
}

print("Pegando dados do Last.fm...\n")

with open(
    "data/raw/lastfm_scrobbles.json",
    "r",
    encoding="utf-8"
) as arquivo:
    lista_tracks = json.load(arquivo)


print("Selecionando artistas...\n")

for faixa in lista_tracks:
    nome_artista = faixa["artist"]["#text"]
    mbid = faixa["artist"].get("mbid", "")

    lista_artista.add(nome_artista)

    if mbid:
        mbids_artistas.setdefault(nome_artista, set()).add(mbid)


# Carrega os dados já coletados.
if os.path.exists("data/raw/musicbrainz_data.json"):
    with open(
        "data/raw/musicbrainz_data.json",
        "r",
        encoding="utf-8"
    ) as arquivo:
        dados_artistas = json.load(arquivo)
else:
    dados_artistas = {}


print("Extraindo dados do MusicBrainz...\n")

for artista in sorted(lista_artista):
    ids = mbids_artistas.get(artista, set())
    mbid = ""

    if len(ids) == 1:
        mbid = next(iter(ids))

    elif len(ids) > 1:
        print(f"Revisar {artista}: há MBIDs diferentes.")
        continue

    # Confere o cache antes de decidir se precisa consultar.
    if artista in dados_artistas:
        if not mbid:
            # Sem identificador, mantém o resultado anterior por nome.
            continue

        cadastro_salvo = dados_artistas[artista]

        candidatos = (
            cadastro_salvo.get("artists", [])
            if isinstance(cadastro_salvo, dict)
            else []
        )

        cache_compativel = (
            isinstance(candidatos, list)
            and len(candidatos) == 1
            and isinstance(candidatos[0], dict)
            and candidatos[0].get("id") == mbid
        )

        if cache_compativel:
            continue

        print(f"Atualizando cadastro de {artista}...")

    # Com MBID, consulta o cadastro diretamente.
    if mbid:
        url_consulta = f"{url}/{mbid}"

        parametros = {
            "fmt": "json",
            "inc": "aliases+tags"
        }

    # Sem MBID, mantém a busca por nome.
    else:
        url_consulta = url

        parametros = {
            "query": artista,
            "fmt": "json",
            "limit": 1
        }

    coletado = False

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            response = requests.get(
                url_consulta,
                params=parametros,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()
            resposta = response.json()

            # Consulta por MBID retorna um cadastro diretamente.
            if mbid:
                if not isinstance(resposta, dict) or not resposta.get("id"):
                    raise ValueError("Resposta sem cadastro de artista.")

                # Adapta para o formato esperado pelo seu transform.
                resposta = {
                    "created": None,
                    "count": 1,
                    "offset": 0,
                    "artists": [resposta]
                }

            else:
                if (
                    not isinstance(resposta, dict)
                    or not isinstance(resposta.get("artists"), list)
                ):
                    raise ValueError("Resposta de busca inválida.")

            # Atualiza somente depois de uma resposta válida.
            dados_artistas[artista] = resposta
            coletado = True

            print(f"Coletado: {artista}")
            break

        except (requests.RequestException, ValueError) as erro:
            print(
                f"Falha em {artista}, "
                f"tentativa {tentativa}/{MAX_TENTATIVAS}: {erro}"
            )

            if tentativa < MAX_TENTATIVAS:
                time.sleep(5)

        finally:
            # Mantém intervalo também após consultas bem-sucedidas.
            time.sleep(1.1)

    if not coletado:
        print(f"Não foi possível atualizar: {artista}")

        if artista in dados_artistas:
            print("O cadastro anterior foi preservado.")

    # Salva o progresso após cada artista consultado.
    with open(
        "data/raw/musicbrainz_data.json",
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            dados_artistas,
            arquivo,
            ensure_ascii=False,
            indent=2
        )


print("Extração concluída!\n")