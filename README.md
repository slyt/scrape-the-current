# scrape-the-current
Python web scraper for [The Current (KCMP)](https://www.thecurrent.org/playlist/) radio station's online playlist.

### Install dependencies
```
pip install requirements.txt
```

### Run Scrape
To download The Current's playlist history, run web_scraper.py with Python (developed in Python 3.7).
```sh
python web_scraper.py
```
Data is periodically stored in CSV files within the project's output directory. Each CSV contains one month's worth of data, with the filename formatted as such: `playlist_YYYY_M.csv`, for example `output/playlist_2006_5.csv`

### Post Processing
I order to visualize the data efficiently, post-processing is done on the raw scraped data to prepare it for visualization.

```sh
python process_top_songs_all_time.py
```

### Visualizing

Streamlit and plotly are used to visualize data:
```sh
streamlit start app.py
```




