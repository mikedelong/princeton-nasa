"""
Download NASA data from planetary.org
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import DataFrame
from pandas import ExcelFile
from pandas import read_excel


def read_dataframe_excel(arg: str, sheet_name: str) -> DataFrame:
    result_df = read_excel(io=arg, sheet_name=sheet_name, engine='openpyxl')
    return result_df


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
    sheet_names = xl.sheet_names
    LOGGER.info(sheet_names)

    df = read_dataframe_excel(arg=input_file, sheet_name='Mission Costs')
    LOGGER.info(df.shape)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
