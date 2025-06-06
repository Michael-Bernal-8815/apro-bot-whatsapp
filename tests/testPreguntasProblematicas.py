"""
Este archivo es para poner a prueba preguntas nuevas/problematicas
durante el desarrollo, mi caso las ultimas 10 eran problematicas
pero ya estan.
"""
from core import services  
from core import sett 

test_number = "52----------" #Numero de prueba
sedd = "test_sedd_final"
message_id = "final_msg"

preguntas = [
    {
        "numero": 40,
        "pregunta": "Tengo claridad sobre lo que se espera de mí.",
        "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"]
    },
    {
        "numero": 41,
        "pregunta": "Tengo autonomía en la toma de decisiones.",
        "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"]
    },
    {
        "numero": 42,
        "pregunta": "Me asignan tareas importantes.",
        "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"]
    },
    {
        "numero": 43,
        "pregunta": "Tengo oportunidades de desarrollar nuevas habilidades.",
        "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"]
    },
    {
        "numero": 44,
        "pregunta": "Me ofrecen capacitación o formación continua.",
        "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"]
    },
    {
        "numero": 45,
        "pregunta": "La empresa promueve el crecimiento profesional.",
        "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"]
    },
    {
        "numero": 46,
        "pregunta": "Existen oportunidades claras de ascenso.",
        "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"]
    },
    {
        "numero": 47,
        "pregunta": "Se reconoce el mérito para promociones.",
        "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"]
    },
    {
        "numero": 48,
        "pregunta": "La empresa motiva a mejorar para ascender.",
        "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"]
    },
    {
        "numero": 49,
        "pregunta": "Conozco el plan de carrera dentro de la org.",
        "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"]
    },
    {
        "numero": 50,
        "pregunta": "Me siento motivado para crecer dentro de la empresa.",
        "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"]
    }
]

# Enviar preguntas
for pregunta in preguntas:
    print(f"\n🔹 Enviando pregunta {pregunta['numero']}: {pregunta['pregunta']}")
    
    data = services.listReply_Message(
        number=test_number,
        options=pregunta["opciones"],
        body=pregunta["pregunta"],
        footer="Selecciona una opción",
        sedd=sedd,
        messageId=message_id
    )
    
    result, status = services.send_wsp_msg(data)
    print(f"Resultado: {result}")
    print(f"Código HTTP: {status}")
