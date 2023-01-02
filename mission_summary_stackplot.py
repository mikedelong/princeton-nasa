"""
Load and visualize data
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from matplotlib.pyplot import legend
from matplotlib.pyplot import savefig
from matplotlib.pyplot import stackplot
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
    df = df.dropna()

    use(style=STYLE)
    figsizes = {
        'stackplot': (12, 12),
    }
    for chart_type in figsizes.keys():
        f, ax = subplots(figsize=figsizes[chart_type], )
        if chart_type == None:
            fname = None
            raise NotImplementedError(chart_type)
        elif chart_type == 'stackplot':
            # we need to reshape the data to get annual amounts including zero amounts for years
            # where a mission was not funded
            min_year = df['Launch'].min()
            max_year = df['End'].max()
            df['$/Year'] = df.apply(axis=1, func=lambda x: 0 if x['End'] == x['Launch'] else x['2019 M Total'] / (
                    x['End'] - x['Launch']))
            # https://github.com/holtzy/The-Python-Graph-Gallery/blob/master/src/notebooks/251-stacked-area-chart-with-seaborn-style.ipynb
            x = list(range(min_year, max_year))
            y = [[row['$/Year'] if row['Launch'] <= year <= row['End'] else 0
                for year in range(min_year, max_year)]
                 for index, row in df.iterrows()]
            stackplot(x, y, labels=df['Name'].unique())
            legend(loc='upper right')
            fname = OUTPUT_FOLDER + 'mission_summary_stackplot.png'
        else:
            fname = None
            raise NotImplementedError(chart_type)
        tight_layout()
        LOGGER.info('saving %s', fname)
        savefig(format='png', fname=fname)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
