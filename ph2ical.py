import logging
from bs4 import BeautifulSoup
import sys
import requests
from datetime import datetime
from icalendar import Calendar, Event

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    # get source code from publicholidays.com
    year = sys.argv[1]
    url = f'https://publicholidays.ch/bern/{year}-dates/'
    r = requests.get(url)
    log.info(f'GET {url} STATUS-CODE={r.status_code}')
    html = r.text

    # parse the source code for holidays
    holidays = []
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'publicholidays phgtable'})
    tablebody = table.find('tbody')
    for row in tablebody.find_all('tr'):
        holiday = row.find_all('td')
        if len(holiday) == 3:
            daymonth = holiday[0].text.lstrip('0')
            date = datetime.strptime(f'{daymonth} {year}', '%d %b %Y').date()
            day = date.strftime('%a')
            log.info(f'parsed holiday from webpagge: {day}, {date} ({holiday[2].text.strip()})')
            holidays.append(date)
    
    # create ical file
