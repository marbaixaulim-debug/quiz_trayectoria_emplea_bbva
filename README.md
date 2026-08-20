# Plan de Proyección Profesional – BBVA

## Descripción

El Plan de Proyección Profesional es una herramienta interactiva diseñada para jóvenes que están comenzando su carrera profesional. A partir de una serie de preguntas sobre sus preferencias e intereses, la herramienta identifica un perfil profesional y un área de interés, y los relaciona con diferentes posibilidades de desarrollo dentro de BBVA.

El resultado muestra una de las 35 combinaciones posibles y presenta una trayectoria profesional formada por diferentes puestos reales de BBVA, con el objetivo de mostrar las distintas opciones de crecimiento, especialización y movilidad que pueden existir dentro de la entidad.

## Funcionamiento

La herramienta combina dos dimensiones:

- **Perfil profesional:** Escalador, Aprendiz, Equilibrado, Especialista e Innovador.
- **Área de interés:** Tecnología, Estrategia, Negocio, Finanzas, Sostenibilidad, Personas y Jurídico.

Las respuestas se puntúan y, mediante un sistema de cálculo y desempate, se obtiene la combinación que presenta una mayor afinidad con las respuestas del usuario.

## Estructura del proyecto

El código se divide en varios archivos:

- `app.py`: desarrolla la interfaz y controla el funcionamiento de la aplicación.
- `questions.py`: contiene las preguntas y las puntuaciones asociadas a cada respuesta.
- `scoring.py`: calcula el resultado y aplica el sistema de desempate.
- `outcomes.py`: contiene las 35 posibilidades de desarrollo, incluyendo su descripción y trayectoria profesional.

## Tecnologías utilizadas

- Python
- Streamlit

