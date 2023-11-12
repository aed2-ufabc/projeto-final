import json
import requests

def call_api(user_input, idiom_input):
    # Verificando a letra digitada, para setar host
    host = verificar_letra(user_input)

    if idiom_input == "i" and host == 1:
        host = 'remote1'
    elif idiom_input == 'i' and host == 2:
        host = 'remote2'
    elif idiom_input == 'e' and host == 1:
        host = 'remote3'
    else:
        host = 'remote4' 

    api_endpoint = 'http://' + host + ':8080'

    try:
        params = {'q': user_input[0].lower(), 'word': user_input}

        # Make the API call
        response = requests.get(api_endpoint, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            meaning = response.content

            # Exibir o significado, se encontrado
            if meaning:
                print(f'"{user_input}": {meaning}')
            else:
                if idiom_input == "i":
                    print(f'The word "{user_input}" was not found in the dictionary.')
                elif idiom_input == "e":
                    print(f'La palabra "{user_input}" no se encontró en el diccionario.')
        else:
            print("Error:", response.status_code, response.text)

    except Exception as e:
        print("An error occurred:", e)

def verificar_letra(palavra):
    if palavra and palavra[0].lower() >= 'a' and palavra[0].lower() <= 'm':
        return 1
    else:
        return 2

def main():
    idiom_input = 'i'

    while(idiom_input.lower() != 's'):
        # Pedir ao usuário para inserir o idioma
        idiom_input = input("\nDigite o idioma desejado \nI - Inglês \nE - Espanhol \nS - Sair\n\n").lower()
        
        if idiom_input == 'i':
            user_input = input("\nEnter the word you want to search for: ").lower()
            # Chamando a API com a entrada do usuário
            call_api(user_input, idiom_input) 
        
        elif idiom_input == 'e': 
            user_input = input("\nIngrese la palabra que desea buscar: ").lower()
            # Chamando a API com a entrada do usuário
            call_api(user_input, idiom_input) 
        
        elif idiom_input == 's':
            print("\nPrograma encerrado.")
        
if __name__ == "__main__":
    main()
