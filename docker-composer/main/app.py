import requests

def call_api(user_input):
    api_endpoint = 'http://remote:5001/'

    # Set up the parameters with the user input
    params = {'q': user_input}

    try:
        # Make the API call
        response = requests.get(api_endpoint, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print or process the API response here
            print("API Response:", response.json())
        else:
            print("Error:", response.status_code, response.text)

    except Exception as e:
        print("An error occurred:", e)

def main():
    # Get user input
    user_input = input("Enter your query: ")

    # Call the API with the user input
    call_api(user_input)

if __name__ == "__main__":
    main()
