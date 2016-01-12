---
layout: page
title: Finishing Up
subtitle:
minutes: 20
---

> ## Learning Objectives {.objectives}
>
> * Add the final step to compile the document.
> * Show how to import tasks.


First code block, adding the final task. This block doesn't add any new content,
other than finishing up the document pipeline. Students will be told to change
the extension to an alternative if they don't have a working LaTeX installation.

~~~ {.python}
def task_pandoc():

    cmd = 'pandoc -r markdown+yaml_metadata_block+startnum+fancy_lists'\
          ' -s -S %(dependencies)s -o %(targets)s'

    return {'actions': [cmd],
            'file_dep': ['Melee_data.csv.document.md'],
            'targets': ['Melee_data.csv.document.pdf'],
            'clean': [clean_targets]}
~~~

The final section will show students how to import the `dict_to_task` function
and use it to manually create task objects. We'll give them the following code:

~~~ {.python}
def create_task_object(task_dict_func):
    '''Wrapper to decorate functions returning pydoit
    Task dictionaries and have them return pydoit Task
    objects
    '''
    def d_to_t(*args, **kwargs):
        ret_dict = task_dict_func(*args, **kwargs)
        return dict_to_task(ret_dict)
    return d_to_t
~~~

Which defines a decorator to wrap their task functions with. Once they've done that,
they can import tasks from a separate file and either wrap them again with `task_` functions,
or gather them into a list and pass them to a custom loader:

~~~ {.python}
def run_tasks(tasks, args, config={'verbosity': 0}):
    
    if type(tasks) is not list:
        raise TypeError('tasks must be a list')
   
    class Loader(TaskLoader):
        @staticmethod
        def load_tasks(cmd, opt_values, pos_args):
            return tasks, config
   
    DoitMain(Loader()).run(args)
~~~

This last piece of code will be a jumping off point for including argparse and writing their
own applications. I won't go in to heavy detail here, because this starts to get pretty advanced;
rather, it's meant to show them the extent of what they can accomplish with pydoit.
