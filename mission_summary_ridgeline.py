"""
Load and visualize data
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from matplotlib.gridspec import GridSpec
from matplotlib.pyplot import figure
from matplotlib.pyplot import savefig
from matplotlib.pyplot import tight_layout
from matplotlib.style import use
from numpy import array
from numpy import exp
from numpy import linspace
from numpy import unique
from pandas import DataFrame
from pandas import read_csv
from sklearn.neighbors import KernelDensity
from matplotlib.colors import rgb2hex
from matplotlib.cm import get_cmap

def read_csv_dataframe(fname: str) -> DataFrame:
    result_df = read_csv(filepath_or_buffer=fname)
    return result_df


INPUT_FILE = 'mission_summary.csv'
URL = 'https://raw.githubusercontent.com/petermckeever/mock-data/master/datasets/mock-european-test-results.csv'
INPUT_FOLDER = './data/'
OUTPUT_FOLDER = './plot/'
OUTPUT_FILE = 'mission_summary_ridgeline.png'
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
        for year in range(start, end+1):
            amounts.append(amount)
            missions.append(mission)
            years.append(year)
    df = DataFrame(data={'Mission': missions, 'Year': years, 'Dollars': amounts})

    # https://matplotlib.org/matplotblog/posts/create-ridgeplots-in-matplotlib/
    # df = read_csv(filepath_or_buffer=URL)
    # countries = [x for x in unique(df['country'])]
    missions = [mission for mission in unique(df['Mission'])][:4]
    LOGGER.info('mission count: %d', len(missions))

    cmap = get_cmap('plasma', len(missions))
    colors = [rgb2hex(cmap(color)[:3]) for color in range(cmap.N)]

    use(style=STYLE)
    gs = GridSpec(len(missions), 1)
    fig = figure(figsize=(9, 16))

    ax_objs = []
    kernel = ['cosine', 'epanechnikov', 'exponential', 'gaussian', 'linear', 'tophat', ][5]
    for index, mission in enumerate(missions):
        x = array(df[df['Mission'] == mission]['Year'])
        x_d = linspace(0, 1, 1000)
        kde = KernelDensity(bandwidth=0.03, kernel=kernel)
        kde.fit(x[:, None])
        logprob = kde.score_samples(x_d[:, None])
        # creating new axes object
        ax_objs.append(fig.add_subplot(gs[index:index + 1, 0:]))
        # plotting the distribution
        ax_objs[-1].plot(x_d, exp(logprob), color='#f0f0f0', lw=1)
        ax_objs[-1].fill_between(x_d, exp(logprob), alpha=1, color=colors[index])

        # setting uniform x and y lims
        ax_objs[-1].set_xlim(0, 1)
        ax_objs[-1].set_ylim(0, 2.5)

        # make background transparent
        rect = ax_objs[-1].patch
        rect.set_alpha(0)

        # remove borders, axis ticks, and labels
        ax_objs[-1].set_yticklabels([])

        if mission != missions[-1]:
            ax_objs[-1].set_xticklabels([])
        else:
            ax_objs[-1].set_xlabel('Budget', fontsize=16, fontweight='bold')

        for spline in ['top', 'right', 'left', 'bottom']:
            ax_objs[-1].spines[spline].set_visible(False)
        adj_mission = mission.replace(' ', '\n')
        ax_objs[-1].text(-0.02, 0, adj_mission, fontweight='bold', fontsize=14, ha='right')

    gs.update(hspace=-0.7)
    fig.text(0.07, 0.85, 'Budget', fontsize=20)

    tight_layout()
    savefig(format='png', fname=OUTPUT_FOLDER + OUTPUT_FILE)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
