from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "18cc3dbd90cf0afb227a0b33"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

@app.route("/")
def home():
    return "¡El servidor Flask está vivo! 🎉"

@app.route("/convert", methods=["GET"])
def convert_currency():
    from_currency = request.args.get("from")
    to_currency = request.args.get("to")
    amount = request.args.get("amount", type=float)

    if not from_currency or not to_currency or amount is None:
        return jsonify({"error": "Faltan parámetros"}), 400

    response = requests.get(BASE_URL + from_currency)
    
    if response.status_code != 200:
        return jsonify({"error": "Error al obtener tasas de cambio"}), 500

    data = response.json()
    exchange_rate = data["conversion_rates"].get(to_currency)

    if exchange_rate is None:
        return jsonify({"error": "Moneda destino no encontrada"}), 400

    converted_amount = amount * exchange_rate

    return jsonify({
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "converted_amount": converted_amount,
        "rate": exchange_rate
    })

if __name__ == "__main__":
    app.run(debug=True)