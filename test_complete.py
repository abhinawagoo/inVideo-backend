from app.services.scraper import WebsiteScraper
from app.services.video_generator import VideoGenerator
from moviepy.config import change_settings
import time

# Set your exact ImageMagick path
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

def test_full_process():
    print("\n=== Starting Website to Video Test ===\n")
    
    # Initialize components
    scraper = WebsiteScraper()
    generator = VideoGenerator()
    
    # Test with a website that has more content
    test_url = "https://www.kognics.ai/"  # Using Python.org as it has more content
    
    try:
        # Step 1: Scrape website
        print("1. Scraping website...")
        start_time = time.time()
        content = scraper.scrape(test_url)
        scrape_time = time.time() - start_time
        
        print(f"\nScraping completed in {scrape_time:.2f} seconds")
        print("Content retrieved:")
        print(f"- Title: {content['title']}")
        print(f"- Description length: {len(content.get('description', ''))} chars")
        print(f"- Main content length: {len(content.get('main_content', ''))} chars")
        print(f"- Images found: {len(content.get('images', []))}")
        
        # Step 2: Generate video
        print("\n2. Generating video...")
        start_time = time.time()
        output_path = generator.generate(content)
        generation_time = time.time() - start_time
        
        print(f"\nVideo generation completed in {generation_time:.2f} seconds")
        print(f"Video saved to: {output_path}")
        
        print("\n=== Test Completed Successfully ===")
        
    except Exception as e:
        print(f"\n❌ Error during test: {str(e)}")

if __name__ == "__main__":
    test_full_process()