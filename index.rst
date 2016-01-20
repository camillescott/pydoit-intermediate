(py)doit for automation
=====================

an intermediate python workshop
-------------------------------

This workshop will teach students how to make use of `doit <http://pydoit.org/index.html>`__
for workflow automation. To accomplish this goal, students will be walked through the creation of
a very basic publication pipeline, which will download data, create a graph, and compile the
document into a PDF with `jinja2 <http://jinja.pocoo.org/docs/dev/>`__ and 
`pandoc <http://pandoc.org/index.html>`__. This means that in addition
to data analysis workflows, students will have a good idea of how to get started with 
reproducible documents, improving their ability to practice open and reproducible research.

For the practically minded, workflow automation can help:

    - Save time rerunning analyses and adding replicates to computation studies.
    - Save computational resources by only running analysis tasks when needed.
    - Self-document your workflow for others.
    - Reduce errors in your analyses by clearly defining *and* executing them step by step.
    - Make you happier and more smug.

Prerequisites
*************

    -  Intermediate python knowledge.
    -  Beginner to intermediate shell proficiency.
    -  The ability to install python packages.
    -  Familiarity with your favorite text editor. The demo will be on
       vim, but use what you're comfortable with.

Setup
*****

    -  Make sure you have python.
    -  Install the necessary python libraries. If you are using
       Anaconda, you should have several of these already, and can
       proceed with: ``pip install doit seaborn jinja2``.
    -  If you're not using Anaconda, install the rest of the
       dependencies with ``pip install matplotlib pandas``.
    -  Install `pandoc <http://pandoc.org/installing.html>`__.

Topics
------

.. toctree::
    :maxdepth: 1

    01-basics
    02-targets
    03-dependencies
    04-python
    05-cleanup
    06-subtasks
    07-advanced

