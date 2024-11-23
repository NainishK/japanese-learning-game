import requests
import sys
import json

def test_api():
    try:
        base_url = 'http://127.0.0.1:8001'
        
        # Test list endpoint
        print("Testing /api/list/ endpoint...")
        response = requests.get(f'{base_url}/api/list/')
        print(f"Status code: {response.status_code}")
        if response.ok:
            print("Characters in database:")
            for char in response.json():
                print(f"  {char['character']} ({char['romaji']})")
        else:
            print(f"Error: {response.text}")

        print("\nTesting /api/random/ endpoint...")
        response = requests.get(f'{base_url}/api/random/')
        print(f"Status code: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"Random character: {data['character']} ({data['romaji']})")
        else:
            print(f"Error: {response.text}")

    except requests.exceptions.ConnectionError:
        print("Could not connect to the server. Is it running?")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    test_api()
