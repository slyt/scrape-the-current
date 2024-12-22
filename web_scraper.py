import httpx
import asyncio
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import os
import logging
from tqdm.asyncio import tqdm
from tenacity import retry, stop_after_attempt, wait_exponential, before_log, after_log

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Directory for storing output
OUTPUT_DIR = 'output'

# Globals
BASE_URL = 'https://www.thecurrent.org/playlist/the-current/'
CONCURRENT_REQUESTS = 25  # Maximum number of concurrent connections

# Retry configuration: up to 5 attempts with exponential backoff
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO),
    reraise=True
)
async def fetch_page(client, curr_date, semaphore):
    """Fetch a single page asynchronously with a semaphore to limit concurrency."""
    async with semaphore:
        url = f"{BASE_URL}{curr_date.strftime('%Y-%m-%d')}"
        logger.info(f"Fetching URL: {url}")
        try:
            response = await client.get(url)
            if response.status_code != 200:
                logger.error(f"Failed to fetch page: {url} (Status code: {response.status_code})")
                return curr_date, None
            return curr_date, response.text
        except Exception as e:
            logger.error(f"Error fetching page: {url}, {e}")
            raise

async def scrape_page(client, curr_date, semaphore):
    """Scrape playlist data for a given date."""
    curr_date, html = await fetch_page(client, curr_date, semaphore)
    if not html:
        return None, pd.DataFrame()
    
    soup = BeautifulSoup(html, 'html.parser')
    playlist_cards = soup.find_all('li', class_='playlist-card')
    
    songs_data = []
    for card in playlist_cards:
        title_elem = card.find('h4', class_='playlist-title')
        artist_elems = card.find_all('div', class_='playlist-artist')
        time_elem = card.find('div', class_='playlist-time')
        album_art_elem = card.find('div', class_='playlist-image').find('img') if card.find('div', class_='playlist-image') else None
        link_elem = title_elem.find('a') if title_elem else None
        
        title = title_elem.text.strip() if title_elem else None
        artists = [artist.text.strip() for artist in artist_elems] if artist_elems else []
        time_str = time_elem.text.strip() if time_elem else None
        album_art_url = album_art_elem['src'] if album_art_elem else None
        song_id = link_elem['href'].split('/')[-1] if link_elem and 'href' in link_elem.attrs else None
        
        # Combine date and time for a full timestamp
        if time_str:
            try:
                timestamp = datetime.datetime.strptime(f"{curr_date} {time_str}", "%Y-%m-%d %I:%M %p")
            except ValueError:
                timestamp = None
        else:
            timestamp = None

        songs_data.append({
            'title': title,
            'artists': ', '.join(artists),
            'album_art_url': album_art_url,
            'timestamp': timestamp,
            'song_id': song_id
        })

    return curr_date, pd.DataFrame(songs_data)

async def scrape_date_range_async(start_date, end_date):
    """Scrape playlist data over a date range asynchronously with throttling."""
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        for curr_date in tqdm(
            [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)],
            desc="Scraping pages",
            unit="page",
            mininterval=1.0
        ):
            _, df = await scrape_page(client, curr_date, semaphore)
            if not df.empty:
                filename = f"playlist_{curr_date.year}_{curr_date.month}.csv"
                save_to_csv(df, filename, curr_date)

def save_to_csv(df, filename, curr_date):
    """Save DataFrame to CSV safely."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    # Append data to the CSV, creating it if it doesn't exist
    df.to_csv(filepath, mode='a', header=not os.path.exists(filepath), index=False, encoding='utf-8')
    logger.info(f"Saved data for {curr_date} to {filepath}")

def main():
    start_date = datetime.date(2005, 12, 22)
    end_date = datetime.date(2006, 12, 31)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    asyncio.run(scrape_date_range_async(start_date, end_date))

if __name__ == "__main__":
    main()
