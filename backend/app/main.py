from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from routes import router

app = FastAPI(title="PDF Editor API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear directorios si no existen
os.makedirs("uploads", exist_ok=True)
os.makedirs("temp", exist_ok=True)

# Montar archivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

# Incluir rutas
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "PDF Editor API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)