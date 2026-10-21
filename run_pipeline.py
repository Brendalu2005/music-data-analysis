import subprocess
import sys
import os

def rodar_script(caminho):
    print(f"Rodando {caminho}...")
    resultado = subprocess.run([sys.executable, caminho])
    if resultado.returncode != 0:
        print(f"Erro ao rodar {caminho}. Parando a pipeline.")
        sys.exit(1)



def rodar_notebook(caminho):
    print(f"Rodando {caminho}...")

    # Pasta onde está run_pipeline.py
    raiz = os.path.dirname(os.path.abspath(__file__))

    entrada = os.path.join(raiz, caminho)
    diretorio = os.path.dirname(entrada)

    # Salva os notebooks executados separadamente.
    pasta_saida = os.path.join(raiz, "notebooks", "executados")
    os.makedirs(pasta_saida, exist_ok=True)

    saida = os.path.join(
        pasta_saida,
        os.path.basename(entrada)
    )

    resultado = subprocess.run([
        sys.executable, "-m", "papermill",
        entrada,
        saida,
        "--cwd", diretorio
    ])

    if resultado.returncode != 0:
        print(f"Erro ao rodar {caminho}. Parando a pipeline.")
        sys.exit(1)

if __name__ == "__main__":
    rodar_script("scripts/extract/extract_lastfm.py")
    rodar_script("scripts/extract/extract_musicbrainz.py")
    rodar_notebook("notebooks/transform/transform_lastfm.ipynb")
    rodar_notebook("notebooks/transform/transform_musicbrainz.ipynb")
    rodar_notebook("notebooks/transform/merge_data.ipynb")
    print("Pipeline concluída com sucesso!")

