from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from .converter import pdf_to_epub
import io

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(400, detail="Invalid file type. Please upload a PDF file.")
    
    contents = await file.read()
    try:
        epub_file = pdf_to_epub(contents, file.filename)
        return StreamingResponse(
            io.BytesIO(epub_file.getvalue()),
            media_type="application/epub+zip",
            headers={"Content-Disposition": f"attachment; filename={file.filename.rsplit('.', 1)[0]}.epub"}
        )
    except Exception as e:
        raise HTTPException(500, detail=str(e))
