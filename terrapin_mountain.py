"""
Scatter plot of age vs finishing tome
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from matplotlib.pyplot import Axes
from matplotlib.pyplot import close
from matplotlib.pyplot import gca
from matplotlib.pyplot import savefig
from matplotlib.pyplot import subplots
from matplotlib.pyplot import tight_layout
from pandas import Series
from pandas import concat
from pandas import read_csv
from seaborn import lmplot
from seaborn import set_style

from json import load

def get_hours(arg: str) -> float:
    pieces = arg.split(':')
    seconds = 3600 * int(pieces[0]) + 60 * int(pieces[1]) + float(pieces[2])
    return seconds / 3600


# https://stackoverflow.com/questions/46027653/adding-labels-in-x-y-scatter-plot-with-seaborn
def label_point(x: Series, y: Series, val: Series, ax: Axes):
    rows_df = concat({'x': x, 'y': y, 'value': val}, axis=1)
    for i, point in rows_df.iterrows():
        ax.text(point['x'] + 0.03, point['y'] + 0.01, str(point['value']), fontsize='x-small')
    return


def map_changes(name: str, sex: str, changes: dict) -> str:
    return sex if name not in changes.keys() else changes[name]

def parse_age_group(arg) -> str:
    if isinstance(arg, float):
        return 'Unknown'
    pieces = arg.split()
    key = pieces[0].split(':')[1]
    if key == 'M':
        return 'Male'
    elif key == 'F':
        return 'Female'
    else:
        return 'Unknown'


FIXES_FILE = 'terrapin_mountain_fixes.json'
INPUT_FILE = '2022 Terrapin 50K_.csv'
INPUT_FOLDER = './data/'
OUTPUT_FOLDER = './plot/'
SEABORN_STYLE = 'darkgrid'

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

    fixes_file = INPUT_FOLDER + FIXES_FILE
    with open(file=fixes_file, mode='r') as input_fp:
        fixes = load(fp=input_fp)
    LOGGER.info('loaded name/sex fixes from %s', fixes_file)
    df['Hours'] = df['Chip Time'].apply(get_hours)
    df['Sex'] = df['Age Group Place'].apply(parse_age_group)
    df['Sex'] = df.apply(axis=1, func=lambda x: map_changes(x['Name'], x['Sex'], fixes))

    set_style(style=SEABORN_STYLE)
    figure_scatterplot, axes_scatterplot = subplots()
    result_scatterplot = lmplot(aspect=2, data=df, fit_reg=True, hue='Sex', legend=True, x='Age', y='Hours', )
    label_point(x=df['Age'], y=df['Hours'], val=df['Name'], ax=gca())
    tight_layout()
    file_scatterplot = OUTPUT_FOLDER + '{}_scatterplot.png'.format('terrapin_mountain_2022')
    savefig(fname=file_scatterplot, format='png')
    LOGGER.info('wrote to %s', file_scatterplot)
    close(fig=figure_scatterplot)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
