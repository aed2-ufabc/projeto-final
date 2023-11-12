import json
import os

def split_dictionary(input_file):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_directory, input_file)

    if not os.path.exists(input_path):
        print(f"O arquivo {input_file} não foi encontrado em {script_directory}.")
        return

    with open(input_path, 'r') as file:
        data = json.load(file)

    for letter in "abcdefghijklmnopqrstuvwxyz":
        words_starting_with_letter = {
            word: meaning for word, meaning in data.items() if word.lower().startswith(letter)
        }

        output_file = os.path.join(script_directory, f"{letter}.json")
        with open(output_file, 'w') as file:
            json.dump(words_starting_with_letter, file, indent=2)

if __name__ == "__main__":
    input_json_file = "dictionary.json"
    
    split_dictionary(input_json_file)
