import requests
import json

# URL da sua API local
url = "http://127.0.0.1:5000/predict"

# Dados do aluno para teste
payload = {
    "idade": 28,
    "horas_disponiveis": 30,
    "nivel_logica": 4,
    "nivel_ingles": 8,
    "area_atual": "Direito"
}

# Envia a requisição POST
try:
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Sucesso! Resposta da API:")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    else:
        print(f"Erro {response.status_code}: {response.text}")

except requests.exceptions.ConnectionError:
    print("Erro: Não foi possível conectar à API. Verifique se ela está rodando.")
