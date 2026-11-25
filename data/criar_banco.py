from core.definitions import ARQUIVO_BANCO
from model.modelos import (
    banco_peewee,
    AlunoORM,
    DisciplinaORM,
    MatriculaORM,
    UsuarioORM,
)


def criar_tabelas():
    with banco_peewee:
        banco_peewee.create_tables(
            [AlunoORM, DisciplinaORM, MatriculaORM, UsuarioORM], safe=True
        )
    print(f"Tabelas criadas em: {ARQUIVO_BANCO}")


if __name__ == "__main__":
    criar_tabelas()
