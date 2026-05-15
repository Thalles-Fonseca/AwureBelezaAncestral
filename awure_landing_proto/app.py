from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import csv
from pathlib import Path

app = Flask(__name__)
app.secret_key = "awure-beleza-ancestral-secret"

LEADS_FILE = Path("leads_awure.csv")
COWORKERS_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSeRzOh0nEMoiXVrzHuAzeNRfELlnpbcWx1RVU9Mvl43be4NLQ/viewform"

SERVICOS = [
    "Limpeza de Pele",
    "Micropigmentação / Design de Sobrancelhas",
    "Micropigmentação / Neutralização Labial",
    "Terapia e Cuidados Capilares",
    "Hidratação e Nutrição Facial",
    "Lash Design / Lash Lifting",
    "Epilação",
    "Drenagem Linfática",
    "Massagens em geral",
    "Redução de Medidas",
    "Reconstrução de Aréola",
    "Maquiagem",
    "Lábios",
    "Nails Design",
    "Tratamento de Estrias",
    "Tranças / Penteados / Telas",
    "HidraGloss / Brown Lamination",
]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", servicos=SERVICOS, coworkers_form=COWORKERS_FORM)

@app.route("/capturar-lead", methods=["POST"])
def capturar_lead():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    telefone = request.form.get("telefone", "").strip()
    empresa = request.form.get("empresa", "").strip()
    cargo = request.form.get("cargo", "").strip()
    interesse = request.form.get("interesse", "").strip()
    mensagem = request.form.get("mensagem", "").strip()

    if not nome or not email or not telefone:
        flash("Preencha nome, e-mail e telefone para receber o atendimento.", "erro")
        return redirect(url_for("index") + "#lead")

    novo_arquivo = not LEADS_FILE.exists()
    with LEADS_FILE.open("a", newline="", encoding="utf-8") as arquivo:
        campos = ["data", "nome", "email", "telefone", "empresa", "cargo", "interesse", "mensagem"]
        writer = csv.DictWriter(arquivo, fieldnames=campos)
        if novo_arquivo:
            writer.writeheader()
        writer.writerow({
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "empresa": empresa,
            "cargo": cargo,
            "interesse": interesse,
            "mensagem": mensagem,
        })

    flash("Cadastro recebido com sucesso! A equipe Awure vai entrar em contato.", "sucesso")
    return redirect(url_for("index") + "#lead")

if __name__ == "__main__":
    app.run(debug=True)
