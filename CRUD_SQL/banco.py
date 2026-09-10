# ==== IMPORTAÇÕES ====

import sqlite3

# ==== FUNÇOES AUXILIARES ====

def pedir_inteiro(mensagem):
    while True:
        try:
            numero = int(input(mensagem))
            return numero
        except ValueError:
            print("Digite apenas números inteiros.")
  
# ==== CONEXAO COM O BANCO ====

conexao = sqlite3.connect("cadastro.db")
conexao.row_factory = sqlite3.Row
cursor = conexao.cursor()

# ==== FUNÇOES DO SISTEMA ====

def criar_tabela():
    cursor.execute("CREATE TABLE IF NOT EXISTS pessoas( id INTEGER PRIMARY KEY, nome TEXT, idade INTEGER)")
    conexao.commit()

def cadastrar_pessoa():
    nome = input("Digite um nome: ")
    idade = pedir_inteiro("Digite a idade: ")
    cursor.execute( "INSERT INTO pessoas(nome, idade) VALUES( ? , ?)",
                  (nome, idade)
    )
    conexao.commit()
    print("Pessoa cadastrada com sucesso! ID:" , cursor.lastrowid)

def listar_pessoas():
    cursor.execute(" SELECT * FROM pessoas ")
    resultado = cursor.fetchall()

    for pessoa in resultado:
        print(f"ID: {pessoa['id']} | Nome: {pessoa['nome']} | Idade: {pessoa['idade']}")

def pesquisar_pessoa():

    while True:

        id_digitado = pedir_inteiro("Digite o ID que deseja pesquisar: ")
        cursor.execute("SELECT * FROM pessoas WHERE id = ?" ,
                      (id_digitado,)
        )
        resultado = cursor.fetchone()

        if resultado is not None:
            print(f" ID: {resultado['id']} | Nome: {resultado['nome']}| Idade: {resultado['idade']}")
            break
        else: 
            print(" Este ID não consta em nosso cadastro. Tente novamente.")

def editar_pessoa():

    while True:

        id_pessoa = pedir_inteiro("Digite o ID que deseja editar: ")    
        cursor.execute("SELECT * FROM pessoas WHERE id = ? " ,
                   (id_pessoa,)
        )
        resultado = cursor.fetchone()

        if resultado is not None:
            print(f" ID: {resultado['id']} | Nome: {resultado['nome']} | Idade: {resultado['idade']}")
            print("\n ==== MENU ====")
            print("1 - Nome")
            print("2 - Idade")
            print("3 - Nome e Idade")

            while True:

                opcao = input("Escolha uma opçao: ")

                if opcao == "1":
                    novo_nome = input("Digite o novo nome: ")
                    cursor.execute(" UPDATE pessoas SET nome = ? WHERE id = ?" , 
                                  (novo_nome, id_pessoa)
                    )
                    conexao.commit()
                    print("Alteraçao realizada com sucesso!")
                    print(f" ID: {resultado['id']} | Nome: {novo_nome} | Idade: {resultado['idade']}")

                elif opcao == "2":
                    nova_idade = pedir_inteiro("Digite a nova idade: ")
                    cursor.execute(" UPDATE pessoas SET idade = ? WHERE id = ?" ,
                                  ( nova_idade, id_pessoa) 
                    )
                    conexao.commit()
                    print("Alteraçao realizada com sucesso!")
                    print(f" ID: {resultado['id']} | Nome: {resultado['nome']} | Idade: {nova_idade} ")

                elif opcao == "3":

                    novo_nome = input("Digite o novo nome: ")
                    nova_idade = pedir_inteiro("Digite a nova idade: ")
                    cursor.execute(" UPDATE pessoas SET nome = ? , idade = ?  WHERE id = ?" , 
                                  (novo_nome, nova_idade, id_pessoa) 
                    )
                    conexao.commit()
                    print("Alterações realizadas com sucesso!")
                    print(f" ID: {resultado['id']} | Nome: {novo_nome} | Idade: {nova_idade}")

                    return

                else:
                    print("Opçao inválida. Tente novamente")
                    continue

                
        else:
            print("Pessoa não encontrada. Tente novamente.")
        

def excluir_pessoa():

    id_pessoa = pedir_inteiro("Digite o id da pessoa que deseja excluir: ")
    cursor.execute("SELECT * FROM pessoas WHERE id = ?" ,
                   (id_pessoa,)
    )
    resultado = cursor.fetchone()

    if resultado is not None:
        print(f"ID: {resultado['id']} | Nome: {resultado['nome']} | Idade: {resultado['idade']}")

        while True:

            print("s - Sim")
            print("n - Não")
            opcao = input(" Tem certeza que deseja excluir essa pessoa? s/n: ").strip().lower()
           

            if opcao == "s":
                cursor.execute( "DELETE FROM pessoas WHERE id = ?" ,
                              (id_pessoa,)
                )
    
                conexao.commit()

                print("Pessoa excluída com sucesso!")
                break

            elif opcao == "n":
                print("Pessoa não excluída.")
                break

            else: 
                print("Opção inválida. Tente novamente.")
                continue

    else:
        print(" Esse ID nao existe.")
            
    
# ==== PROGRAMA PRINCIPAL ====

def main():
    criar_tabela()
    while True:

        print("\n===== MENU =====")
        print("1 - Cadastrar Pessoa")
        print("2 - listar Pessoa")
        print("3 - Pesquisar Pessoa")
        print("4 - Editar Pessoa")
        print("5 - Excluir Pessoa")
        print("6 - Sair")


        opcao = input("Escolha uma opçao: ")

        if opcao == "1":
         cadastrar_pessoa()

        elif opcao == "2":
            listar_pessoas()

        elif opcao == "3":
            pesquisar_pessoa()

        elif opcao == "4":
            editar_pessoa()

        elif opcao == "5":
            excluir_pessoa()

        elif opcao == "6":
            print( "Você saiu do sistema.")
            conexao.close()
            break 

# ==== PONTO DE ENTRADA ====
if __name__ == "__main__":
    main()