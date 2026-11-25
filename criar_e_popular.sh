python -m data.criar_banco
python -m data.popular_banco
cp .env.example .env
#python -c 'import secrets; from pathlib import Path; Path(".env").write_text(Path(".env.example").read_text().replace("API_KEY=", "API_KEY=" + secrets.token_urlsafe(32), 1))'