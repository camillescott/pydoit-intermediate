Targets
=======

    .. rubric:: Learning Objectives

    -  Write a task to download the example data.
    -  Understand how targets work.

The first step in our pipeline is to actually get the data. Because
we're all radical open science types, we keep our data freely available
for download. The data we'll use is stored in an `S3
bucket <https://s3.amazonaws.com/pydoit-intermediate/Melee_data.csv.gz>`__.
It is clearly a dataset of great performance: win ratios from a Super
Smash Brothers server! We could just have our users download it on their
own, but we can easily remove this necessity by automating the process
with curl.

If we just doing this on the command line, our command would look
something like this:

.. code:: bash

    $ curl -OL https://s3.amazonaws.com/pydoit-intermediate/Melee_data.csv.gz 

What is going on in this command? It runs a program, ``curl``, giving it
a URL, and creates a file, ``Melee_data.csv``. If we look at the command
as a task to complete, this file is that task's output, and if this file
exists already, we can safely assume that the command has been run. In
doit lingo, we call it the task's *target*, and we call the command
itself the task's *action*. Based on the previous section, you might be
able to guess what this task would look like.

.. code:: python

    def task_download_data():
        return {'actions': ['curl -OL https://s3.amazonaws.com/pydoit-intermediate/Melee_data.csv.gz'],
                'targets': ['Melee_data.csv.gz']}

Open your ``dodo.py`` and add this function to it. Save and run the
``doit`` command. You'll see the task output, followed by the normal
output you'd expect from ``curl``.

.. code:: output

    .  download_data

The dot means that the task was executed. If we run ``doit`` again, the
task will run again. This is because we have specified no dependencies,
and doit will determine that the task is never up to date; we will learn
about dependencies in the next section.

    .. note::

    When we run ``doit``, the current directory is searched for a file
    named ``dodo.py``. That file is searched for tasks which are
    executed. Those familiar with ``make`` might have noticed some
    similarity, where typing ``make`` will search the current directoy
    for a file named ``Makefile``. We will cover alternative ways to
    execute your doit tasks later on.
