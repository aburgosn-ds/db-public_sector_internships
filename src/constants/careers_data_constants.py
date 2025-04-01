SYSTEM_INSTRUCTIONS = """
You are a formater machine, specialiced on extracting information from pdfs to a semi-structured format like JSON.
Extraerás información del documento pdf que se adjuntará. Algunas consideraciones para la extracción:

    primer dígito: Campo de Educación
    segundo dígito: Campo Específico
    tercer dígito: Campo Detallado
    cuarto dígito: Carrera 
            
"""
PROMPT_1 = """
Extrae toda la información para los campos de educación 1,2,3,4:
1 Educación
2 Humanidades y Arte
3 Ciencias Sociales, Comerciales y Derecho
4 Ciencias Naturales, Exactas y de la Computación


Usa este esquema JSON:

{
    "CAMPO DE EDUCACIÓN 1": 
    {
        "CAMPO ESPECÍFICO 11": 
        {
            "CAMPO DETALLADO 111": ["carrera1", "carrera2", ...],
            "CAMPO DETALLADO 112": ...
        },
        "CAMPO ESPECÍFICO 12":
        {
            ...
        },
        ...
    },

    "CAMPO DE EDUCACIÓN 2": 
    {
        "CAMPO ESPECÍFICO 21": 
        {
            "CAMPO DETALLADO 211": ["carrera1", "carrera2", ...],
            "CAMPO DETALLADO 212": ...
        },
        "CAMPO ESPECÍFICO 22":
        {
            ...
        },
        ...
    } ,
    ...
}

Extrae toda la información, todos los campos especificos, todos los campos detallados, y todas las carreras para campos específicos
reemplazando el número por el texto que significa, así como en el siguiente ejemplo:

Ejemplo:

{
    "EDUCACIÓN": 
    {
        "EDUCACIÓN INICIAL Y PRIMARIA": 
        {
            "EDUCACIÓN INICIAL": ["EDUCACIÓN BÁSICA, INICIAL Y PRIMARIA", "EDUCACIÓN INICIAL", ...],
            "EDUCACIÓN PRIMARIA": ...
        },
        "EDUCACIÓN SECUNDARIA":
        {
            ...
        },
        ...
    },
    "HUMANIDADES Y ARTE": 
    {
        "HUMANIDADES": 
        {
            "ANTROPOLOGÍA Y ARQUEOLOGÍA": ["ANTROPOLOGÍA", "ANTROPOLOGÍA SOCIAL", ...],
            "HISTORIA": ...,
            ...
        },
        "ARTES":
        {
            ...
        },
        ...
    } ,
    ...
}

Recuerda cerrar el diccionario.
"""
PROMPT_2 = """
Extrae toda la infomración para los campos de educación 5,6,7:
5 Ingeniería, Industria y Construcción
6 Agropecuaria y Veterinaria
7 Ciencias de la Salud

Usa este esquema JSON:

{
    "CAMPO DE EDUCACIÓN 1": 
    {
        "CAMPO ESPECÍFICO 11": 
        {
            "CAMPO DETALLADO 111": ["carrera1", "carrera2", ...],
            "CAMPO DETALLADO 112": ...
        },
        "CAMPO ESPECÍFICO 12":
        {
            ...
        },
        ...
    },

    "CAMPO DE EDUCACIÓN 2": 
    {
        "CAMPO ESPECÍFICO 21": 
        {
            "CAMPO DETALLADO 211": ["carrera1", "carrera2", ...],
            "CAMPO DETALLADO 212": ...
        },
        "CAMPO ESPECÍFICO 22":
        {
            ...
        },
        ...
    } ,
    ...
}

Extrae toda la información, todos los campos especificos, todos los campos detallados, y todas las carreras para campos específicos
reemplazando el número por el texto que significa, así como en el siguiente ejemplo:

Ejemplo:

{
    "EDUCACIÓN": 
    {
        "EDUCACIÓN INICIAL Y PRIMARIA": 
        {
            "EDUCACIÓN INICIAL": ["EDUCACIÓN BÁSICA, INICIAL Y PRIMARIA", "EDUCACIÓN INICIAL", ...],
            "EDUCACIÓN PRIMARIA": ...
        },
        "EDUCACIÓN SECUNDARIA":
        {
            ...
        },
        ...
    },
    "HUMANIDADES Y ARTE": 
    {
        "HUMANIDADES": 
        {
            "ANTROPOLOGÍA Y ARQUEOLOGÍA": ["ANTROPOLOGÍA", "ANTROPOLOGÍA SOCIAL", ...],
            "HISTORIA": ...,
            ...
        },
        "ARTES":
        {
            ...
        },
        ...
    } ,
    ...
}

Recuerda cerrar el diccionario.
"""
PDF_PTH="data\data_tables\Clasificador de Carreras e Instituciones de Educación Superior y Técnico Productivas.pdf"
CAREERS_PATH="data\data_tables\careers.json"