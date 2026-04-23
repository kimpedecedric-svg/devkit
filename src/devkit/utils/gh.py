import subprocess
import json

def gh(*args):
    """Lance une commande 'gh' et récupère le texte de sortie."""
    # On utilise subprocess pour lancer la commande dans le système
    result = subprocess.run(['gh', *args], capture_output=True, text=True)
    return result.stdout.strip()

def gh_json(*args):
    """Lance une commande 'gh' et transforme la sortie JSON en liste/dictionnaire Python."""
    raw = gh(*args)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return []