import json
import requests

def call_api(user_input):
    host = 'remote3'

    if user_input == 'a':
        host = 'remote1'
    elif user_input == 'b':
        host = 'remote2'

    api_endpoint = 'http://' + host + ':8080'

    try:
        params = {'q': 'dictionary', 'word': user_input}

        # Make the API call
        response = requests.get(api_endpoint, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            meaning = response.content

            # Exibir o significado, se encontrado
            if meaning:
                print(f'O significado de "{user_input}" é: {meaning}')
            else:
                print(f'A palavra "{user_input}" não foi encontrada no dicionário.')
        else:
            print("Error:", response.status_code, response.text)

    except Exception as e:
        print("An error occurred:", e)

def main():
    # Pedir ao usuário para inserir o idioma
    # idiom_input = input("Digite o idioma desejado \nI - Inglês \nE - Espanhol\n\n").lower()
    
    # if idiom_input == 'i':
    #     user_input = input("\nEnter the word you want to search for: ").lower()
    # elif idiom_input == 'e': 
    #     user_input = input("\nIngrese la palabra que desea buscar: ").lower()
      
    user_input = input("\nEnter the word you want to search for: ").lower()
    
    # Chamando a API com a entrada do usuário
    call_api(user_input) 

if __name__ == "__main__":
    main()
