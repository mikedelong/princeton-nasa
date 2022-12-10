"""
Load and parse Excel data
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import read_csv


DATA_FOLDER = './data/'
OUTPUT_FOLDER = './data/'
URL_ROOT = 'https://dataspace.princeton.edu/bitstream/88435/dsp019593tz25c/'
URLS = {
    'space_science': '1/1.%20NASA%20Space%20Science%20Funding%2c%201959-1999.csv',
    'lunar_and_planetary': '2/2.%20Comparison%20of%20NASA%20Lunar%20and%20Planetary%20Funding%2c%201959-2019.csv',
    'mission_panel': '3/3.%20Mission%20Panel%20Data%2c%201960-2019.csv',
    'mission_summary': '4/4.%20Mission%20Summary%2c%201961-2019.csv'
}

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    for folder in [DATA_FOLDER, OUTPUT_FOLDER]:
        LOGGER.info('creating folder %s if it does not exist', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    for short_name, url in URLS.items():
        filepath_or_buffer = URL_ROOT + url
        df = read_csv(filepath_or_buffer=filepath_or_buffer)
        df.to_csv(OUTPUT_FOLDER + short_name + '.csv')

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
