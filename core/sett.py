import os
from dotenv import load_dotenv

load_dotenv()  

token = os.getenv('VERIFY_TOKEN')
whatsapp_token = os.getenv('WHATSAPP_TOKEN')
whatsapp_url = os.getenv('WHATSAPP_URL')
