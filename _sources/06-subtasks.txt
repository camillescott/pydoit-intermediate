Subtasks
========

    .. rubric:: Learning Objectives

    -  Introduce subtasks.
    -  Add a document templating task.

We've defined tasks to download our data, gunzip it, and plot it.
However, our original goal was to create a publication pipeline, so we
should get on with it!

The file actually defining our paper will be written in
`markdown <https://daringfireball.net/projects/markdown/>`__. For the
unititiated, markdown is an extremely simply markup language (like HTML)
designed with the goal of being human readable. Eventually we'll be
using pandoc to compile the markdown document into our format of choice.
However, before we do any of that, we need to add our image file and
other information to the markdown document. We could just include these
things directly in the file, but we're cooler than that -- we want to do
it dynamically. We'll use the
`jinja2 <http://jinja.pocoo.org/docs/dev/>`__ templating library to
build our markdown document dynamically.

Given that this is a course on pydoit and not jinja2, it would be best
if we downloaded the jinja2 template rather than writing it ourselves.
Convenienty, we already have a task for downloading things -- but
currently, it only downloads a single file. "Surely," you say, "this
task must be capable of downloading other files!" And you would be
correct! We can use *subtasks* to generate multiple tasks from the same
task function.

.. code:: python

    import os
    from doit.task include clean_targets

    DATA_URLS = ['https://s3.amazonaws.com/pydoit-intermediate/Melee_data.csv.document.md.tpl',
                 'https://s3.amazonaws.com/pydoit-intermediate/Melee_data.csv.gz']

    def task_download_data():

        def print_url(URL):
            print 'File was retrieved from: {0}'.format(URL)

        for URL in DATA_URLS:
            target = os.path.basename(URL)
            yield {'name': 'download:{0}'.format(target),
                   'actions': ['curl -OL {0}'.format(URL)],
                   'targets': [target],
                   'uptodate': [run_once],
                   'clean': [clean_targets, (print_url, [URL])]}

We've made a number of changes here, but most important is that we've
switched to using a generator object instead of a normal function. For
those of you not familiar with generators, the generator is signified by
the ``yield`` keyword, which takes the place of a ``return`` keyword.
Because this function has a ``yield``, it becomes a generator and can be
iterated over, for example, with a ``for`` loop. For pydoit
specifically, this means it can yield multiple tasks, one for each in
the ``DATA_URLS`` list. We've also included a ``name`` attribute; this
is necessary because pydoit needs the ability to uniquely identify tasks
in order to resolve dependencies.

Now that we have the task to download the template file, we'll add one
to compile the template into a markdown file. This is another python
task, which will include much of what we've gone over already.

.. code:: python

    import jinja2

    # ... the other tasks ...

    def task_build_markdown_file():

        def do_build(targets):
            
            with open(targets[0] + '.tpl') as fp:
                template = jinja2.Template(fp.read())

            with open(targets[0], 'wb') as fp:
                fp.write(template.render(author='Your Name',
                                         affiliation='Your Institution',
                                         date='Jan 20, 2016',
                                         heatmap_filename='Melee_data.csv.heatmap.pdf'))

        return {'actions': [do_build],
                'file_dep': ['Melee_data.csv.heatmap.pdf',
                             'Melee_data.csv.document.md.tpl'],
                'targets': ['Melee_data.csv.document.md'],
                'clean': [clean_targets]}

This task creates a jinja2 ``Template`` object from the template file we
downloaded, then renders it into its final form by passing in a number
of keyword arguments.

    .. rubric:: Fun with Templates

    Although templating isn't specific to pydoit, you may find jinja2
    quite useful. Try playing around with the template ``.tpl`` file and
    adding your own content to it. Can you see how to to add additional
    fields?
