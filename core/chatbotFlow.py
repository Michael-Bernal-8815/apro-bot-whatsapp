import json
import time
import os
from utils import csvExporter
from core import userStateManager as state
from core.services import (
    send_wsp_msg,
    listReply_Message,
    text_Message,
    markRead_Message,
)

# (ruta absoluta del json)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_path = os.path.join(BASE_DIR, "data", "questions.json")

with open(json_path, "r", encoding="utf-8") as f:
    QUESTIONS_DATA = json.load(f)

def enviar_pregunta(pregunta, number, messageId):
    if not pregunta:
        return
    texto = pregunta["pregunta"]
    opciones = pregunta["opciones"]
    seccion = pregunta["seccion"]
    footer = f"Equipo APRO - {seccion}"
    pregunta_numero = pregunta["numero"]

    if opciones:
        mensaje = listReply_Message(
            number, opciones, texto, footer, f"sed{pregunta_numero}", messageId
        )
        send_wsp_msg(mensaje)
    else:
        send_wsp_msg(text_Message(number, texto))


def administrar_chatbot(text, number, messageId, name):
    text = text.lower().strip()
    markRead = markRead_Message(messageId)
    send_wsp_msg(markRead)
    time.sleep(1)

    estado = state.get_user_state(number)

    # Si no hay estado, debe escribir "inicio"
    if not estado:
        if text != "inicio":
            send_wsp_msg(
                text_Message(
                    number,
                    "¡Hola! Esta es una pequeña encuesta. Escribe 'inicio' para comenzar."
                )
            )
            return
        
        # Preparar preguntas
        preguntas = []
        for seccion in QUESTIONS_DATA["secciones"]:
            nombre_seccion = seccion["nombre"]
            for pregunta in seccion["preguntas"]:
                preguntas.append({
                    "pregunta": pregunta["pregunta"],
                    "opciones": pregunta["opciones"],
                    "numero": pregunta["numero"],
                    "seccion": nombre_seccion
                })

        # Iniciar estado
        state.init_user_state(number, preguntas)

        # Enviar primera pregunta
        pregunta = state.get_next_question(number)
        enviar_pregunta(pregunta, number, messageId)
        state.advance_index(number)
        return

    # Si ya hay estado, validamos si ya terminó
    pregunta_anterior = state.get_last_question(number)
    if pregunta_anterior:
        opciones_validas = [
            opt["title"].lower() if isinstance(opt, dict) else opt.lower()
            for opt in pregunta_anterior["opciones"]
        ] if pregunta_anterior["opciones"] else []

        if opciones_validas and text not in opciones_validas:
            send_wsp_msg(
                text_Message(number, "Por favor responde seleccionando una opción válida.")
            )
            return
        
        # Guardar respuesta
        respuesta = {
            "seccion": pregunta_anterior["seccion"],
            "pregunta": pregunta_anterior["pregunta"],
            "respuesta": text
        }
        state.update_user_state(number, respuesta=respuesta)

    # Obtener siguiente pregunta
    siguiente = state.get_next_question(number)

    if siguiente:
        enviar_pregunta(siguiente, number, messageId)
        state.advance_index(number)
    else:
        # Encuesta terminada
        respuestas = state.get_all_responses(number)
        send_wsp_msg(text_Message(number, "🎉 Gracias por completar la encuesta."))

        print(f"\n📋 RESULTADOS PARA: {number}")
        print("seccion,pregunta,respuesta")
        for r in respuestas:
            print(f'"{r["seccion"]}","{r["pregunta"]}","{r["respuesta"]}"')
        
        # Exportar CSV
        csvExporter.exportar_respuestas_csv(respuestas, number)
        state.clear_user_state(number)
