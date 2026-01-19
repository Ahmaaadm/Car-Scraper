import requests
from bs4 import BeautifulSoup
import re
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class IAAScraper:
    BASE_URL = "https://ca.iaai.com"

    def __init__(self, output_dir="downloads"):
        self.driver = None
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _init_driver(self):
        """Initialize Selenium Chrome driver"""
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

            # Check for Chrome in different locations
            chrome_paths = [
                "/usr/bin/google-chrome-stable",  # Arch Linux
                "/usr/bin/google-chrome",          # Ubuntu/Debian
                "/usr/bin/chromium-browser",       # Chromium
                "/usr/bin/chromium",               # Alpine
            ]

            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_options.binary_location = path
                    break

            # Use webdriver-manager and fix the path issue
            from webdriver_manager.chrome import ChromeDriverManager

            driver_path = ChromeDriverManager().install()

            # Fix: webdriver-manager sometimes returns wrong file path
            if 'THIRD_PARTY_NOTICES' in driver_path or not driver_path.endswith('chromedriver'):
                driver_dir = os.path.dirname(driver_path)
                chromedriver_path = os.path.join(driver_dir, 'chromedriver')
                if os.path.exists(chromedriver_path):
                    driver_path = chromedriver_path

            # Make sure it's executable
            if os.path.exists(driver_path):
                os.chmod(driver_path, 0o755)

            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self.driver

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def scrape_vehicle_page(self, vehicle_url):
        """
        Scrape a single vehicle page and download all images.
        Returns dict with year and folder path.
        """
        try:
            driver = self._init_driver()
            driver.get(vehicle_url)

            # Wait for page to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
            )
            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract year from page
            year = "Unknown"
            title = ""

            # Try to find vehicle title (e.g., "2008 TOYOTA YARIS")
            title_elem = soup.select_one("h1, .vehicle-title, [class*='title']")
            if title_elem:
                title = title_elem.get_text(strip=True)

            # Also check page title
            if not title:
                page_title = soup.select_one("title")
                if page_title:
                    title = page_title.get_text(strip=True)

            # Extract year from title
            year_match = re.search(r'(19|20)\d{2}', title)
            if year_match:
                year = year_match.group()

            # If no year found, search in page text
            if year == "Unknown":
                for text in soup.stripped_strings:
                    match = re.search(r'^(19|20)\d{2}\s+[A-Z]', text)
                    if match:
                        year = match.group()[:4]
                        break

            # Get all image URLs
            image_urls = []
            seen_image_keys = set()

            all_imgs = soup.select("img[src*='vis.iaai'], img[src*='anvis.iaai']")
            for img in all_imgs:
                src = img.get('src') or img.get('data-src')
                if src and 'imageKeys' in src:
                    # Extract image key to avoid duplicates
                    key_match = re.search(r'imageKeys=([^&]+)', src)
                    if key_match:
                        image_key = key_match.group(1)
                        if image_key in seen_image_keys:
                            continue
                        seen_image_keys.add(image_key)

                    # Use good size for download
                    full_src = re.sub(r'width=\d+', 'width=640', src)
                    full_src = re.sub(r'height=\d+', 'height=480', full_src)
                    image_urls.append(full_src)

            print(f"Found year: {year}, images: {len(image_urls)}")

            # Create folder named by year
            folder_path = os.path.join(self.output_dir, year)
            os.makedirs(folder_path, exist_ok=True)

            # Download images
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://ca.iaai.com/',
            }

            downloaded = 0
            for i, url in enumerate(image_urls):
                try:
                    response = requests.get(url, headers=headers, timeout=30)
                    if response.status_code == 200 and 'image' in response.headers.get('content-type', ''):
                        content_type = response.headers.get('content-type', '')
                        ext = '.jpg'
                        if 'png' in content_type:
                            ext = '.png'
                        elif 'webp' in content_type:
                            ext = '.webp'

                        filename = f"image_{i+1:03d}{ext}"
                        filepath = os.path.join(folder_path, filename)

                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        downloaded += 1
                        print(f"Downloaded: {filename}")

                except Exception as e:
                    print(f"Error downloading image {i+1}: {e}")

            print(f"Downloaded {downloaded}/{len(image_urls)} images to {folder_path}")

            return {
                'success': True,
                'year': year,
                'title': title,
                'folder': folder_path,
                'image_count': downloaded,
                'total_images': len(image_urls)
            }

        except Exception as e:
            print(f"Error scraping vehicle page: {e}")
            return {
                'success': False,
                'error': str(e)
            }


# Simple test
if __name__ == "__main__":
    scraper = IAAScraper(output_dir="downloads")
    try:
        # Test with a vehicle page URL
        test_url = "https://ca.iaai.com/vehicle-details/2863311"
        result = scraper.scrape_vehicle_page(test_url)
        print(f"\nResult: {result}")
    finally:
        scraper.close()
