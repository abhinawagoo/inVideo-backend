from app.services.scraper import WebsiteScraper
import time

def test_scraper_only():
    print("\n=== Testing Website Scraper ===\n")
    
    scraper = WebsiteScraper()
    test_url = "https://example.com"
    
    try:
        print("Scraping website...")
        start_time = time.time()
        content = scraper.scrape(test_url)
        scrape_time = time.time() - start_time
        
        print(f"\nScraping completed in {scrape_time:.2f} seconds")
        print("Content retrieved:")
        print(f"- Title: {content['title']}")
        print(f"- Description length: {len(content['description'])} chars")
        print(f"- Main content length: {len(content['main_content'])} chars")
        print(f"- Images found: {len(content['images'])}")
        
    except Exception as e:
        print(f"\n❌ Error during test: {str(e)}")
        raise e

if __name__ == "__main__":
    test_scraper_only()