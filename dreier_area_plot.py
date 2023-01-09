"""
Download NASA data from planetary.org
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from matplotlib.pyplot import cm
from matplotlib.pyplot import legend
from matplotlib.pyplot import savefig
from matplotlib.pyplot import stackplot
from matplotlib.pyplot import subplots
from matplotlib.pyplot import tight_layout
from numpy import linspace
from pandas import DataFrame
from pandas import read_excel


def read_dataframe_excel(arg_io: str, arg_sheet_name: str) -> DataFrame:
    result_df = read_excel(io=arg_io, sheet_name=arg_sheet_name, engine='openpyxl')
    return result_df


INPUT_FILE = 'Planetary Exploration Budget Dataset - The Planetary Society.xlsx'
INPUT_FOLDER = './data/'
OUTPUT_FOLDER = './plot/'
SHEET_NAMES = ['Introduction', 'Mission Costs', 'Timeline', 'Planetary Science Budget Histor',
               'Budget History (inflation adj)', 'Funding by Destination', 'Decadal Totals (inflation adj)',
               'Major Programs, 1994 - current', 'Major Programs, 1960 - 1980', 'Cassini', 'CONTOUR', 'DART', 'DAVINCI',
               'Dawn', 'Deep Impact', 'Deep Space 1', 'Discovery Program', 'Europa Clipper', 'Galileo', 'Genesis',
               'GRAIL', 'InSight', 'Juno', 'LADEE', 'Lucy', 'Lunar Orbiters', 'Lunar Prospector', 'Magellan',
               'Mariner 10', 'Mariner 8 & 9', 'Mariner Program', 'Mars Perseverance', 'Mars Global Surveyor',
               'Mars Observer', 'Mars Odyssey', 'Mars Pathfinder', 'MAVEN', 'Mars Sample Return', 'MESSENGER', 'MER',
               'MPLMCO', 'MRO', 'MSL Curiosity', 'NEAR', 'New Horizons', 'OSIRIS-REx', 'Phoenix', 'Pioneer 10 & 11',
               'Pioneer Venus', 'Pioneer Program', 'Planetary Defense', 'Psyche', 'Ranger', 'SIMPLEx Program',
               'Stardust', 'Surveyor Program', 'Viking', 'VIPER', 'VERITAS', 'Voyager', 'FY 2023', 'FY 2022', 'FY 2021',
               'FY 2020', 'FY 2019', 'FY 2018', 'FY 2017', 'FY 2016', 'FY 2015', 'FY 2014', 'FY 2013', 'FY 2012',
               'FY 2011', 'FY 2010', 'FY 2009', 'FY 2008', 'FY 2007', 'FY 2006', 'FY 2005', 'FY 2004', 'FY 2003',
               'FY 2002', 'FY 2001', 'FY 2000', 'FY 1999', 'FY 1998', 'FY1997', 'FY 1996', 'FY 1995', 'FY 1994',
               'FY 1993', 'FY 1992', 'FY 1991', 'FY 1990', 'FY 1989', 'FY 1988', 'FY 1987', 'FY 1986', 'FY 1985',
               'FY 1984', 'FY 1983', 'FY 1982', 'FY 1981', 'FY 1980', 'FY 1979', 'FY 1978', 'FY 1977', 'FY 1976',
               'FY 1976 TQ', 'FY 1975', 'FY 1974', 'FY 1973', 'FY 1972', 'FY 1971', 'FY 1970', 'FY 1969', 'FY 1968',
               'FY 1967', 'FY 1966', 'FY 1965', 'FY 1964', 'FY 1963', 'FY 1962', 'FY 1961', 'FY 1960', 'FY 1959',
               'NNSI', 'NAICS', 'US Spending & Outlays']

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    for folder in [INPUT_FOLDER]:
        LOGGER.info('creating folder %s if it does not exist', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    input_file = INPUT_FOLDER + INPUT_FILE
    sheet_name = 'Mission Costs'
    LOGGER.info('loading sheet %s from %s', sheet_name, input_file)
    df = read_dataframe_excel(arg_io=input_file, arg_sheet_name=sheet_name)
    df = df.drop(columns=['Unnamed: 0'])
    df = df[~df['Fiscal Year'].isna()].fillna(0)
    # for the moment let's drop our problematic row
    df = df[df['Fiscal Year'] != '1976 TQ']
    LOGGER.info(df.shape)
    f, ax = subplots(figsize=(16, 9), )
    ax.set_prop_cycle(color=cm.plasma(linspace(0, 1, len(df.columns))))

    max_year = df['Fiscal Year'].max() + 1
    min_year = df['Fiscal Year'].min()
    columns = [item for item in df.columns if item != 'Fiscal Year']
    stackplot(
        list(range(min_year, max_year)),
        [df[column].values for column in columns],
        labels=columns,
    )
    legend(loc='upper left', ncol=2)
    fname = OUTPUT_FOLDER + 'dreier_stackplot.png'
    tight_layout()
    LOGGER.info('saving %s', fname)
    savefig(format='png', fname=fname)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
