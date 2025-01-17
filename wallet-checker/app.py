import os
from helpful_scripts import TigergraphAPI
from constants import constants
from dotenv import load_dotenv
from flask import Flask, render_template, request


load_dotenv()

TG_USERNAME = os.getenv("TG_USERNAME")
TG_PASSWORD = os.getenv("TG_PASSWORD")
SECRET = os.getenv("SECRET_KMTEST_GRAPH")


app = Flask(__name__)


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/data/", methods=["POST", "GET"])
def data():
    if request.method == "GET":
        return (
            f"The URL /data is accessed directly. Try going to '/form' to submit form"
        )
    if request.method == "POST":
        # Go and get score from API
        form_data = request.form

        target_wallet = form_data["Target wallet"]
        network = form_data["Network"].lower()

        query_params = {
            "v_type": "Wallet",
            "e_type": "sending_payment",
            "re_type": "receiving_payment",
        }

        print(f"Target wallet: {target_wallet}")
        print(f"Checking on the {network} network")

        HOST = constants[network]["host"]
        GRAPH_NAME = constants[network]["graph_name"]

        tg = TigergraphAPI(HOST, GRAPH_NAME, TG_USERNAME, TG_PASSWORD, SECRET)
        score = tg.get_wallet_score(
            installed_query_name="Degree", query_params=query_params
        )

        return render_template("data.html", form_data={target_wallet: score})


app.run(host="localhost", port=5000)
