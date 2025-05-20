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
    lines = []
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r') as f:
            lines = f.readlines()

    env_dict = {}
    for line in lines:
        if '=' in line:
            k, v = line.strip().split('=', 1)
            env_dict[k] = v

    # Yangilash yoki qo‘shish
    env_dict['VITE_FRONTEND_URL'] = frontend_url
    env_dict['VITE_API_URL'] = api_url

    with open(ENV_PATH, 'w') as f:
        for k, v in env_dict.items():
            f.write(f"{k}={v}\n")

    print(f"✅ VITE_FRONTEND_URL={frontend_url}")
    print(f"✅ VITE_API_URL={api_url}")

if __name__ == "__main__":
    frontend_url, api_url = get_ngrok_urls()
    if frontend_url and api_url:
        update_env_file(frontend_url, api_url)
    else:
        print("❌ Ngrok URL topilmadi! Ngrok tunnel ishlayaptimi tekshir.")
