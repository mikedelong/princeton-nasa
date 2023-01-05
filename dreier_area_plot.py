"""
Download NASA data from planetary.org
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import ExcelFile


INPUT_FILE = 'Planetary Exploration Budget Dataset - The Planetary Society.xlsx'
INPUT_FOLDER = './data/'

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    for folder in [INPUT_FOLDER]:
        LOGGER.info('creating folder %s if it does not exist', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    input_file = INPUT_FOLDER + INPUT_FILE
    engine = 'openpyxl'
    xl = ExcelFile(path_or_buffer=input_file, engine=engine)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
