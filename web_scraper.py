# Web scraper for The Current (KCMP) radio station's online playlist (thecurrent.org).
#
# It gathers information about songs that have been played on the radio (no audio is downloaded).
# Information gathered includes: timestamp of when the song was played, name of song, artist,
# album, URL to album art (if available), and song ID from the radio station's catalogue.
#
# The date range to be scraped can be changed via the main() function.
# First day of data is 2005-12-22: https://www.thecurrent.org/playlist/2005-12-22
# URL format for a given day's playlist: https://www.thecurrent.org/playlist/YYYY-MM-DD
#
# Data is periodically stored in CSV files within the project's output directory.
# This is intended so that you can 'be nice' to their servers and save a local cache of data
# for further processing.
# Each CSV contains one month's worth of data, with the filename formatted as such: playlist_YYYY_M.csv

import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import os

# Globals
base_url = 'https://www.thecurrent.org/playlist/'

def main():
    # First day of data is 2005-12-22
    start_date = datetime.date(2020, 4, 1)  # Year, Month, Day
    end_date = datetime.date(2020, 4, 30)
    if not os.path.exists('output'): # create output directory if it doesn't exist
        os.makedirs('output')
    month_iterator(start_date, end_date)


# Scrape song data for a given date.
# Returns a pandas dataframe with all songs played on that day.
def scrape_data(curr_date):
    df_daily_data = pd.DataFrame(columns=['title',
                                  'artist',
                                  'album',
                                  'album_art_url',
                                  'song_id',
                                  'date_time'])  # pandas dataframe

    url = base_url + str(curr_date)
    print(base_url + str(curr_date))

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Song information is stored in the 'row song' class on the website
    song_elems = soup.find_all(class_='row song')

    # Keep track if the current time is AM or PM
    eleven_pm_completed = False
    morning = False

    # Strip out necessary data for each song on the current day.
    for song in song_elems:
        title_elem = song.find('h5', class_='title')  # Title
        #title = title_elem.text.encode('utf-8').strip()
        title = title_elem.text.strip()

        artist_elem = song.find('h5', class_='artist')  # Artist
        #artist = artist_elem.text.encode('utf-8').strip()
        artist = artist_elem.text.strip()
        # if artist is None: artist = '' # Assume artist is required

        # Album and Album Art link
        album_element = song.find('img', class_='album-art js-lazy')# Album
        if album_element:
            #album = album_element.get('alt', '').encode('utf-8').strip()
            album = album_element.get('alt', '').strip()
            album_art_url = album_element.get('data-src','')
        else:
            album = ''
            album_art_url = ''

        # Song ID from The Current's catalogue
        song_id_elem = song.find('a') # Song ID
        if song_id_elem:
            song_id = song_id_elem.get('href', '')
            if song_id != '':
                song_id = song_id[5:] # strip first five characters ('#song')
        else:
            song_id = ''

        # Detect AM or PM
        # The website does not have 24-hour time, so this funky logic is used to determine
        # if the time is AM or PM. We use the fact that the songs on the page
        # are ordered from newest (at the top) to oldest (at the bottom) [PM on top, AM on bottom].

        time_elem = song.find('time') # Time
        time = time_elem.text.strip()
        time = datetime.datetime.strptime(time + str(curr_date), '%H:%M%Y-%m-%d')

        # Keep track of when the hour switches from 11pm to 10pm.
        if (eleven_pm_completed is False and time.hour < 11):
            eleven_pm_completed = True

        # If we see 11:00 again, and we already scraped 11:00pm, then it must be 11:00am.
        if (eleven_pm_completed == True and time.hour == 11):
            morning = True

        # Add 12 hours to shift non-morning times to PM
        if (morning == False and time.hour !=12):
            time = time + datetime.timedelta(hours=12)

        # Debugging - printing helps throttle requests so as to be nice to the servers.
        #print('---- New Entry ----')
        print(title)
        #print(artist)
        #print(album)
        #print(album_art_url)
        #print(song_id)
        print(time)

        row_dict = {'title': title, 'artist': artist, 'album': album, 'album_art_url': album_art_url, 'song_id': song_id, 'date_time': time}
        df_daily_data = df_daily_data.append(row_dict, ignore_index=True)

    return df_daily_data

# Loop over months and call scrape_date() for each day.
# Append scrape_date() to monthly CSV files: for example, playlist_2005-1.csv, playlist_2005-2
# CSV files are saved to the output directory.
def month_iterator(start_date, end_date):

    # Iterate over Months
    curr_date = start_date
    delta_day = datetime.timedelta(days=1)
    while curr_date <= end_date:

        curr_month = curr_date.month
        curr_year = curr_date.year
        print('Incrementing Month ' + str(curr_month) + str('(Year: ' + str(curr_year) + ')'))
        csv_filename = 'output/playlist_' + str(curr_year) + '-' + str(curr_month) + '.csv'
        print(csv_filename)

        # Iterate over Days in each month
        while curr_date.month == curr_month and curr_date<= end_date: # Iterate until the end of the month

            # Create dataframe for the day
            df_day = scrape_data(curr_date)
            # Append dataframe to CSV (append mode automatically creates file if it doesn't exist)
            with open(csv_filename, 'a', newline='', encoding='utf8') as f: # open in append mode
                df_day.to_csv(f, header=f.tell() == 0, index=False) # only add header if we have empty file

            curr_date += delta_day


if __name__=="__main__":
    main()