import threading

user_states = {}
lock = threading.Lock()

def init_user_state(number, preguntas):
    with lock:
        user_states[number] = {
            "preguntas": preguntas,  # lista de preguntas (diccionarios)
            "indice_actual": 0,
            "respuestas": []
        }

def get_user_state(number):
    with lock:
        return user_states.get(number)

def update_user_state(number, seccion_index=None, pregunta_index=None, respuesta=None):
    with lock:
        if number in user_states:
            if seccion_index is not None:
                user_states[number]["seccion_index"] = seccion_index
            if pregunta_index is not None:
                user_states[number]["indice_actual"] = pregunta_index
            if respuesta is not None:
                user_states[number]["respuestas"].append(respuesta)

def clear_user_state(number):
    with lock:
        if number in user_states:
            del user_states[number]

def get_all_responses(number):
    with lock:
        if number in user_states:
            return user_states[number]["respuestas"]
        return []

def get_next_question(number):
    with lock:
        estado = user_states.get(number)
        if not estado:
            return None
        idx = estado["indice_actual"]
        preguntas = estado["preguntas"]
        if idx < len(preguntas):
            return preguntas[idx]
        return None

def get_last_question(number):
    with lock:
        estado = user_states.get(number)
        if not estado:
            return None
        idx = estado["indice_actual"] - 1
        preguntas = estado["preguntas"]
        if 0 <= idx < len(preguntas):
            return preguntas[idx]
        return None

def advance_index(number):
    with lock:
        if number in user_states:
            user_states[number]["indice_actual"] += 1
