from doit.tools import run_once
from doit.task import clean_targets

DATA_URL = 'https://s3.amazonaws.com/pydoit-intermediate/Melee_data.csv.gz'

def task_download_data():

    def print_url():
        print 'File was retrieved from: {0}'.format(DATA_URL)

    return {'actions': ['curl -OL {0}'.format(DATA_URL)],
             'targets': ['Melee_data.csv.gz'],
             'uptodate': [run_once],
             'clean': [clean_targets, print_url]}

def task_gunzip_data():
    return {'actions': ['gunzip -c %(dependencies)s > %(targets)s'],
            'targets': ['Melee_data.csv'],
            'file_dep': ['Melee_data.csv.gz']}

def task_plot_heatmap():

    def do_plot(dependencies, targets):
        import matplotlib.pyplot as plt
        import pandas as pd
        import seaborn as sns

        data = pd.read_csv(list(dependencies)[0], index_col=0)
        clst = sns.clustermap(data, linewidths=.5, figsize=(8, 8), square=True,
                              method='ward', z_score=0, row_cluster=False)
        # I'm a stickler, so rotate the labels nicely
        plt.setp(clst.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        plt.setp(clst.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
        clst.savefig(targets[0])

    return {'actions': [do_plot],
            'file_dep': ['Melee_data.csv'],
            'targets': ['Melee_data.csv.heatmap.pdf']}
