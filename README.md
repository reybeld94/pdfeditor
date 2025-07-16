# PDF Editor Example

Este proyecto contiene una API sencilla construida con FastAPI para subir y manipular archivos PDF, junto con un front‑end mínimo en HTML/JavaScript para probarla.

## Uso

1. Instalar dependencias de Python (idealmente dentro de un entorno virtual):
   ```bash
   pip install -r requirements.txt
   ```
2. Iniciar el servidor:
   ```bash
   python backend/app/test_server.py
   ```
3. Abrir `web/index.html` en un navegador. Desde ahí se puede subir un PDF y visualizarlo utilizando la ruta que devuelve la API.

### CORS

Los orígenes permitidos pueden configurarse mediante la variable de entorno `ALLOW_ORIGINS`. Por defecto se permite `http://localhost:3000`, pero puede asignarse `*` para aceptar peticiones desde cualquier dominio.
