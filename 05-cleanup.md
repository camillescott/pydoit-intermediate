---
layout: page
title: Cleaning
subtitle: 
minutes: 20
---

> ## Learning Objectives {.objectives}
>
> * Learn how to use the `clean` attribute.
> * Define a custom clean function.

In the last section, we changed the heatmap plotting function and had to manually remove
the target to have it regenerated. Wouldn't it be nice to not have to do that? Yes, yes it would!

The best way to accomplish this is via the `clean` attribute. As one might guess, the `clean`
attribute should be a function which cleans up after the task. Conveniently, the project creator
has included an extremely useful function for this, called `clean_targets`, which just goes
ahead and `rm`'s the target for that task. Here's what it looks like included in our
humble download task.

~~~ {.python}
from doit.task include clean_targets

def task_download_data():
     return {'actions': ['curl -OL https://s3.amazonaws.com/pydoit-intermediate/Melee_data.csv.gz'],
             'targets': ['Melee_data.csv.gz'],
             'uptodate': [run_once],
             'clean': [clean_targets]}
~~~

Now, if we run `doit clean`, the data file will be removed; if we run `doit`, all the tasks
will be rerun, because they all depend directly or indirectly on the downloaded data file.

> ## Cleaning targets {.callout}
>
> Pydoit's creator clearly saw that removing the targets would be an extremely common task.
> As such, one does not actually need to import the `clean_targets` function; just passing
> `[True]` to `clean` will suffice. However, if you would like both remove the targets *and*
> do something else to revert your task, the list should include `clean_targets` and whatever
> other callable or string you'd like run.

`clean` can also be a shell command or function that the user defines. For example, we might want
to inform the user where the pipeline got the file they just blew away.

~~~ {.python}
DATA_URL = 'https://s3.amazonaws.com/pydoit-intermediate/Melee_data.csv.gz'

def task_download_data():

    def print_url():
        print 'File was retrieved from: {0}'.format(DATA_URL)

    return {'actions': ['curl -OL {0}'.format(DATA_URL)],
             'targets': ['Melee_data.csv.gz'],
             'uptodate': [run_once],
             'clean': [clean_targets, print_url]}
~~~

The `clean` attribute takes the same form as `actions` or even `uptodate`, and so can also
be a string to be executed in the shell.

> ## Clean all the things {.challenge}
>
> Add `clean` attributes to all the currently defined tasks. If you'd like, get creative
> with your attributes. Include two clean actions in at least one of the tasks (the second
> doesn't have to do anything groundbreaking).
