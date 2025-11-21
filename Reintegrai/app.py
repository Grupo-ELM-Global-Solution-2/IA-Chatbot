from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# --- Configuração e Carregamento dos Modelos ---
MODELO_CLASS_PATH = 'modelo_recomendacao_area.joblib'
MODELO_REG_PATH = 'modelo_estimativa_tempo.joblib'

modelo_classificacao = None
modelo_regressao = None

def carregar_modelos():
    global modelo_classificacao, modelo_regressao
    if os.path.exists(MODELO_CLASS_PATH):
        modelo_classificacao = joblib.load(MODELO_CLASS_PATH)
        print("Modelo de Classificação carregado.")
    else:
        print("AVISO: Modelo de Classificação não encontrado.")

    if os.path.exists(MODELO_REG_PATH):
        modelo_regressao = joblib.load(MODELO_REG_PATH)
        print("Modelo de Regressão carregado.")
    else:
        print("AVISO: Modelo de Regressão não encontrado.")

carregar_modelos()

@app.route('/')
def home():
    return jsonify({
        "message": "API ReIntegrAI Online",
        "endpoints": {
            "/predict": "POST - Envie dados do aluno para receber recomendação e tempo estimado."
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Recebe JSON no formato:
    {
        "idade": 25,
        "horas_disponiveis": 20,
        "nivel_logica": 8,
        "nivel_ingles": 6,
        "area_atual": "Vendas"
    }
    """
    if not modelo_classificacao or not modelo_regressao:
        return jsonify({"error": "Modelos não estão carregados no servidor."}), 500

    try:
        dados = request.get_json()

        # Converter JSON para DataFrame (necessário para o Pipeline entender as colunas)
        df_input = pd.DataFrame([dados])
        
        # Garantir que as colunas estejam na ordem correta/existam
        required_cols = ['idade', 'horas_disponiveis', 'nivel_logica', 'nivel_ingles', 'area_atual']
        for col in required_cols:
            if col not in df_input.columns:
                return jsonify({"error": f"Campo faltando: {col}"}), 400

        # 1. Predição de Classificação (Área)
        area_predita = modelo_classificacao.predict(df_input)[0]

        # 2. Predição de Regressão (Tempo)
        tempo_predito = modelo_regressao.predict(df_input)[0]

        response = {
            "status": "success",
            "aluno": {
                "perfil_atual": dados['area_atual'],
                "dedicacao_semanal": dados['horas_disponiveis']
            },
            "recomendacoes_ia": {
                "trilha_sugerida": area_predita,
                "tempo_estimado_semanas": int(tempo_predito),
                "mensagem_motivacional": f"Com sua experiência em {dados['area_atual']} e dedicando {dados['horas_disponiveis']}h/semana, você pode se tornar um pro em {area_predita} em cerca de {int(tempo_predito)} semanas!"
            }
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)