import sys
from os.path import join, dirname, abspath, isdir


def _start_linter():
    """
    This is a pre-alpha API. You're not supposed to use it at all, except for
    testing. It will very likely change.
    """
    pass


def _complete():
    import jedi
    import pdb

    if '-d' in sys.argv:
        sys.argv.remove('-d')
        jedi.set_debug_function()

    try:
        completions = jedi.Script(sys.argv[2]).complete()
        for c in completions:
            c.docstring()
            c.type
    except Exception as e:
        print(repr(e))
        pdb.post_mortem()
    else:
        print(completions)


if len(sys.argv) == 2 and sys.argv[1] == 'repl':
    # don't want to use __main__ only for repl yet, maybe we want to use it for
    # something else. So just use the keyword ``repl`` for now.
    print(join(dirname(abspath(__file__)), 'api', 'replstartup.py'))
elif len(sys.argv) > 1 and sys.argv[1] == '_linter':
    _start_linter()
elif len(sys.argv) > 1 and sys.argv[1] == '_complete':
    _complete()
else:
    print('Command not implemented: %s' % sys.argv[1])
