import sys
from typing import List
from pathlib import Path

from jedi.inference.cache import inference_state_method_cache
from jedi.inference.imports import goto_import, load_module_from_path
from jedi.inference.filters import ParserTreeFilter
from jedi.inference.base_value import NO_VALUES, ValueSet
from jedi.inference.helpers import infer_call_of_leaf

_PYTEST_FIXTURE_MODULES = [
    ('_pytest', 'monkeypatch'),
    ('_pytest', 'capture'),
    ('_pytest', 'logging'),
    ('_pytest', 'tmpdir'),
    ('_pytest', 'pytester'),
]


def execute(callback):
    def wrapper(value, arguments):
        # This might not be necessary anymore in pytest 4/5, definitely needed
        # for pytest 3.
        pass
    return wrapper


def infer_anonymous_param(func):
    pass


def goto_anonymous_param(func):
    pass


def complete_param_names(func):
    def wrapper(context, func_name, decorator_nodes):
        pass
    return wrapper


def _goto_pytest_fixture(module_context, name, skip_own_module):
    pass


def _is_a_pytest_param_and_inherited(param_name):
    """
    Pytest params are either in a `test_*` function or have a pytest fixture
    with the decorator @pytest.fixture.

    This is a heuristic and will work in most cases.
    """
    pass


def _is_pytest_func(func_name, decorator_nodes):
    return func_name.startswith('test') \
        or any('fixture' in n.get_code() for n in decorator_nodes)


def _find_pytest_plugin_modules() -> List[List[str]]:
    """
    Finds pytest plugin modules hooked by setuptools entry points

    See https://docs.pytest.org/en/stable/how-to/writing_plugins.html#setuptools-entry-points
    """
    if sys.version_info >= (3, 8):
        from importlib.metadata import entry_points

        if sys.version_info >= (3, 10):
            pytest_entry_points = entry_points(group="pytest11")
        else:
            pytest_entry_points = entry_points().get("pytest11", ())

        if sys.version_info >= (3, 9):
            return [ep.module.split(".") for ep in pytest_entry_points]
        else:
            # Python 3.8 doesn't have `EntryPoint.module`. Implement equivalent
            # to what Python 3.9 does (with additional None check to placate `mypy`)
            matches = [
                ep.pattern.match(ep.value)
                for ep in pytest_entry_points
            ]
            return [x.group('module').split(".") for x in matches if x]

    else:
        from pkg_resources import iter_entry_points
        return [ep.module_name.split(".") for ep in iter_entry_points(group="pytest11")]


@inference_state_method_cache()
def _iter_pytest_modules(module_context, skip_own_module=False):
    if not skip_own_module:
        yield module_context

    file_io = module_context.get_value().file_io
    if file_io is not None:
        folder = file_io.get_parent_folder()
        sys_path = module_context.inference_state.get_sys_path()

        # prevent an infinite loop when reaching the root of the current drive
        last_folder = None

        while any(folder.path.startswith(p) for p in sys_path):
            file_io = folder.get_file_io('conftest.py')
            if Path(file_io.path) != module_context.py__file__():
                try:
                    m = load_module_from_path(module_context.inference_state, file_io)
                    conftest_module = m.as_context()
                    yield conftest_module

                    plugins_list = m.tree_node.get_used_names().get("pytest_plugins")
                    if plugins_list:
                        name = conftest_module.create_name(plugins_list[0])
                        yield from _load_pytest_plugins(module_context, name)
                except FileNotFoundError:
                    pass
            folder = folder.get_parent_folder()

            # prevent an infinite for loop if the same parent folder is return twice
            if last_folder is not None and folder.path == last_folder.path:
                break
            last_folder = folder  # keep track of the last found parent name

    for names in _PYTEST_FIXTURE_MODULES + _find_pytest_plugin_modules():
        for module_value in module_context.inference_state.import_module(names):
            yield module_value.as_context()


def _load_pytest_plugins(module_context, name):
    from jedi.inference.helpers import get_str_or_none

    for inferred in name.infer():
        for seq_value in inferred.py__iter__():
            for value in seq_value.infer():
                fq_name = get_str_or_none(value)
                if fq_name:
                    names = fq_name.split(".")
                    for module_value in module_context.inference_state.import_module(names):
                        yield module_value.as_context()


class FixtureFilter(ParserTreeFilter):
    def _filter(self, names):
        for name in super()._filter(names):
            # look for fixture definitions of imported names
            if name.parent.type == "import_from":
                imported_names = goto_import(self.parent_context, name)
                if any(
                    self._is_fixture(iname.parent_context, iname.tree_name)
                    for iname in imported_names
                    # discard imports of whole modules, that have no tree_name
                    if iname.tree_name
                ):
                    yield name

            elif self._is_fixture(self.parent_context, name):
                yield name

    def _is_fixture(self, context, name):
        funcdef = name.parent
        # Class fixtures are not supported
        if funcdef.type != "funcdef":
            return False
        decorated = funcdef.parent
        if decorated.type != "decorated":
            return False
        decorators = decorated.children[0]
        if decorators.type == 'decorators':
            decorators = decorators.children
        else:
            decorators = [decorators]
        for decorator in decorators:
            dotted_name = decorator.children[1]
            # A heuristic, this makes it faster.
            if 'fixture' in dotted_name.get_code():
                if dotted_name.type == 'atom_expr':
                    # Since Python3.9 a decorator does not have dotted names
                    # anymore.
                    last_trailer = dotted_name.children[-1]
                    last_leaf = last_trailer.get_last_leaf()
                    if last_leaf == ')':
                        values = infer_call_of_leaf(
                            context, last_leaf, cut_own_trailer=True
                        )
                    else:
                        values = context.infer_node(dotted_name)
                else:
                    values = context.infer_node(dotted_name)
                for value in values:
                    if value.name.get_qualified_names(include_module_names=True) \
                            == ('_pytest', 'fixtures', 'fixture'):
                        return True
        return False
