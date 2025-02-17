import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia.wikipedia
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import requests, unicodedata, re
import traductor

'''
# Vizualizar opciones de voces instaladas en el ordenador
engine = pyttsx3.init()
for voz in engine.getProperty('voices'):
    print(voz)
'''
# Opciones de voz / Idioma
id_voice1 = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
id_voice2 = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"
id_voice3 = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"


# Escuchar microfono y devolver el audio como texto
def transformar_audio_en_texto():
    # Almacenar Recognizer en variable
    r = sr.Recognizer()

    # Configurar microfono
    with sr.Microphone() as origen:
        # Teimpo de espera en lo que se activa el microfono
        r.pause_threshold = 0.8

        # Informar que comenzo la grabacion
        print("Ya puedes hablar")

        # Guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # Buscar en Google
            pedido = r.recognize_google(audio, language="es-mx")
            # Prueba de que pudo ingresar
            print("Dijiste: "+pedido)
            # Decolver pedido
            return pedido
        
        # En caso de no comprender el audio
        except sr.UnknownValueError:
            # Prueba de que no comprendio el audio
            print("No Entendi")

            # devolver error
            return "Sigo esperando"
        
        # En caso de no resolver el pedido
        except sr.RequestError:
            # Prueba de que no comprendio el audio
            print("No hay servicio")

            # devolver error
            return "Sigo esperando"
        
        # Error inesperado
        except:
            # Prueba de que no comprendio el audio
            print("Algo salio mal")

            # devolver error
            return "Sigo esperando"


# Funcion para que el asistente pueda ser escuchado
def hablar_asistente(mensaje):
    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice',id_voice1)

    # pronuncioar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# Informar que dia de la semana es
def pedir_dia():
    # Crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)
    mes = dia.month

    # Diccionarios de dias de la semana y meses
    dic_dia_semana = {0:'Lunes',
                      1:'Martes',
                      2:'Miércoles',
                      3:'Juevez',
                      4:'Viernes',
                      5:'Sábado',
                      6:'Domingo'}
    dic_meses = {1:"Enero",
                 2:"Febrero",
                 3:"Marzo",
                 4:"Abril",
                 5:"Mayo",
                 6:"Junio",
                 7:"Julio",
                 8:"Agosto",
                 9:"Septiembte",
                 10:"Octubre",
                 11:"Noviembre",
                 12:"Diciembre"}
    
    # El asistente dira que dia es 
    hablar_asistente(f'Hoy es {dic_dia_semana[dia_semana]} {dia.day} de {dic_meses[mes]} del {dia.year}')


# Infromar Hora
def pedir_hora():
    # Variable con datos de la hora 
    hora = datetime.datetime.now()
    hora = f'Son las {hora.hour} horas con {hora.minute} minutos'
    print(hora)

    # Decir la hora
    hablar_asistente(hora)


# Funcion saludo inicial
def saludo_inicial():
    # Variables con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif  6 <= hora.hour < 12:
        momento = 'Buenos dias'
    else:
        momento = 'Buenas Tardes'
    # Decir saludo
    hablar_asistente(f"{momento}, Hola soy Sabina, tu asistente virtual. ¿En que puedo ayudarte el día de hoy?")


def procesar_conversion(texto):
    # Diccionario de símbolos y monedas
    divisas = {
    "dólar": {"plural": "dólares", "código": "USD"},
    "euro": {"plural": "euros", "código": "EUR"},
    "€": {"plural": "€", "código": "EUR"},
    "peso": {"plural": "pesos", "código": "MXN"},
    "libra": {"plural": "libras", "código": "GBP"},
    "yen": {"plural": "yenes", "código": "JPY"},
    "rublo": {"plural": "rublos", "código": "RUB"},
    "real": {"plural": "reales", "código": "BRL"},
    "franco": {"plural": "francos", "código": "CHF"},
    "corona": {"plural": "coronas", "código": "DKK"},
    "króna": {"plural": "krónas", "código": "ISK"},
    "złoty": {"plural": "złotys", "código": "PLN"},
    "rupia": {"plural": "rupias", "código": "INR"},
    "won": {"plural": "wones", "código": "KRW"},
    "dólar australiano": {"plural": "dólares australianos", "código": "AUD"},
    "dólar canadiense": {"plural": "dólares canadienses", "código": "CAD"},
    }

    palabras = texto.lower().split(' ')

    # Buscar monto
    monto = None
    for palabra in palabras:
        if palabra.startswith('$') or palabra.isdigit():
            monto = palabra.replace('$', '')  # Extraer monto
        if "un" in palabra or "una" in palabra:
            monto = 1
        
        if "$" in palabra and palabras[-1] == "pesos":
            palabras.insert(2,"dólares")
        if "$" in palabra and palabras[-1] == "dólares":
            palabras.insert(2,"pesos")
        


    # Buscar moneda de origen y destino
    moneda_origen = None
    moneda_destino = None
    for palabra in palabras:
        for divisa, info in divisas.items():
            if palabra == divisa or palabra == info["plural"]:
                if not moneda_origen:
                    moneda_origen = info["código"]
                else:
                    moneda_destino = info["código"]
    
    if monto and moneda_origen and moneda_destino:
        return monto, moneda_origen, moneda_destino
    else:
        return None


