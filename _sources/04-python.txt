Python Tasks
============

    .. rubric:: Learning Objectives

    -  Write a Python task
    -  Expand on automatic variables

So far, we have downloaded the data and gunzipped it. Both of those
tasks were simple shell commands. However, pydoit can do much more than
that; actions can also be arbitrary python code. We will take advantage
of that to do some "analysis" of our Super Smash Bros data and generate
a plot.

Python tasks are defined in the same way as any other task, but the
actions entry will include a function name instead. Python lets us
define functions within functions and access variables from the outer
function's namespace (there are called closures, which are beyond the
scope of this workshop); to make things simpler, we'll define our task
this way.

.. code:: python

    def task_plot_heatmap():

        def do_plot(dependencies, targets):
            import matplotlib.pyplot as plt
            import pandas as pd
            import seaborn as sns

            # Read the data in a DataFrame
            data = pd.read_csv(list(dependencies)[0], index_col=0)
            # Make a heatmap and dendrogram with seaborn
            clst = sns.clustermap(data, linewidths=.5, figsize=(8, 8), square=True,
                                  method='ward', z_score=0, row_cluster=False)
            clst.savefig(targets[0])

        return {'actions': [do_plot],
                'file_dep': ['Melee_data.csv'],
                'targets': ['Melee_data.csv.heatmap.pdf']}

The python action takes two parameters -- ``file_dep`` and ``targets``.
These behave similarly to the *automatic variables* we accessed earlier,
but instead the actual python objects are passed to the function and can
be accessed. It is important to note that only the task function
``task_plot_heatmap`` is executed immediately when we run the pipeline;
the ``do_plot`` function will be defined, and then only executed when
and if the task is determined to be out of date.

Run it and take a look at the output.

Well that sucks.

It's likely that your labels are all garbled and overlapping. Let's add
some code to fix them and rerun it.

.. code:: python

    def task_plot_heatmap():

        def do_plot(dependencies, targets):
            import matplotlib.pyplot as plt
            import pandas as pd
            import seaborn as sns

            data = pd.read_csv(list(dependencies)[0], index_col=0)
            clst = sns.clustermap(data, linewidths=.5, figsize=(8, 8), square=True,
                                  method='ward', z_score=0, row_cluster=False)
            # We like pretty charts, so rotate the labels
            plt.setp(clst.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
            plt.setp(clst.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
            clst.savefig(targets[0])

        return {'actions': [do_plot],
                'file_dep': ['Melee_data.csv'],
                'targets': ['Melee_data.csv.heatmap.pdf']}

It didn't run! That's because we didn't change any of the targets or
dependencies, so as far as doit is concerned, nothing has changed. Not
having the dodo file be a dependency is a design decision defended in
the documentation; in order to regenerate the plot, you'll have to
``rm`` the PDF file and run doit again.
