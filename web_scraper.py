import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Directory for storing output
OUTPUT_DIR = 'output'

# Globals
BASE_URL = 'https://www.thecurrent.org/playlist/'

def scrape_page(curr_date):
    """Scrape playlist data for a given date."""
    url = f"{BASE_URL}{curr_date.strftime('%Y-%m-%d')}"
    logger.info(f"Scraping URL: {url}")
    
    page = requests.get(url)
    if page.status_code != 200:
        logger.error(f"Failed to fetch page: {url} (Status code: {page.status_code})")
        return pd.DataFrame()
    
    soup = BeautifulSoup(page.content, 'html.parser')
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

    return pd.DataFrame(songs_data)

def save_to_csv(df, filename):
    """Save DataFrame to CSV."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(filepath, mode='a', header=not os.path.exists(filepath), index=False, encoding='utf-8')
    logger.info(f"Saved data to {filepath}")

def scrape_date_range(start_date, end_date):
    """Scrape playlist data over a date range."""
    curr_date = start_date
    while curr_date <= end_date:
        logger.info(f"Processing date: {curr_date}")
        daily_data = scrape_page(curr_date)
        if not daily_data.empty:
            filename = f"playlist_{curr_date.year}_{curr_date.month}.csv"
            save_to_csv(daily_data, filename)
        curr_date += datetime.timedelta(days=1)

def main():
    start_date = datetime.date(2005, 12, 22)
    end_date = datetime.date(2024, 12, 22)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    scrape_date_range(start_date, end_date)

if __name__ == "__main__":
    main()
