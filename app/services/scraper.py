# app/services/scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import time

class WebsiteScraper:
    def __init__(self):
        self.setup_driver()
        self.screenshots_dir = "screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
    
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def scrape(self, url: str) -> dict:
        try:
            print(f"Starting to scrape URL: {url}")
            self.driver.get(url)
            time.sleep(2)  # Wait for dynamic content
            
            # Take screenshots
            screenshots = self._take_screenshots()
            
            content = self.driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            
            # Get title from multiple sources
            title = self._get_title(soup)
            if not title:
                h1 = soup.find('h1')
                if h1:
                    title = h1.text.strip()
                else:
                    meta_title = soup.find('meta', {'property': 'og:title'})
                    if meta_title:
                        title = meta_title.get('content', '').strip()
            
            # Get description from multiple sources
            description = self._get_description(soup)
            if not description:
                meta_desc = soup.find('meta', {'property': 'og:description'})
                if meta_desc:
                    description = meta_desc.get('content', '').strip()
            
            # Get all content
            data = {
                'title': title,
                'description': description,
                'main_content': self._get_main_content(soup),
                'images': self._get_images(soup),
                'screenshots': screenshots,
                'sections': self._get_sections(soup),
                'features': self._get_features(soup),
                'colors': self._get_colors(soup)
            }
            
            print(f"Scraped data: {data}")
            return data
            
        except Exception as e:
            print(f"Error scraping website: {str(e)}")
            raise
        finally:
            self.driver.quit()

    def _get_title(self, soup):
        title = soup.find('title')
        if title:
            title_text = title.text.strip()
            print(f"Found title: {title_text}")
            return title_text
        return ''

    def _get_description(self, soup):
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc = meta_desc.get('content').strip()
            print(f"Found description: {desc}")
            return desc
        return ''

    def _get_main_content(self, soup):
        content_text = ""
        # Try different common content containers
        for tag in ['article', 'main', '.content', '.post-content', '#main-content']:
            content = soup.select(tag)
            if content:
                paragraphs = content[0].find_all('p')
                content_text = ' '.join([p.text.strip() for p in paragraphs])
                if content_text:
                    break
        return content_text

    def _get_images(self, soup):
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                if not src.startswith('http'):
                    if src.startswith('//'):
                        src = f"https:{src}"
                    elif src.startswith('/'):
                        src = f"https://{self.driver.current_url.split('/')[2]}{src}"
                    else:
                        src = f"https://{self.driver.current_url.split('/')[2]}/{src}"
                print(f"Found image: {src}")
                images.append(src)
        return images

    def _take_screenshots(self) -> dict:
        screenshots = {}
        
        # Full page screenshot
        full_path = os.path.join(self.screenshots_dir, "full_page.png")
        self.driver.save_screenshot(full_path)
        screenshots['full'] = full_path
        
        # Above the fold screenshot
        fold_path = os.path.join(self.screenshots_dir, "above_fold.png")
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        self.driver.save_screenshot(fold_path)
        screenshots['above_fold'] = fold_path
        
        # Try to get hero section if exists
        try:
            hero = self.driver.find_element(By.CLASS_NAME, 'hero') or \
                   self.driver.find_element(By.ID, 'hero') or \
                   self.driver.find_element(By.TAG_NAME, 'header')
            
            hero_path = os.path.join(self.screenshots_dir, "hero.png")
            hero.screenshot(hero_path)
            screenshots['hero'] = hero_path
        except:
            pass
        
        return screenshots

    def _get_sections(self, soup) -> list:
        sections = []
        for section in soup.find_all(['section', 'div']):
            if section.get('class') or section.get('id'):
                text = section.get_text(strip=True)
                if len(text) > 50:  # Only meaningful sections
                    sections.append({
                        'text': text,
                        'type': section.name,
                        'class': section.get('class', []),
                        'id': section.get('id', '')
                    })
        return sections

    def _get_features(self, soup) -> list:
        features = []
        feature_identifiers = [
            'feature', 'benefit', 'service', 'product',
            'card', 'item', 'highlight'
        ]
        
        for feature in soup.find_all(['div', 'section', 'article']):
            classes = ' '.join(feature.get('class', [])).lower()
            if any(id in classes for id in feature_identifiers):
                title_elem = feature.find(['h1', 'h2', 'h3', 'h4'])
                features.append({
                    'title': title_elem.text.strip() if title_elem else '',
                    'description': feature.get_text(strip=True),
                    'image': feature.find('img').get('src') if feature.find('img') else None
                })
        return features

    def _get_colors(self, soup) -> list:
        styles = soup.find_all('style')
        colors = set()
        import re
        
        for style in styles:
            if style.string:
                hex_colors = re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}', style.string)
                colors.update(hex_colors)
                
                rgb_colors = re.findall(r'rgb\([^)]+\)', style.string)
                colors.update(rgb_colors)
        
        return list(colors)