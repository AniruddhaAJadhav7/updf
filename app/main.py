from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .converter import pdf_to_epub
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert(request: Request, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(400, detail="Invalid file type. Please upload a PDF file.")
    
    contents = await file.read()
    try:
        epub_path = pdf_to_epub(contents, file.filename)
        return templates.TemplateResponse("result.html", {"request": request, "epub_filename": os.path.basename(epub_path)})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@app.get("/download/{filename}")
async def download(filename: str):
    file_path = f"temp/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/epub+zip", filename=filename)
    raise HTTPException(404, detail="File not found")