# scrape-the-current
Python web scraper for [The Current (KCMP)](https://www.thecurrent.org/playlist/) radio station's online playlist.

### Install dependencies
```
pip install requirements.txt
```

### Run script
To download The Current's playlist history, run web_scraper.py with Python (developed in Python 3.7).
```
python web_scraper.py
```
Data is periodically stored in CSV files within the project's output directory. Each CSV contains one month's worth of data, with the filename formatted as such: playlist_YYYY_M.csv



## TO-DO 
* Add command line interface to choose start/end dates and output directory
* Create new module to analyze data.
