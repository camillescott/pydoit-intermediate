Background and Basics
=====================

    .. rubric:: Learning Objectives

    -  Discuss the build system
    -  Write a pydoit hello world

If you've made it this far, I will assume you've been convinced and are prepared to receive
your happiness and smugness, and are ready to dive into doit. 

-  Pydoit it is a task management and automation tool
-  It is similar to build systems like make
-  Tasks are defined individually and executed in order according to
   dependencies, via a directed acyclic graph

.. seealso:: `A comparison between GNU Make and pydoit by Software Carpentry <http://swcarpentry.github.io/bc/intermediate/doit/make-vs-doit.html>`__

For me, it helps to immediately get started with an example. The basic
building blocks of a pydoit workflow are tasks, which encode the work we
would like to get done. Here is an extremely simple task.

.. code:: python

    def task_hello_world():
        return {'actions': ['echo "hello world!" > hello.txt'],
                'targets': ['hello.txt']}

The task is a python function prefixed with ``task``, which returns a
dictionary containing some predefined entries. The ``actions`` entry is
a list of the actual commands we'd like to run, in this case, a single
shell command. The ``targets`` entry is a list of the files output by
this task.

    .. rubric:: Testing your installation

    Create a working directory, and within it, create a script named
    dodo.py. Copy the above function into it, save, and close. Then,
    move to that directory and run ``doit``. This should run the task
    and generate ``hello.txt``.

Of course, hello world doesn't really do anything for us. Throughout
this lesson, we're going to build a pipeline which downloads some data,
plots it with matplotlib, generates a markup file with the chart, and
outputs a final compiled document -- in other words, a barebones version
of a publication pipeline.
