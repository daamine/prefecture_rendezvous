# Selenium Web Scraping Script for RDV prefecture booking

A booking script that can be used for booking rendez-vous from French prefectures using Python and Selenium.  
Tested on Paris and Yvelines prefecture but might also work with other prefectures as well. You are welcome to adapt and change it.

## Note
- A sound notification is triggered when a RDV page is available. 
- The script only notifies you of the availability of a rendez-vous by ringing, and you must manually finish the rendez-vous steps after the notification. 
- It is recommended to set the timeout between requests to a few minutes (3 minutes by default) to avoid being blocked.

## Requirements
- Python 3
- Selenium
- webdriver-manager
- pygame

## Usage
book.py [-h] --url URL --timeout TIMEOUT


### Optional arguments:
  -h, --help            show this help message and exit
  --url URL             URL of the prefecture booking page
  --timeout TIMEOUT     time to wait between requests (in seconds)

## Steps to run the script
1. Clone this repository `git clone https://github.com/daamine/prefecture_rendezvous.git` and `cd prefecture_rendezvous`  
2. Install the required packages by running `pip install -r requirements.txt`
3. Run the script using the command `python3 book.py --url <link> --timeout <TIMEOUT>`

### Examples:
`python3 book.py --url https://pprdv.interieur.gouv.fr/booking/create/989 --timeout 180`  
`python3 book.py --url https://www.yvelines.gouv.fr/booking/create/20024/0 --timeout 180`
