from fastapi import FastAPI, Query, HTTPException
from app.services import extract_metadata, extract_article

app = FastAPI(
    title="Metadata + Article Extractor API",
    description="Simple SaaS API for website metadata and article extraction",
    version="1.0.0"
)

@app.get("/WAExtractor/ping")
def root():
    return {"status": "ok", "message": "Metadata & Article Extractor API running"}

@app.get("/meta")
def get_metadata(url: str = Query(..., description="Website URL")):
    try:
        data = extract_metadata(url)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/article/extract")
def get_article(url: str = Query(..., description="Article URL")):
    try:
        data = extract_article(url)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
