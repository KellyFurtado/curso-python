
# ==== IMPORTAÇÕES ====

import os
import json


# ==== FUNÇOES DE ARQUIVO ====

def carregar_cadastro():
    """Carrega os dados do arquivo cadastro.json, ou retorna lista vazia se não existir."""
    if not os.path.exists("cadastro.json"):
        return []
    with open("cadastro.json", "r") as arquivo:
        return json.load(arquivo)
    
def salvar_cadastro(lista_cadastro):
  """Salva a lista de pessoas no arquivo cadastro.json."""
  with open("cadastro.json", "w") as arquivo:
    json.dump(lista_cadastro , arquivo, indent=4)


def atribuir_ids(lista_cadastro):
    """Garante que cada pessoa tenha um ID único."""
    for numero, pessoa in enumerate(lista_cadastro, start=1):
        if "id" not in pessoa:
            pessoa["id"] = numero
        
    salvar_cadastro(lista_cadastro)


# ==== FUNÇOES AUXILIARES ====


def validar_inteiro(valor_str):
    """Valida se uma string pode ser convertida em inteiro."""
    try:
        return int(valor_str)
    except ValueError:
        return None

def encontrar_pessoa_por_id(lista_cadastro, id_procurado):
    """Procura pessoa pelo ID."""
    for pessoa in lista_cadastro:
        if pessoa["id"] == id_procurado:
            return pessoa
    return None

def encontrar_pessoa_por_nome(lista_cadastro, nome_procurado):
    """Procura pessoa pelo nome."""
    for pessoa in lista_cadastro:
        if pessoa["nome"].lower() == nome_procurado.lower():
            return pessoa
    return None

def lista_id(lista_cadastro):
    """Retorna lista de todos os IDs cadastrados."""
    return [pessoa["id"] for pessoa in lista_cadastro]

def maior_id(lista_cadastro):
    """Retorna o maior ID existente no cadastro."""
    ids = lista_id(lista_cadastro)
    return max(ids) if ids else 0
  

# ==== FUNÇOES DO CRUD ====

def cadastro_pessoa(lista_cadastro):
    """Cadastra uma nova pessoa no sistema."""
    nome = input("Nome: ").strip().title()

    # Verifica se já existe pessoa com esse nome
    encontrado = encontrar_pessoa_por_nome(lista_cadastro, nome)
    if encontrado is not None:
        print("Esse nome já está cadastrado. Tente novamente.")
        return
    
    # Idade com validação
    while True:
        idade_str = input("Idade: ")
        idade = validar_inteiro(idade_str)
        if idade is not None:
            break
        print("Idade inválida. Tente novamente.")

    novo_id = maior_id(lista_cadastro) + 1

    nova_pessoa = {
        "id": novo_id,
        "nome": nome,
        "idade": idade
    }
     
    lista_cadastro.append(nova_pessoa)
    salvar_cadastro(lista_cadastro)
    print("Pessoa cadastrada com sucesso!")
        
                      
def listar_pessoas(lista_cadastro):
    """Lista todas as pessoas cadastradas."""
    for pessoa in lista_cadastro:
        print(f" ID: {pessoa['id']} | Nome: {pessoa['nome']}| Idade: {pessoa['idade']}")


def pesquisar_pessoa(lista_cadastro):
    """Pesquisa pessoa pelo ID informado."""
    while True:
        id_str = input("Digite o ID que deseja pesquisar: ")
        id_digitado = validar_inteiro(id_str)
        if id_digitado is not None:
            break
        print("ID inválido. Tente novamente.")

    pessoa_encontrada = encontrar_pessoa_por_id(lista_cadastro, id_digitado)

    if pessoa_encontrada:
        print(f"ID: {pessoa_encontrada['id']} | Nome: {pessoa_encontrada['nome']} | Idade: {pessoa_encontrada['idade']}")
    else:
        print("Esse ID não consta em nosso cadastro.")  

  
