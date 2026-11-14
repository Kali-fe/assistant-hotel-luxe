"""Prépare un notebook Colab pour GitHub.

Usage :
    python tools/nettoyer_notebook.py notebooks/AVH_final.ipynb            # garde les sorties
    python tools/nettoyer_notebook.py notebooks/AVH_final.ipynb --sorties  # efface aussi les sorties

Pourquoi : Colab enregistre l'état des barres de progression (metadata.widgets), ce qui fait échouer l'affichage
du notebook sur GitHub (« Invalid Notebook ») et alourdit le fichier de plusieurs centaines de Ko.
"""
import json
import sys

chemin = sys.argv[1]
effacer_sorties = "--sorties" in sys.argv

with open(chemin, encoding="utf-8") as f:
    nb = json.load(f)

nb.get("metadata", {}).pop("widgets", None)
for cellule in nb["cells"]:
    cellule.get("metadata", {}).pop("widgets", None)
    if effacer_sorties and cellule["cell_type"] == "code":
        cellule["outputs"] = []
        cellule["execution_count"] = None

with open(chemin, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print(f"Notebook nettoyé : {chemin}")
