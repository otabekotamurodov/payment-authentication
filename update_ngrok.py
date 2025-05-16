import os
import requests
from dotenv import set_key, load_dotenv

# Local ngrok API endpoint
NGROK_API = "http://127.0.0.1:4040/api/tunnels"

# Path to frontend .env file
ENV_PATH = os.path.join(os.getcwd(), 'frontend', '.env')

def get_ngrok_urls():
    resp = requests.get(NGROK_API).json()
    tunnels = resp.get('tunnels', [])

    frontend_url = ""
    api_url = ""

    for tunnel in tunnels:
        public_url = tunnel.get('public_url', '')
        config_addr = tunnel.get('config', {}).get('addr', '')

        if '5174' in str(config_addr):
            frontend_url = public_url
        elif '8000' in str(config_addr):
            api_url = public_url

    return frontend_url, api_url

def update_env_file(frontend_url, api_url):
    load_dotenv(ENV_PATH)

    if frontend_url:
        set_key(ENV_PATH, 'VITE_FRONTEND_URL', frontend_url)
        print(f"✅ VITE_FRONTEND_URL updated to: {frontend_url}")

    if api_url:
        set_key(ENV_PATH, 'VITE_API_URL', api_url)
        print(f"✅ VITE_API_URL updated to: {api_url}")

if __name__ == "__main__":
    frontend_url, api_url = get_ngrok_urls()
    if frontend_url and api_url:
        update_env_file(frontend_url, api_url)
    else:
        print("❌ Ngrok URL topilmadi! Ngrok tunnel ishlayaptimi tekshir.")
