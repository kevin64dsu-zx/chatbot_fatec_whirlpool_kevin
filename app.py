from flask import Flask, render_template, request, jsonify
from port_ia import responder_ia
from db_connector import log_message, get_history

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    mensagem_usuario = data.get("message", "")

    log_message('user', mensagem_usuario)
    resposta = responder_ia(mensagem_usuario)
    log_message('model', resposta)

    return jsonify({"response": resposta})

@app.route("/historico")
def view_history():
    history_data = get_history()
    return render_template("history.html", history=history_data)

if __name__ == "__main__":
    app.run(debug=True)
