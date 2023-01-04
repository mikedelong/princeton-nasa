"""
Download NASA data from planetary.org
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path
from urllib.request import urlretrieve

from arrow import now

OUTPUT_FILE = 'Planetary Exploration Budget Dataset - The Planetary Society.xlsx'
OUTPUT_FOLDER = './data/'
URL = 'https://docs.google.com/spreadsheets/d/e/' \
      '2PACX-1vSngWs2AJa9KoPByrpX-XUgqD6UcMdjl3IW1xAW-m3yCvjreNM6d9KFWkshhxE_sPW9JmgmsaV0NwbG/pub?output=xlsx'

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    for folder in [OUTPUT_FOLDER]:
        LOGGER.info('creating folder %s if it does not exist', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    # https://stackoverflow.com/a/56129059
    output_file = OUTPUT_FOLDER + OUTPUT_FILE
    LOGGER.info('downloading file to %s', output_file)
    urlretrieve(url=URL, filename=output_file)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
