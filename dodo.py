import glob
import os

input_files = glob.glob('*.rst')

def task_build_html():

    html_files = [fn[:-4] for fn in input_files]

    return {'file_dep': input_files,
            'actions': ['make html'],
            'targets': [os.path.join('_build/html/', fn) for fn in html_files],
            'clean': ['rm -rf _build/html']}

def task_publish():

    cmd_list = ['touch _build/html/.nojekyll',
                'git add _build/',
                'git commit  -m "Generated gh-pages for `git log master -1 '\
                '--pretty=short --abbrev-commit`"',
                'git subtree split --prefix _build/html -b gh-pages',
                'git push -f origin gh-pages:gh-pages',
                'git branch -D gh-pages']

    return {'task_dep': ['build_html'],
            'file_dep': input_files,
            'actions': cmd_list}

