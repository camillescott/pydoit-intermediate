Dependencies and Task Status
============================

    .. rubric:: Learning Objectives

    -  Introduce task ``uptodate``
    -  Introduce file dependencies

If you run ``doit`` again, you'll notice that you get the same output as
before -- the dot and task name indicating that the task was run again.
Preferably, we'd like the task not to run once it already has (the file
might be large, for example). pydoit handles this two ways: through
dependencies and the ``uptodate`` function. *File dependencies* are
quite intuitive. The task names the files it depends on, and if any of
those change, the task is rerun. Our download command already adds a bit
of complexity though, because it does not depend on any files. This is
where ``uptodate`` comes in.

``uptodate`` is another entry in the task dictionary. It is a list of
booleans, callables (that is, functions), or strings specifying shell
commands. If any of the ``uptodate`` items evaluates to ``False``, the
task is out-of-date and run.

For our download task, we are going to use a function which is included
in the doit library, ``run_once``. As one might expect, this makes sure
the task is run at least once. Let's add it to our ``dodo.py``.

.. code:: python

    from doit.tools import run_once

    def task_download_data():
        return {'actions': ['curl -OL https://s3.amazonaws.com/pydoit-intermediate/Melee_data.csv.gz'],
                'targets': ['Melee_data.csv.gz'],
                'uptodate': [run_once]}

Now if we run ``doit`` again (twice more, actually), our output will
change.

.. code:: bash

    -- download_data

The dash-dash indicates that the task was determined to be up to date,
and was not executed.

    .. note::

    By default, the task name will be taken from the function defining
    it. We can also define our own task names with the ``name`` entry in
    the task dictionary.

doit's system for determining whether a task is up to date is actually
somewhat complex. The
`documentation <http://pydoit.org/dependencies.html#doit-up-to-date-definition>`__
provides a more detailed list of conditions where a task is **not** up
to date:

-  An uptodate item is (or evaluates to) ``False``
-  A file is added to or removed from file\_dep
-  A file\_dep changed since last successful execution
-  A target path does not exist
-  A task has no file\_dep and uptodate item equal to ``True``

The last of these explains why we need to include the ``uptodate`` entry
in our download task; it has no file dependencies, and so will always be
considered out of date, even if the target exists.

    .. rubric:: Experimenting with uptodate

    What would happen if we changed ``uptodate`` to ``[True]``? How
    about ``[False]``?

Now that we know more about how tasks are considered up to date, let's
introduce a file dependency. The file we downloaded was a gzip archive,
so we'll write a task to extract it. The command we would run in the
shell might be:

.. code:: bash

    $ gunzip Melee_data.csv.gz

This would produce a file called ``Melee_data.csv``. We can see then
that we have a *target* (``Melee_data.csv``), an *action* (running
``gunzip``), and a *file dependency* (``Melee_data.csv.gz``). Let's add
the task to our ``dodo.py``.

.. code:: python

    def task_gunzip_data():
        return {'actions': ['gunzip -c %(dependencies)s > %(targets)s'],
                'targets': ['Melee_data.csv'],
                'file_dep': ['Melee_data.csv.gz']}

On top of the file dependency, this task also introduces *automatic
variables*. These are in the ``actions`` string, and are recognized by
the task creator. This removes redundancy and saves us some code.

When we run ``doit``, we get output showing that only the gunzip task
was executed.

.. code::

    -- download_data
    .  gunzip_data
