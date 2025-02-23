# backend/test_video_generator.py
from app.services.scraper import WebsiteScraper
from app.services.video_generator import VideoGenerator

def test_video_creation():
    # First scrape a website
    scraper = WebsiteScraper()
    content = scraper.scrape("https://example.com")
    
    # Generate video
    generator = VideoGenerator()
    try:
        output_path = generator.generate(content)
        print(f"\nVideo generated successfully at: {output_path}")
    except Exception as e:
        print(f"Error generating video: {str(e)}")

if __name__ == "__main__":
    test_video_creation()