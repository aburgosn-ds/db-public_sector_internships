SYS_INSTRUCTIONS = '''Leerás htmls, cada uno perteneciente a una página web que detalla la convocatoria de una oferta laboral para practicante en alguna entidad pública del Perú.
    Listarás la información que existe en el html en formato JSON.

    Usa este esquema JSON:

    description_i = {"offer_page_code": int,
    "offer_title": str, 
    "vacants": int,
    "type": str,
    "organization": str,
    "to_apply": str,
    "careers": list[str],
    "specific_requirements": list[str],
    "salary": float,
    "knowledge": list[str],
    "responsabilities": list[str],
    "city": str,
    "specific_location": str,
    "end_date": str,
    "url": str}
    
    Return: list[description_1, description_2, ...]
    Cada string que escribas será en double quotes: "text"

    Donde:
    offer_page_code: información después del HTML; si no hay, 0
    offer_title: si hay, nombre del puesto; si no hay, string vacío 
    vacants: si hay, número de vacantes; si no hay, 0 
    type: si hay, modalidad de prácticas convertido a MAYÚSCULA (PROFESIONAL O PRE-PROFESIONAL); si no hay, string vacío
    organization: si hay, nombre de la entidad pública convertido a MAYÚSCULAS; si no hay, string vacío
    to_apply: si hay, quienes pueden postular (estudiantes o egresados ...) ; si no hay, string vacío
    careers: si hay, solo las carreras conervidas a MAYÚSCULAS de los estudiantes/egresados, cada carrera como elemento de lista; si no hay, lista vacía
    specific_requirements: si hay, requisitos específicos, cada requisito específico como elemento de lista; si no hay, lista vacía
    salary: si hay, pago o subvención de la práctica, mostrar solo el monto sin la moneda; si no hay, 0.0
    knowledge: si hay, conocimientos requeridos para el puesto, cada conocimientos requerido como elemento de lista; si no hay, lista vacía
    responsabilities: si hay, actividades a realizar para el puesto, cada actividad a realizar como elemento de lista; si no hay, lista vacía
    city: información después del HTML, convertido en MAYÚSCULAS si no hay, string vacío
    specific_location: si hay, lugar específico en donde se desarrollarán las práticas (prácticas para); si no hay, string vacío
    end_date: si hay, fecha límite para postular en formato año-mes-día; si no hay, string vacío
    url: información después del HTML; si no hay, string vacío

    Toda la información es en español, así que todos los values serán en español.
    '''