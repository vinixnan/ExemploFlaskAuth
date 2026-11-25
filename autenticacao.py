from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from model.modelos import UsuarioORM, banco_peewee

auth = HTTPBasicAuth()
# Executa a mesma verificação de hash mesmo quando o login não existe.
HASH_FICTICIO = generate_password_hash("senha-ficticia-nao-utilizada")


@auth.verify_password
@banco_peewee.connection_context()
def verificar_senha(login, senha):
    if not login or not senha:
        return None
    usuario = UsuarioORM.get_or_none(UsuarioORM.login == login)
    senha_hash = usuario.senha_hash if usuario else HASH_FICTICIO
    if not check_password_hash(senha_hash, senha) or usuario is None:
        return None
    if usuario.perfil == "admin" or (
        usuario.perfil == "aluno" and usuario.aluno_id is not None
    ):
        return usuario
    return None


@auth.get_user_roles
def obter_perfil(usuario):
    return usuario.perfil


def pode_acessar(nusp):
    usuario = auth.current_user()
    return usuario.perfil == "admin" or usuario.aluno_id == nusp


@auth.error_handler
def erro_autenticacao(status):
    mensagem = "Autenticação necessária" if status == 401 else "Acesso proibido"
    return {"erro": mensagem}, status
