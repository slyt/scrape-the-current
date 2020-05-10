# This module analyzes the CSV files scraped via web_scraper.py.

import glob  # Unix style pathname pattern expansion
import pandas as pd
import matplotlib.pyplot as plt

all_files = glob.glob('C:/Users/Hrothgar/Desktop/output/*.csv') # Get all csv files in output directory
data_list = []
for file in all_files:
    #print(file)
    df = pd.read_csv(file, index_col=None)
    data_list.append(df)

df_all = pd.concat(data_list, axis=0, ignore_index=True)
# When web_scraper.py appended to each csv, it would also add the column headers for each day
# therefore we need to remove rows where the title column == title

df_all = df_all[df_all.title != 'title']
#print(df_all.head())
#print(df_all.describe())

# Number of songs ever played
#print('Total songs played: ', df_all.count())



# Top songs and frequency
print('Top songs')
df_playcount = df_all.groupby(['title', 'artist', 'album'])\
      .size()\
      .reset_index(name='count')\
      .sort_values(['count'], ascending=False)
print(df_playcount)
df_playcount.to_csv('analysis_output/top_songs_all_time.csv', index=False)
#print(df_all['title'].value_counts()[:n])

# Top artists
n = 893
print('Top artists')
df_artist_count = df_all.groupby(['artist'])\
      .size()\
      .reset_index(name='count')\
      .sort_values(['count'], ascending=False)
print(df_artist_count)
df_artist_count.to_csv('analysis_output/top_artists_all_time.csv', index=False)


# Top albums
n = 893
print('Top albums')
df_album_count = df_all.groupby(['album', 'artist'])\
      .size()\
      .reset_index(name='count')\
      .sort_values(['count'], ascending=False)
print(df_album_count)
df_album_count.to_csv('analysis_output/top_albums.csv', index=False)

# Plotting
ax = df_playcount.head(100).plot(x='title', y='count', kind='barh')
ax.invert_yaxis() # labels read top-to-bottom
ax.set_xlabel('Play Count')
ax.set_title('100 most frequently played songs on The Current (KCMP)')
plt.show()


# TODO: Qustions to be answered
# - Make a plot over time for each song, artist, or album selected (When were songs popular?)
# - Overlay plots of the most commonly played songs over time       (Compare when song were popular)
# - Plot diversity over time (Number of unique songs per day/month/week (Can we detect radio format changes?)
# - Plot average song length over time (Are songs getting shorter or longer over time?)