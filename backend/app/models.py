from pydantic import BaseModel
from typing import Optional, List

class PDFUploadResponse(BaseModel):
    filename: str
    file_id: str
    pages: int
    size: int
    message: str

class TextAddRequest(BaseModel):
    file_id: str
    page_number: int
    text: str
    x: float
    y: float
    font_size: int = 12
    color: str = "#000000"

class TextEditRequest(BaseModel):
    file_id: str
    page_number: int
    old_text: str
    new_text: str
    x: Optional[float] = None
    y: Optional[float] = None

class PDFInfo(BaseModel):
    filename: str
    pages: int
    size: int
    created_at: str

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None