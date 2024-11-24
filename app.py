from fastapi import FastAPI, UploadFile, Form, File
from llama_parse import LlamaParse
from typing import Optional

app = FastAPI()

@app.post("/parse")
async def parse_document(
    file: UploadFile = File(...),
    language: Optional[str] = Form(default="en"),
    target_pages: Optional[str] = Form(default=None)
):
    parser = LlamaParse(
        result_type='markdown',
        language=language,
        target_pages=target_pages
    )
    
    file_content = await file.read()
    
    try:
        documents = await parser.aload_data(
            file_content, 
            {'file_name': file.filename}
        )
        
        return {
            "status": "success",
            "documents": [{'text': doc.text, 'meta': doc.metadata} for doc in documents]
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
    finally:
        await file.close()
