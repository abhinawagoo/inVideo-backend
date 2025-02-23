# backend/test_scraper.py
from app.services.scraper import WebsiteScraper

def test_scraper():
    scraper = WebsiteScraper()
    # Test with a known website structure
    url = "https://youtube.com"  # We can change this to any website you want to test
    
    try:
        print(f"\nTesting scraper with URL: {url}")
        print("================================")
        
        result = scraper.scrape(url)
        
        print("\nScraping Results:")
        print("================")
        print(f"Title: {result['title']}")
        print(f"Description: {result['description']}")
        print(f"Content Length: {len(result['main_content'])} characters")
        print(f"Number of Images: {len(result['images'])}")
        
        print("\nContent Preview (first 200 chars):")
        print("---------------------------------")
        print(result['main_content'][:200])
        
        print("\nImages found:")
        print("-------------")
        for idx, img in enumerate(result['images'], 1):
            print(f"{idx}. {img}")
            
        return result
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        raise e

if __name__ == "__main__":
    test_scraper()