# Remover acentos 
def remover_acentos(texto):
    # Normalizar el texto a formato Unicode y eliminar las marcas de acento
    texto_normalizado = unicodedata.normalize('NFD', texto)
    return ''.join(char for char in texto_normalizado if unicodedata.category(char) != 'Mn')


# Funcion central del asistente 
def solicitud():
    
    # Activar saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True
    while comenzar:
        # Activar microfono y guardar la solicitud en string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar_asistente('Con gusto, espera un moemento en lo que abro youtbue')
            webbrowser.open('https://www.youtube.com')
            continue
        
        elif 'abrir navegador' in pedido:
            hablar_asistente('Claro, estoy en eso')
            webbrowser.open('https://www.google.com')
            continue
        
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        
        elif 'hora es' in pedido:
            pedir_hora()
            continue
        
        elif 'busca en wikipedia' in pedido:
            hablar_asistente('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia','')
            wikipedia.set_lang('es')
            #wikipedia.wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar_asistente('Según Wikipedia dice')
            hablar_asistente(resultado)
            continue

        elif 'busca en internet' in pedido:
            hablar_asistente('Ya estoy en eso')
            pedido = pedido.replace('busca en internet','')
            pywhatkit.search(pedido)
            hablar_asistente('Esto es lo que he encontrado')
            continue

        elif 'reproducir' in pedido:
            hablar_asistente('Subele a esa canción')
            pywhatkit.playonyt(pedido)
            continue
        
        elif 'chiste' in pedido:
            hablar_asistente(pyjokes.get_joke('es'))
            continue
        
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip().title()
            cartera = { 'Apple': 'AAPL',
                        'Microsoft': 'MSFT',
                        'Amazon': 'AMZN',
                        'Tesla': 'TSLA',
                        'Google': 'GOOGL',
                        'Meta': 'META',
                        'Nvidia': 'NVDA',
                        'Netflix': 'NFLX',
                        'Coca Cola': 'KO',
                        'Pepsi': 'PEP',
                        'Disney': 'DIS',
                        'Visa': 'V',
                        'Berkshire Hathaway': 'BRK-B',
                        'JPMorgan Chase': 'JPM',
                        'Johnson & Johnson': 'JNJ',
                        'Procter & Gamble': 'PG',
                        'Pfizer': 'PFE',
                        'Intel': 'INTC',
                        'Ibm': 'IBM',
                        'Goldman Sachs': 'GS'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketDayHigh']
                hablar_asistente(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar_asistente('Perdon no la he encontrado')
                continue
        
        elif 'temperatura en' in pedido:
            # remover_acentos(pedido.split('en')[-1].strip())
            ciudad = remover_acentos(re.split(r'\ben\b | \ben la\b', pedido)[1].strip())
            API_KEY = '###############'
            URL = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&lang=es&units=metric"

            respuesta = requests.get(URL)

            #if respuesta.status_code == 200:
            try:
                datos = respuesta.json()
                clima = datos['weather'][0]['description']
                temperatura = datos['main']['temp']
                hablar_asistente(f"El clima en {ciudad}: {clima}")
                hablar_asistente(f"Temperatura: {round(temperatura)}°C")
                continue
            #else:
            except:
                print("Error al obtener el clima. Verifica el nombre de la ciudad.")
                continue
        
        elif 'convertir' in pedido:
            API_KEY = "##################"
            try:
                monto, moneda_origen, moneda_destino = procesar_conversion(pedido)
                hablar_asistente(f"Convirtiendo {monto} de {moneda_origen} a {moneda_destino}")
                URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{moneda_origen}/{moneda_destino}/{monto}"
                respuesta = requests.get(URL)
                datos = respuesta.json()
                
                if respuesta.status_code == 200:
                    # Extraer el resultado de la conversión
                    conversion = datos['conversion_result']
                    hablar_asistente(f"{monto} {moneda_origen} son equivalentes a {conversion} {moneda_destino}")
                else: 
                    print(f"Error en la conversión: {datos['error-type']}")
                continue
            except:
                print("Error al hacer la solicitud")
                continue
        
        elif "traducir" in pedido or "traduce" in pedido or "translate" in pedido:            
            patron = r'.*\btraducir\b|.*\btraduce\b|.*\btranslate\b'
            texto_traducir = re.sub(patron,"", pedido)
            texto_traducir = re.sub(' +', ' ', texto_traducir).strip().capitalize()
            print(texto_traducir)
            traductor.traducir_y_hablar(texto_traducir)
            continue

        elif 'adiós' in pedido:
            hablar_asistente('Adiós, me ire a descansar, Cualquier cosa me avisas')
            break

## Inicia el asistente virtual
solicitud()
