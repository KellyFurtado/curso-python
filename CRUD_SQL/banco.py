# ==== IMPORTAÇÕES ====

import sqlite3

# ==== FUNÇÕES AUXILIARES ====

def pedir_nome(mensagem):
    """Solicita um nome válido, aceitando letras e espaços."""

    while True:
        nome = input(mensagem).strip()
        nome_sem_espacos = nome.replace(" ", "")

        if nome_sem_espacos.isalpha() and len(nome_sem_espacos) >= 2:
            return nome
        else:
            print("Digite um nome válido (apenas letras e mínimo 2 caracteres).")

def pedir_inteiro(mensagem):
    """Solicita um número inteiro ao usuário, com tratamento de erro."""
    while True:
        try:
            numero = int(input(mensagem))
            return numero
        except ValueError:
            print("Digite apenas números inteiros.")

def inserir_pessoa(nome, idade, cursor, conexao):
    """Insere uma pessoa no banco de dados."""
    cursor.execute("INSERT INTO pessoas(nome, idade) VALUES(?, ?)", (nome, idade))
    conexao.commit()
    return cursor.lastrowid

def atualizar_pessoa(cursor, conexao, pessoa_id, nome, idade):
    """Atualiza o nome e/ou a idade de uma pessoa no banco de dados pelo ID."""

    if nome is not None and idade is None:
        cursor.execute("UPDATE pessoas SET nome = ? WHERE id = ?", (nome, pessoa_id))
    elif nome is None and idade is not None:
        cursor.execute("UPDATE pessoas SET idade = ? WHERE id = ?", (idade, pessoa_id))
    elif nome is not None and idade is not None:
        cursor.execute("UPDATE pessoas SET nome = ?, idade = ? WHERE id = ?", (nome, idade, pessoa_id))
    conexao.commit()
    return cursor.rowcount

def buscar_pessoas(cursor):
    """Busca todas as pessoas cadastradas no banco."""
    cursor.execute("SELECT * FROM pessoas")
    return cursor.fetchall()

def buscar_pessoa_por_id(cursor, id_digitado):
    """Busca uma pessoa pelo ID no banco de dados."""
    cursor.execute("SELECT * FROM pessoas WHERE id = ?", (id_digitado,))
    return cursor.fetchone()

def remover_pessoa(cursor, conexao, id_pessoa):
    """Remove uma pessoa do banco de dados pelo ID."""
    cursor.execute("DELETE FROM pessoas WHERE id = ?", (id_pessoa,))
    conexao.commit()
    return cursor.rowcount

# ==== FUNÇÕES DO SISTEMA ====

def criar_tabela(cursor, conexao):
    """Cria a tabela 'pessoas' se não existir."""
    cursor.execute("CREATE TABLE IF NOT EXISTS pessoas( id INTEGER PRIMARY KEY, nome TEXT, idade INTEGER)")
    conexao.commit()

def cadastrar_pessoa(cursor, conexao):
    """Cadastra uma nova pessoa no banco de dados."""
    nome = pedir_nome("Digite o novo nome: ").title()
    idade = pedir_inteiro("Digite a idade: ")
    pessoa_id = inserir_pessoa(nome, idade, cursor, conexao)
    print("Pessoa cadastrada com sucesso! ID:", pessoa_id)

def listar_pessoas(cursor):
    """Lista todas as pessoas cadastradas."""
    resultado = buscar_pessoas(cursor)
    if resultado:
        for pessoa in resultado:
            print(f"ID: {pessoa['id']} | Nome: {pessoa['nome']} | Idade: {pessoa['idade']}")
    else:
        print("Nenhuma pessoa cadastrada.")

def pesquisar_pessoa(cursor):
    """Pesquisa pessoa pelo ID informado."""
    while True:
        id_digitado = pedir_inteiro("Digite o ID que deseja pesquisar: ")
        resultado = buscar_pessoa_por_id(cursor, id_digitado)
        if resultado is not None:
            print(f"ID: {resultado['id']} | Nome: {resultado['nome']} | Idade: {resultado['idade']}")
            break
        else:
            print("Este ID não consta em nosso cadastro. Tente novamente.")

def editar_pessoa(cursor, conexao):
    """Edita nome e/ou idade de uma pessoa cadastrada."""
    id_pessoa = pedir_inteiro("Digite o ID que deseja editar: ")
    resultado = buscar_pessoa_por_id(cursor, id_pessoa)

    if resultado is not None:
        print(f"ID: {resultado['id']} | Nome: {resultado['nome']} | Idade: {resultado['idade']}")

        nome = None
        idade = None

        print("\n==== MENU ====")
        print("1 - Nome")
        print("2 - Idade")
        print("3 - Nome e Idade")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = pedir_nome("Digite o novo nome: ").title()
            atualizar_pessoa(cursor, conexao, id_pessoa, nome, None)
            print("Alteração realizada com sucesso!")

        elif opcao == "2":
            idade = pedir_inteiro("Digite a nova idade: ")
            atualizar_pessoa(cursor, conexao, id_pessoa, None, idade)
            print("Alteração realizada com sucesso!")

        elif opcao == "3":
            nome = pedir_nome("Digite o novo nome: ").title()
            idade = pedir_inteiro("Digite a nova idade: ")
            atualizar_pessoa(cursor, conexao, id_pessoa, nome, idade)
            print("Alterações realizadas com sucesso!")

        else:
            print("Opção inválida. Tente novamente")
    else:
        print("Pessoa não encontrada.")

def excluir_pessoa(cursor, conexao):
    """Exclui uma pessoa do cadastro pelo ID."""
    id_pessoa = pedir_inteiro("Digite o ID da pessoa que deseja excluir: ")
    resultado = buscar_pessoa_por_id(cursor, id_pessoa)

    if resultado is not None:
        print(f"ID: {resultado['id']} | Nome: {resultado['nome']} | Idade: {resultado['idade']}")
        opcao = input("Tem certeza que deseja excluir essa pessoa? (s/n): ").strip().lower()

        if opcao == "s":
            remover_pessoa(cursor, conexao, id_pessoa)
            print("Pessoa excluída com sucesso!")

        elif opcao == "n":
            print("Pessoa não excluída.")

        else:
            print("Opção inválida.")
    else:
        print("Esse ID não existe.")

# ==== PROGRAMA PRINCIPAL ====

def main():
    """Função principal que controla o menu do sistema."""
    conexao = sqlite3.connect("cadastro.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    criar_tabela(cursor, conexao)

    while True:
        print("\n===== MENU =====")
        print("1 - Cadastrar Pessoa")
        print("2 - Listar Pessoas")
        print("3 - Pesquisar Pessoa")
        print("4 - Editar Pessoa")
        print("5 - Excluir Pessoa")
        print("6 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_pessoa(cursor, conexao)
        elif opcao == "2":
            listar_pessoas(cursor)
        elif opcao == "3":
            pesquisar_pessoa(cursor)
        elif opcao == "4":
            editar_pessoa(cursor, conexao)
        elif opcao == "5":
            excluir_pessoa(cursor, conexao)
        elif opcao == "6":
            print("Você saiu do sistema.")
            conexao.close()
            break
        else:
            print("Opção inválida. Tente novamente.")

# ==== PONTO DE ENTRADA ====
if __name__ == "__main__":
    main()