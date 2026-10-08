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
    diretorio = os.path.dirname(caminho)
    resultado = subprocess.run([
        sys.executable, "-m", "papermill",
        caminho, caminho,
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

