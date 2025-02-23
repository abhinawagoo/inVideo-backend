from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Video, VideoStatus
from app.services.scraper import WebsiteScraper
from app.services.video_generator import VideoGenerator
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/videos", tags=["videos"])

class VideoRequest(BaseModel):
    website_url: str

class VideoResponse(BaseModel):
    id: int
    website_url: str
    status: str
    output_path: Optional[str] = None
    error_message: Optional[str] = None

@router.post("/", response_model=VideoResponse)
async def create_video(request: VideoRequest, db: Session = Depends(get_db)):
    # Create video record
    video = Video(website_url=request.website_url)
    db.add(video)
    db.commit()
    db.refresh(video)
    
    # Start video generation process
    try:
        # Initialize services
        scraper = WebsiteScraper()
        video_generator = VideoGenerator()
        
        # Update status to processing
        video.status = VideoStatus.PROCESSING
        db.commit()
        
        # Scrape website content
        content = scraper.scrape(request.website_url)
        
        # Generate video
        output_path = video_generator.generate(content)
        
        # Update video record with success
        video.status = VideoStatus.COMPLETED
        video.output_path = output_path
        db.commit()
        
    except Exception as e:
        # Update video record with error
        video.status = VideoStatus.FAILED
        video.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))
    
    return video

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video