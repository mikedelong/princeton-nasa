"""
Load and visualize data
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from matplotlib.pyplot import gca
from matplotlib.pyplot import savefig
from numpy import tile
from numpy.random import RandomState
from pandas import DataFrame
from pandas import read_csv
from seaborn import FacetGrid
from seaborn import cubehelix_palette
from seaborn import histplot
from seaborn import kdeplot
from seaborn import set_theme


def read_csv_dataframe(fname: str) -> DataFrame:
    result_df = read_csv(filepath_or_buffer=fname)
    return result_df


# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = gca()
    ax.text(0, .2, label, fontweight='bold', color=color, ha='left', va='center', transform=ax.transAxes)


INPUT_FILE = 'mission_summary.csv'
INPUT_FOLDER = './data/'
OUTPUT_FOLDER = './plot/'
OUTPUT_FILE = 'demo_seaborn_ridgeplot.png'

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    for folder in [INPUT_FOLDER]:
        LOGGER.info('creating folder %s if it does not exist', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    set_theme(style='white', rc={'axes.facecolor': (0, 0, 0, 0)})


    case  = 2
    if case == 0:
        # Create the data
        rs = RandomState(1)
        x = rs.randn(500)
        g = tile(list('ABCDEFGHIJ'), 50)
        df = DataFrame(dict(x=x, g=g))
        m = df.g.map(ord)
        df['x'] += m

        # Initialize the FacetGrid object
        pal = cubehelix_palette(10, rot=-.25, light=.7)
        g = FacetGrid(df, row='g', hue='g', aspect=15, height=.5, palette=pal)

        # Draw the densities in a few steps
        g.map(kdeplot, 'x', bw_adjust=.5, clip_on=False, fill=True, alpha=1, linewidth=1.5)
        g.map(kdeplot, 'x', clip_on=False, color='w', lw=2, bw_adjust=.5)

        # passing color=None to refline() uses the hue mapping
        g.refline(y=0, linewidth=2, linestyle='-', color=None, clip_on=False)
        g.map(label, 'x')

        # Set the subplots to overlap
        g.figure.subplots_adjust(hspace=-.25)

        # Remove axes details that don't play well with overlap
        g.set_titles('')
        g.set(yticks=[], ylabel='')
        g.despine(bottom=True, left=True)
    elif case == 1:

        input_file = INPUT_FOLDER + INPUT_FILE
        raw_df = read_csv_dataframe(fname=input_file)

        raw_df = raw_df.dropna()
        raw_df['$/Year'] = raw_df.apply(axis=1, func=lambda x: 0 if x['End'] == x['Launch'] else x['2019 M Total'] / (
                x['End'] - x['Launch']))
        amounts = list()
        missions = list()
        years = list()
        for index, row in raw_df.iterrows():
            mission = row['Name']
            start = row['Launch']
            end = row['End']
            amount = row['$/Year']
            for year in range(start, end + 1):
                amounts.append(amount)
                missions.append(mission)
                years.append(year)
        df = DataFrame(data={'Mission': missions, 'Year': years, 'Dollars': amounts})
        pal = cubehelix_palette(10, rot=-.25, light=.7)
        g = FacetGrid(df, row='Mission', hue='Mission', aspect=15, height=.5, palette=pal)

        # Draw the densities in a few steps
        g.map(kdeplot, 'Dollars', bw_adjust=.5, clip_on=False, fill=True, alpha=1, linewidth=1.5)
        g.map(kdeplot, 'Dollars', clip_on=False, # color='Year',
              lw=2, bw_adjust=.5)

        # passing color=None to refline() uses the hue mapping
        g.refline(y=0, linewidth=2, linestyle='-', color=None, clip_on=False)
        g.map(label, 'Dollars')

        # Set the subplots to overlap
        g.figure.subplots_adjust(hspace=-.25)

        # Remove axes details that don't play well with overlap
        g.set_titles('')
        g.set(yticks=[], ylabel='')
        g.despine(bottom=True, left=True)
    elif case == 2:
        # todo implement case 1 but use a histplot with element = 'step'
        # https://stackoverflow.com/questions/69614677/plot-the-probability-density-function-in-a-way-that-the-output-can-be-a-smooth-c#comment123048714_69614677
        input_file = INPUT_FOLDER + INPUT_FILE
        raw_df = read_csv_dataframe(fname=input_file)

        raw_df = raw_df.dropna()
        raw_df['$/Year'] = raw_df.apply(axis=1, func=lambda x: 0 if x['End'] == x['Launch'] else x['2019 M Total'] / (
                x['End'] - x['Launch']))
        amounts = list()
        missions = list()
        years = list()
        for index, row in raw_df.iterrows():
            mission = row['Name']
            start = row['Launch']
            end = row['End']
            amount = row['$/Year']
            for year in range(start, end + 1):
                amounts.append(amount)
                missions.append(mission)
                years.append(year)
        df = DataFrame(data={'Mission': missions, 'Year': years, 'Dollars': amounts})
        pal = cubehelix_palette(10, rot=-.25, light=.7)
        g = FacetGrid(df, row='Mission', hue='Mission', aspect=15, height=.5, palette=pal)
        # Draw the densities in a few steps
        g.map(histplot, 'Dollars', clip_on=False, fill=True, alpha=1, linewidth=1.5, element='step',)
        g.map(histplot, 'Dollars', clip_on=False, lw=2, element='step')
              # color='Year',

        # passing color=None to refline() uses the hue mapping
        g.refline(y=0, linewidth=2, linestyle='-', color=None, clip_on=False)
        g.map(label, 'Dollars')

        # Set the subplots to overlap
        g.figure.subplots_adjust(hspace=-.25)

        # Remove axes details that don't play well with overlap
        g.set_titles('')
        g.set(yticks=[], ylabel='')
        g.despine(bottom=True, left=True)
    else:
        raise NotImplementedError(case)

    savefig(format='png', fname=OUTPUT_FOLDER + OUTPUT_FILE)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
