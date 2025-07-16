import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Iniciando servidor PDF Editor API...")
    print("📍 URL: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    print("🔧 Para detener: Ctrl+C")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Recarga automática en desarrollo
        log_level="info"
    )