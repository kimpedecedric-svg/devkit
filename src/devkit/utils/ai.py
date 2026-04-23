import os
import time
from google import genai
from google.genai import errors

# Modèles à essayer dans l'ordre
MODELS_FALLBACK = [
    'gemini-2.0-flash', # Ton modèle principal
    'models/gemini-1.5-flash', # Avec le préfixe complet pour éviter le 404
    'models/gemini-1.5-pro',
]

def ask_gemini(prompt, max_retries=2, retry_delay=60):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Erreur : La variable GOOGLE_API_KEY n'est pas définie."

    client = genai.Client(api_key=api_key)

    for model in MODELS_FALLBACK:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                return response.text

            except errors.ClientError as e:
                status = getattr(e, 'status', None) or str(e)

                # Quota dépassé → retry après délai ou passer au modèle suivant
                if '429' in str(e) or 'RESOURCE_EXHAUSTED' in str(e):
                    if attempt < max_retries - 1:
                        print(f"[{model}] Quota dépassé, retry dans {retry_delay}s...")
                        time.sleep(retry_delay)
                    else:
                        print(f"[{model}] Quota épuisé, passage au modèle suivant...")
                        break  # Essayer le prochain modèle

                # Modèle non disponible → passer directement au suivant
                elif '404' in str(e) or 'NOT_FOUND' in str(e):
                    print(f"[{model}] Modèle non disponible, passage au suivant...")
                    break

                # Autre erreur → remonter immédiatement
                else:
                    return f"Erreur inattendue ({model}) : {str(e)}"

            except Exception as e:
                return f"Erreur inattendue : {str(e)}"

    return "Erreur : Tous les modèles sont indisponibles ou les quotas sont épuisés."