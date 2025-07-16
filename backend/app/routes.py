from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
from datetime import datetime
from models import PDFUploadResponse, TextAddRequest, APIResponse, PDFInfo
from utils import PDFProcessor

router = APIRouter()

# Almacenamiento temporal en memoria (en producción usar base de datos)
uploaded_files = {}

@router.post("/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Subir un archivo PDF"""
    try:
        # Validar que sea PDF
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

        # Generar ID único
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{file.filename}"
        filepath = os.path.join("uploads", filename)

        # Leer contenido del archivo
        content = await file.read()

        # Guardar archivo
        with open(filepath, "wb") as buffer:
            buffer.write(content)

        # Procesar PDF después de guardar
        try:
            processor = PDFProcessor(filepath)
            pages = processor.get_page_count()
        except Exception as pdf_error:
            # Si hay error al procesar, eliminar archivo y mostrar error específico
            if os.path.exists(filepath):
                os.remove(filepath)
            raise HTTPException(status_code=400, detail=f"Error al procesar PDF: {str(pdf_error)}")

        size = len(content)

        # Almacenar información
        uploaded_files[file_id] = {
            "filename": file.filename,
            "filepath": filepath,
            "pages": pages,
            "size": size,
            "created_at": datetime.now().isoformat()
        }

        return PDFUploadResponse(
            filename=file.filename,
            file_id=file_id,
            pages=pages,
            size=size,
            message="PDF subido exitosamente"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/pdf-info/{file_id}", response_model=PDFInfo)
async def get_pdf_info(file_id: str):
    """Obtener información del PDF"""
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="PDF no encontrado")

    info = uploaded_files[file_id]
    return PDFInfo(**info)

@router.post("/add-text", response_model=APIResponse)
async def add_text_to_pdf(request: TextAddRequest):
    """Añadir texto a un PDF"""
    try:
        if request.file_id not in uploaded_files:
            raise HTTPException(status_code=404, detail="PDF no encontrado")

        file_info = uploaded_files[request.file_id]
        processor = PDFProcessor(file_info["filepath"])

        # Añadir texto
        success = processor.add_text(
            page_number=request.page_number,
            text=request.text,
            x=request.x,
            y=request.y,
            font_size=request.font_size,
            color=request.color
        )

        if success:
            return APIResponse(
                success=True,
                message="Texto añadido exitosamente"
            )
        else:
            raise HTTPException(status_code=500, detail="Error al añadir texto")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{file_id}")
async def download_pdf(file_id: str):
    """Descargar PDF modificado"""
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="PDF no encontrado")

    file_info = uploaded_files[file_id]
    filepath = file_info["filepath"]

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return FileResponse(
        path=filepath,
        filename=file_info["filename"],
        media_type="application/pdf"
    )

@router.delete("/delete/{file_id}", response_model=APIResponse)
async def delete_pdf(file_id: str):
    """Eliminar PDF"""
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="PDF no encontrado")

    file_info = uploaded_files[file_id]
    filepath = file_info["filepath"]

    # Eliminar archivo
    if os.path.exists(filepath):
        os.remove(filepath)

    # Eliminar de memoria
    del uploaded_files[file_id]

    return APIResponse(
        success=True,
        message="PDF eliminado exitosamente"
    )