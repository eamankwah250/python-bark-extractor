# BARK-Extractor

- `bark_extractor.py`: main app
- `Database.py`: Database class to interact actual database
- `PSTtime.py`: Convert data received time to PST time

## Dependencies

- Chrome browser
- `$ python --version`: Python 3.8.5
- `$ pip show selenium`: Version: 3.141.0
- `$ pip show pytz`: Version: 2021.3
- `$ pip show psycopg2`: Version: 2.9.1

## Database_Schema

To see the Epibark_Database_Schema:

1. open www.draw.io
2. Drag and drop `./Database_Schema/Epibark_Database_Schema.drawio` file

## SetUp

1. Download source code by:
   - `$ git clone https://github.com/heeshin174/bark-extractor`
   - Download Zip file
2. Download Chrome browser
3. Download latest **Python** programming language
   - [Python Download Link](https://www.python.org/downloads/)
4. Install dependencies for project

   - `$ pip install -r requirements.txt`

     or

   - `$ pip install selenium pytz psycopg2`

5. Download **Chrome browser** on your local computer
6. Check your Chrome browser Version
   - Settings -> About Chrome

![chromeVewrsion](./img/chromeVersion.png)

7. Google **chrome driver** and download the correct chrome driver that matches your current chrome version.
   - [ChromeDriver Download Link](https://chromedriver.chromium.org/downloads)
8. Replace current `./chromedriver.exe` to your downloaded `./chromedriver.exe`.
9. Run the program by typing `$ python bark_extractor.py`

## Usage

- Excute Program: `$ python bark_extractor.py`
  - MacOS: `$ python3 bark_extractor.py`
- Terminate Program: `Ctrl + C`
