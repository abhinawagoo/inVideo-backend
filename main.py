from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.scraper import WebsiteScraper

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebsiteRequest(BaseModel):
    url: str

@app.post("/api/scrape")
async def scrape_website(request: WebsiteRequest):
    scraper = WebsiteScraper()
    content = scraper.scrape(request.url)
    return content

@app.get("/")
def read_root():
    return {"message": "Website to Video API"}