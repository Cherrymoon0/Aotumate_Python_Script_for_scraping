import logging
from pathlib import Path

BASE_DIR = Path('/home/ec2-user/Automate_Python_Script_for_scraping')
logging.basicConfig(filename=BASE_DIR / 'app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
try:
    logging.info('Successfully scraped website')
except Exception as e:
    logging.error('This will get logged to a file')    