def editar_pessoa(lista_cadastro):
    """Edita nome e/ou idade de uma pessoa cadastrada."""

    # === Entrada do ID ===
    while True:
        id_str = input("Digite o ID que deseja editar: ")
        id_editar = validar_inteiro(id_str)
        if id_editar is not None:
            break
        print("ID inválido. Tente novamente.")

    # === Busca da pessoa ===
    pessoa_encontrada = encontrar_pessoa_por_id(lista_cadastro, id_editar)

    if pessoa_encontrada:
        print(f"Nome: {pessoa_encontrada['nome']} \nIdade: {pessoa_encontrada['idade']}")
        print("\n===MENU===")
        print("1- Nome")
        print("2- Idade")
        print("3- Nome e Idade")

        opcao = input("Escolha uma opção: ")

        # === Alteração do nome ===
        if opcao == "1":
            pessoa_encontrada['nome'] = input("Qual será o novo nome? ").strip().title()

        # === Alteração da idade ===
        elif opcao == "2":
            while True:
                idade_str = input("Nova idade: ")
                nova_idade = validar_inteiro(idade_str)
                if nova_idade is not None:
                    pessoa_encontrada["idade"] = nova_idade
                    break
                print("Idade inválida. Tente novamente.")

        # === Alteração de nome e idade ===
        elif opcao == "3":
            pessoa_encontrada['nome'] = input("Qual será o novo nome? ").strip().title()
            while True:
                idade_str = input("Nova idade: ")
                nova_idade = validar_inteiro(idade_str)
                if nova_idade is not None:
                    pessoa_encontrada["idade"] = nova_idade
                    break
                print("Idade inválida. Tente novamente.")

        else:
            print("Opção inválida. Tente novamente")
            return

        # === Salvamento ===
        salvar_cadastro(lista_cadastro)
        print("Dados atualizados com sucesso!")

    else:
        print("Pessoa não encontrada")

def excluir_pessoa(lista_cadastro):
    """Exclui uma pessoa do cadastro pelo ID."""
    while True:
        id_str = input("Digite o ID que deseja excluir: ")
        id_excluir = validar_inteiro(id_str)
        if id_excluir is not None:
            break
        print("ID inválido. Tente novamente.")

    pessoa_encontrada = encontrar_pessoa_por_id(lista_cadastro, id_excluir)
   
    if pessoa_encontrada:
        print(f"Nome: {pessoa_encontrada['nome']} \nIdade: {pessoa_encontrada['idade']}")
        opcao = input("Tem certeza que deseja excluir? (s/n): ").strip().lower()
                                                  
        if opcao == "s":
            lista_cadastro.remove(pessoa_encontrada)
            salvar_cadastro(lista_cadastro)
            print("Exclusão feita com sucesso!")
        elif opcao == "n":
            print("Pessoa não excluída.") 
        else:
            print("Opção inválida")
    else:
        print("Pessoa não encontrada")

# ==== PROGRAMA PRINCIPAL ====

if __name__ == "__main__":
    lista_cadastro = carregar_cadastro()
    atribuir_ids(lista_cadastro) 

                   
while True:

    print("\n===MENU===")
    print("1- cadastrar pessoa")
    print("2- listar pessoas")
    print("3- Pesquisar pessoa")
    print("4- Editar pessoa")
    print("5- Excluir")
    print("6- Sair")
    

    opcao = input("Escolha uma opçao: ")

    if opcao == "1":
        cadastro_pessoa(lista_cadastro)
        
    elif opcao == "2":
        listar_pessoas(lista_cadastro)
    
    elif opcao == "3":
        pesquisar_pessoa(lista_cadastro)

    elif opcao == "4":
        editar_pessoa(lista_cadastro)   
    
    elif opcao == "5":
        excluir_pessoa(lista_cadastro)  
            
    elif opcao == "6":
        print( " Voce saiu do sistema")
        break 

    else:
        print("Opcao inválida. Tente novamente")


