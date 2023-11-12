import json
from ftplib import FTP
from io import BytesIO

ftp_user = 'username'
ftp_password = 'mypass'

def download_file(ftp_host, ftp_user, ftp_password, remote_file_path):
    try:
        # Connect to the FTP server
        with FTP() as ftp:
            ftp.connect(ftp_host, 21)
            # Log in
            ftp.login(user=ftp_user, passwd=ftp_password)

            # Change to the appropriate directory if needed
            # ftp.cwd('/path/to/remote/directory')
            # Open a local file for writing in binary mode
           # Use BytesIO to store the file content in memory
            file_content = BytesIO()

            # Retrieve the remote file and write it to BytesIO
            ftp.retrbinary('RETR ' + remote_file_path, file_content.write)

            # Move the cursor to the beginning of the BytesIO buffer
            file_content.seek(0)

            # Read the content of BytesIO into a JSON variable
            json_data = json.load(file_content)

            # Print or use the JSON data as needed
            print("JSON Data:")
            print(json_data)

    except Exception as e:
        print(f"An error occurred: {e}")


def call_api(user_input):
    first_letter = user_input[0]
    host = 'remote3'

    if first_letter == 'a':
        host = 'remote1'
    elif first_letter == 'b':
        host = 'remote2'

    remote_file_path = '/'+first_letter+'/file.json'
    try:
        download_file(host, ftp_user, ftp_password, remote_file_path)
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