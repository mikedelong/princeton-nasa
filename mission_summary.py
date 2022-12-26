"""
Load and visualize data
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from matplotlib.pyplot import savefig
from matplotlib.pyplot import subplots
from matplotlib.pyplot import tight_layout
from matplotlib.style import use
from pandas import DataFrame
from pandas import read_csv


def read_csv_dataframe(fname: str) -> DataFrame:
    result_df = read_csv(filepath_or_buffer=fname)
    return result_df


INPUT_FILE = 'mission_summary.csv'
INPUT_FOLDER = './data/'
OUTPUT_FOLDER = './plot/'
STYLE = 'fivethirtyeight'

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    for folder in [INPUT_FOLDER]:
        LOGGER.info('creating folder %s if it does not exist', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    input_file = INPUT_FOLDER + INPUT_FILE
    LOGGER.info('reading %s', input_file)
    df = read_csv_dataframe(fname=input_file)

    f, ax = subplots(figsize=(6, 15), )
    use(style=STYLE)
    y_ticks = list()
    df['$/Year'] = df.apply(axis=1, func=lambda x: 0 if x['End'] == x['Launch'] else x['2019 M Total'] / (
            x['End'] - x['Launch']))
    choice = 0
    df['box_height'] = [10, df['$/Year'].astype(int)][choice]
    df['y_coordinate'] = df['box_height'].cumsum()
    for index, row in df.iterrows():
        facecolor = 'C0' if row['End'] != 2019 else 'C2'
        height = (row['y_coordinate'], row['box_height'],)
        ax.broken_barh([(row['Launch'], row['End'] - row['Launch'])], height, facecolor=facecolor)
        y_tick = row['y_coordinate'] + 0.5 * row['box_height']
        y_ticks.append(y_tick)
    ax.set_yticks(y_ticks, labels=df['Name'].values.tolist())
    tight_layout()
    savefig(format='png', fname=OUTPUT_FOLDER + 'mission_summary.png')

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
