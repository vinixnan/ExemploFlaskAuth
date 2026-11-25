import os
from secrets import compare_digest

from flask import Flask, request
from dotenv import load_dotenv

from core.banco import BancoSQLite
from core.definitions import DEBUG
from rotas import api

load_dotenv(".env", override=True)


def criar_app():
    app = Flask(__name__)

    api_key = os.environ.get("API_KEY")

    if not api_key:
        raise RuntimeError("Defina API_KEY no arquivo .env.")

    @app.before_request
    def verificar_api_key():
        chave = request.headers.get("X-API-Key", "")

        if not compare_digest(chave.encode("utf-8"), api_key.encode("utf-8")):
            return (
                {"erro": "API Key ausente ou inválida"},
                401,
                {"WWW-Authenticate": 'ApiKey realm="universidade"'},
            )

    app.register_blueprint(api)

    @app.teardown_appcontext
    def fechar_banco(erro=None):
        BancoSQLite().fechar()

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=DEBUG, threaded=True, use_reloader=False)
