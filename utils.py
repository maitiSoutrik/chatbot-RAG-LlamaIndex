import os
import yaml

def get_apikey(service):
    """
    Reads API key from a configuration file for a given service.

    Args:
    service (str): The name of the service (e.g., 'openai', 'livekit', 'deepgram', 'cartesia').

    Returns:
    dict or str: The API key(s) for the specified service.
    """
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "apikeys.yml")

    with open(file_path, 'r') as yamlfile:
        apikeys = yaml.safe_load(yamlfile)
        return apikeys.get(service)

if __name__ == "__main__":
    print("OpenAI API Key:", get_apikey('openai').get('api_key'))
    print("LiveKit Config:", get_apikey('livekit'))
    print("Deepgram API Key:", get_apikey('deepgram').get('api_key'))
    print("Cartesia API Key:", get_apikey('cartesia').get('api_key'))