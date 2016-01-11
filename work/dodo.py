#!/usr/bin/env python

import jinja2
import time
from doit.task import clean_targets

author = 'Camille Scott'
affiliation = 'UC Davis'
cur_date = time.strftime('%Y-%m-%d')

data_url = 'https://gist.githubusercontent.com/camillescott/ee842c1677447f373488/raw/8f22692e65f86b1df497bba3d2779fbe4a3c297d/Project_M_char_win_mat.csv'
data_filename = 'Project_M_char_win_mat.csv'
heatmap_filename = 'Project_M_char_dendro_ward.pdf'
template_filename = 'Project_M_document.md.tpl'
markdown_filename = 'Project_M_document.md'
document_filename = 'Project_M.pdf'


def task_download():

    cmd = 'curl -L {url} > {target}'.format(url=data_url, 
                                            target=data_filename)

    return {'actions': [cmd],
            'targets': [data_filename],
            'uptodate': [True]}

def task_plot_heatmap():

    def do_plot():
        import matplotlib.pyplot as plt
        import pandas as pd
        import seaborn as sns

        data = pd.read_csv(data_filename, index_col=0)
        clst = sns.clustermap(data, linewidths=.5, figsize=(8, 8), square=True,
                              method='ward', z_score=0, row_cluster=False)
        plt.setp(clst.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        plt.setp(clst.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
        clst.savefig(heatmap_filename)

    return {'actions': [do_plot],
            'file_dep': [data_filename],
            'targets': [heatmap_filename],
            'clean': [clean_targets]}


def task_build_markdown_file():

    def do_build():
        
        with open(template_filename) as fp:
            template = jinja2.Template(fp.read())

        with open(markdown_filename, 'wb') as fp:
            fp.write(template.render(author=author,
                                     affiliation=affiliation,
                                     date=cur_date,
                                     heatmap_filename=heatmap_filename))

    return {'actions': [do_build],
            'file_dep': [heatmap_filename,
                         template_filename],
            'targets': [markdown_filename],
            'clean': [clean_targets]}

def task_pandoc():

    cmd = 'pandoc -r markdown+yaml_metadata_block+startnum+fancy_lists'\
          ' -s -S {0} -o {1}'.format(markdown_filename, document_filename)

    return {'actions': [cmd],
            'file_dep': [markdown_filename],
            'targets': [document_filename],
            'clean': [clean_targets]}
