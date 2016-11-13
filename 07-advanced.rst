Advanced doit: Applications
===========================

    .. rubric:: Learning Objectives

    -  Add the final step to compile the document.
    -  Show how to import tasks.

We've gone over basic task definition and execution, and have seen how to
define a simple workflow and run it with `doit`. However, we haven't talked much
about how the tasks are actually executed and what `doit` does. To motivate this discussion,
let's first define our final task, which compiles the document. Hopefully you've already
downloaded pandoc; if not, head back to the home page and follow the link there.

.. code:: python

    def task_pandoc():

        cmd = 'pandoc -r markdown+yaml_metadata_block+startnum+fancy_lists'\
              ' -s -S %(dependencies)s -o %(targets)s'

        return {'actions': [cmd],
                'file_dep': ['Melee_data.csv.document.md'],
                'targets': ['Melee_data.csv.document.pdf'],
                'clean': [clean_targets]}

This task compiles the markdown document into a nice PDF using LaTeX. Running `doit`
after adding this task will have one of two results: either you'll have the PDF document
at the end, or you'll get an error from pandoc. The error will occur if you don't have LaTeX;
it's a big package, and we don't want to make you install it just for this. So, what if we want
the option to choose the file type for the pandoc output, to avoid using LaTeX?

There are two ways to do this. The first way is to use doit's built-in task
`arguments functionality <http://pydoit.org/task_args.html#command-line-variables-doit-get-var>`__.
This method is quite verbose, and documented at the link for the curious. The other way is to
specify your parameters with `argparse <https://docs.python.org/2.7/library/argparse.html>`__. This
will require building a bit of scaffolding, and show you the beginnings of how to write
complex applications with doit. 

When we run our file with the `doit` command, it uses pattern matching to find all functions
starting with "task" and runs the task generator on them. If the task functions aren't captured
by this step, they just return regular old dictionaries, which isn't what we want! To get
around this, we will use the built-in `dict_to_task` function to create a decorator we can apply
to our task functions.

.. code:: python

    from doit.task import dict_to_task

    def make_task(task_dict_func):
        '''Wrapper to decorate functions returning pydoit
        `Task` dictionaries and have them return pydoit `Task`
        objects
        '''
        def d_to_t(*args, **kwargs):
            ret_dict = task_dict_func(*args, **kwargs)
            return dict_to_task(ret_dict)
        return d_to_t

Okay, so what's the point? Using this decorator, we can just define tasks as regular
old functions, decorate them, and execute them with a loader whenever we want. That way, we can
write our own infrastructure instead of relying on the `doit` command. We can write our own 
simple task loader by inheriting from the `TaskLoader` base class, like so:

.. code:: python

    from doit.cmd_base import TaskLoader
    from doit.doit_cmd import DoitMain

    def run_tasks(tasks, args, config={'verbosity': 0}):
        '''Given a list of `Task` objects, a list of arguments,
        and a config dictionary, execute the tasks.
        '''
        
        if type(tasks) is not list:
            raise TypeError('tasks must be of type list.')
       
        class Loader(TaskLoader):
            @staticmethod
            def load_tasks(cmd, opt_values, pos_args):
                return tasks, config
       
        return DoitMain(Loader()).run(args)

If this all seems a little obtuse, don't be alarmed; this is most of what you need to start
writing your own applications with doit. The `TaskLoader` is what parses a file or object and
pulls tasks from it, and we have overridden the `load_tasks` method to take the list
of `Task` objects we're passing in. We then pass this `Loader` to `DoitMain`, which executes
using it. You can read more `here <http://pydoit.org/extending.html#task-loader-customization>`__.

We're now ready to create our application. Create a new file called `myapp.py` (or whatever you'd
like) and copy the above pieces of code into it. Then, copy
the code from `dodo.py` into it and decorate the tasks with `make_task`, like so:

.. code:: python
 
    @make_task
    def gunzip_data():
        return {'actions': ['gunzip -c %(dependencies)s > %(targets)s'],
                'targets': ['Melee_data.csv'],
                'file_dep': ['Melee_data.csv.gz']}

Finally, we'll add the argument parsing. Defined a new function `main`, import argparse, and
add one argument. We'll also modify the `pandoc` function to take an argument.

.. code:: python

    @make_task
    def task_pandoc(outfmt='pdf'):

        cmd = 'pandoc -r markdown+yaml_metadata_block+startnum+fancy_lists'\
              ' -s -S %(dependencies)s -o %(targets)s'

        return {'actions': [cmd],
                'file_dep': ['Melee_data.csv.document.md'],
                'targets': ['Melee_data.csv.document.{fmt}'.format(fmt=outfmt)],
                'clean': [clean_targets]}

    def main():
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument('--outfmt', default='pdf')
        args = parser.parse_args()
        
        tasks = []
        tasks.append(task_download_data())
        tasks.append(task_gunzip_data())
        tasks.append(task_plot_heatmap())
        tasks.append(task_build_markdown_file())
        tasks.append(task_pandoc(outfmt=args.outfmt))

        run_tasks(tasks, ['run'])

    if __name__ == '__main__':
        main()

We can now run this script with a regular python interpreter, like so:

.. code:: bash

    $ python myapp.py --outfmt md

Which will execute the tasks. Unfortunately, we get an error when we run this script!
The reason has to do with our download task, which uses a `yield` statement, and doesn't play
well with the decorator. So, we're going to making this task more generalized by removing
the direct access to the URLs.

.. code:: python

    
    @make_task
    def task_download_data(URL, target=None):

        if target is None:
            target = os.path.basename(URL)

        def print_url(URL):
            print 'File was retrieved from: {0}'.format(URL)

        return {'name': 'download:{0}'.format(target),
                'actions': ['curl -OL {0}'.format(URL)],
                'targets': [target],
                'uptodate': [run_once],
                'clean': [clean_targets, (print_url, [URL])]}

    # ... moar code

    def main():
        # ...
        for URL in DATA_URLS:
            tasks.append(task_download_data(URL))

The final modification we need to make is to add `name` attributes to our tasks,
which are usually taken directly from the function names. Once we're done there,
we'll have a working doit application.

To save some time and any headaches, a final, working form can be :download:`found here 
<_static/myapp.py>`.
