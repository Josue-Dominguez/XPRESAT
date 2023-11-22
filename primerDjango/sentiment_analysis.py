from transformers import pipeline

# Inicializar el pipeline de análisis de sentimientos
analizador_de_sentimientos = pipeline("sentiment-analysis")

def analizar_sentimiento(texto):
    # Utilizar el pipeline para analizar el sentimiento
    resultado = analizador_de_sentimientos(texto)

    # La salida será una lista de diccionarios, cada uno con las claves 'label' y 'score'
    sentimiento = resultado[0]['label']

    # Convertir las etiquetas a un formato más simple ('positivo', 'negativo', 'neutral')
    if sentimiento == 'POSITIVE':
        return 'positivo'
    elif sentimiento == 'NEGATIVE':
        return 'negativo'
    else:
        return 'neutral'
