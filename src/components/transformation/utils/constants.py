SYS_INSTRUCTIONS = '''Leerás htmls, cada uno perteneciente a una página web que detalla la convocatoria de una oferta laboral para practicante en alguna entidad pública.
    Listarás la información que existe en el html en formato JSON.

    Usa este esquema JSON:

    description_i = {"offer_id": str, "offer_title": str, "vacant": str, "type": str, "entity": str, "to_apply": str, "careers": list[str], specifit_requirements: list[str], "salary": str, "knowledge": list[str], "responsabilities": list[str], "city": str, "location": str, "end_date": str, "url": str}
    Return: list[description_1, description_2, ...]
    Cada string que escribas será en double quotes: "text"

    Donde:
    offer_id: información después del HTML, si no hay, string vacío
    offer_title: si hay, nombre del puesto, si no, string vacío 
    vacant: si hay, número de vacantes, si no, string vacío   
    type: si hay, modalidad de prácticas, si no, string vacío
    entity: si hay, nombre de la entidad, si no, string vacío
    to_apply: si hay, quienes pueden postular (estudiantes o egresados ...) , si no, string vacío
    careers: si hay, solo las carreras de los estudiantes/egresados, si no, lista vacía
    specifit_requirements: si hay, requisitos específicos , si no, lista vacía
    salary: si hay, pago o subvención de la práctica, mostrar solo el monto sin la moneda, si no, string vacío
    knowledge: si hay, conocimientos requeridos para el puesto , si no, lista vacía
    responsabilities: si hay, actividades a realizar para el puesto, si no, lista vacía
    city: información después del HTML, si no hay, string vacío
    location: si hay, lugar específico en donde se desarrollarán las práticas (prácticas para), si no, string vacío
    end_date: si hay, fecha límite para postula en formato dia/mes/año, si no, string vacío
    url: información después del HTML, si no hay, string vacío
    '''