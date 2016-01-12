---
layout: page
title: pydoit for automation and applications
---

* Open science, reproducible science is good
* We can help make our work reproducible by automating it
* Automation can be tricky and time consuming, so we need tools to help make it easier
* Pydoit!

Our goal is to create a very basic publication workflow with pydoit. The final pipeline
will download the data, create a graph, and compile the document with pandoc, providing a basic
framework for publishing a reproducible paper.

> ## Prerequisites {.prereq}
>
> * Intermediate python knowledge.
> * Intermediate shell proficiency.
> * The ability to install python packages.
> * Familiarity with your favorite text editor. The demo will be on vim, but use what you're comfortable with.

> ## Setup {.prereq}
>
> * Make sure you have Python.
> * Install the necessary python libraries. If you are using Anaconda, you should
>   have several of these already, and can proceed with: `pip install doit seaborn jinja2`.
> * If you're not using Anaconda, install the rest of the dependencies
>   with `pip install matplotlib pandas`.
> * Install [pandoc](http://pandoc.org/installing.html).


## Topics

1.  [Background and Basics](01-basics.html)
2.  [Targets](02-targets.html)
3.  [Dependencies and uptodate](03-dependencies.html)
4.  [Python Tasks](04-python.html)
5.  [Cleanup](05-cleanup.html)
6.  [Subtasks](06-subtasks.html)
7.  [Finishing Up](07-finishing-up.html)

