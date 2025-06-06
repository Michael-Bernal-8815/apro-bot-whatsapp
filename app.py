from flask import Flask, request
from core import sett
from core import services
from logs import logs
from core import chatbotFlow

app = Flask(__name__)

@app.route('/welcome', methods=['GET'])
def welcome():
    logs.log("Endpoint /welcome solicitado.")
    return 'Hello world, Im running Flask.'

@app.route('/webhook', methods=['GET'])
def verify_token():
    try:
        logs.log("Verificación de token solicitada.")
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        logs.debug(f"Token recibido: {token}, Challenge: {challenge}")
        
        if token == sett.token and challenge:
            logs.log("Token válido.")
            return challenge
        else:
            logs.error("Token inválido.")
            return 'Wrong token', 403
    except Exception as e:
        logs.error(f"Excepción en verify_token: {e}")
        return str(e), 403

def replace_start(s):
    # A formato estandar (Caso Mexico y Argentina)
    number = s[3:]
    if s.startswith("521"):
        return "52" + number
    elif s.startswith("549"):
        return "54" + number
    else:
        return s

@app.route('/webhook', methods=['POST'])
def receive_messages():
    try:
        logs.log("POST recibido en /webhook.")
        body = request.get_json()
        logs.debug(f"JSON recibido: {body}")

        entry = body.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        messages = value.get('messages', [])

        if not messages:
            logs.warning("No hay mensajes en el webhook recibido.")
            return 'no messages', 200

        message = messages[0]

        if 'from' in message:
            raw_number = message['from']
            number = replace_start(str(raw_number))
            messageId = message.get('id', '')
            contacts_list = value.get('contacts', [])
            if contacts_list and isinstance(contacts_list[0], dict):
                contacts = contacts_list[0]
                name = contacts.get('profile', {}).get('name', 'Desconocido')
            else:
                name = 'Desconocido'
            text = services.get_wsp_msg(message)

            logs.log(f"Mensaje recibido de {name} ({number}): {text}")

            # pasamos el texto ya limpio, junto con datos
            chatbotFlow.administrar_chatbot(text, number, messageId, name)

            logs.log("Mensaje procesado correctamente.")
        else:
            logs.warning("No se encontró campo 'from' en el mensaje recibido.")

        return 'sent', 200
    
    except Exception as e:
        logs.error(f"Excepción en receive_messages: {e}")
        return f'not sent: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True)
