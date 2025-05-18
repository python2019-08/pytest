import requests

proxies = {
    'http': 'http://127.0.0.1:8123',
    'https': 'http://127.0.0.1:8123'
}

proxies01 = {
    'http': 'http://127.0.0.1:8123',
    'https': 'http://127.0.0.1:8123'
}

try:
    # response = requests.get('https://huggingface.co/Flux9665/ToucanTTS/resolve/main/ToucanTTS.pt', proxies=proxies)
    response = requests.get('https://huggingface.co/Flux9665/ToucanTTS/resolve/main/ToucanTTS.pt', proxies=proxies01)
    print(response.text)
except requests.exceptions.RequestException as e:
    print(f"请求出错: {e}")