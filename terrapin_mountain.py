"""
Download NASA data from the Princeton site
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import read_csv


def get_hours(arg: str) -> float:
    pieces = arg.split(':')
    seconds = 3600 * int(pieces[0]) + 60 * int(pieces[1]) + float(pieces[2])
    return seconds/3600

INPUT_FILE = '2022 Terrapin 50K_.csv'
INPUT_FOLDER = './data/'
OUTPUT_FOLDER = './plot/'

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    for folder in [INPUT_FOLDER, OUTPUT_FOLDER]:
        LOGGER.info('creating folder %s if it does not exist', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    input_file = INPUT_FOLDER + INPUT_FILE
    df = read_csv(filepath_or_buffer=input_file)
    LOGGER.info(df.shape)
    LOGGER.info(df.columns.tolist())
    df['Hours'] = df['Chip Time'].apply(get_hours)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
