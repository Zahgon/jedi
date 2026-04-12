import difflib
from pathlib import Path
from typing import Dict, Iterable, Tuple

from parso import split_lines

from jedi.api.exceptions import RefactoringError
from jedi.inference.value.namespace import ImplicitNSName

EXPRESSION_PARTS = (
    'or_test and_test not_test comparison '
    'expr xor_expr and_expr shift_expr arith_expr term factor power atom_expr'
).split()


class ChangedFile:
    def __init__(self, inference_state, from_path, to_path,
                 module_node, node_to_str_map):
        self._inference_state = inference_state
        self._from_path = from_path
        self._to_path = to_path
        self._module_node = module_node
        self._node_to_str_map = node_to_str_map

    def get_diff(self):
        pass

    def get_new_code(self):
        pass

    def apply(self):
        pass

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self._from_path)


class Refactoring:
    def __init__(self, inference_state, file_to_node_changes, renames=()):
        self._inference_state = inference_state
        self._renames = renames
        self._file_to_node_changes = file_to_node_changes

    def get_changed_files(self) -> Dict[Path, ChangedFile]:
        pass

    def get_renames(self) -> Iterable[Tuple[Path, Path]]:
        """
        Files can be renamed in a refactoring.
        """
        pass

    def get_diff(self):
        pass

    def apply(self):
        """
        Applies the whole refactoring to the files, which includes renames.
        """
        pass


def _calculate_rename(path, new_name):
    pass


def rename(inference_state, definitions, new_name):
    pass


def inline(inference_state, names):
    pass


def _remove_indent_of_prefix(prefix):
    r"""
    Removes the last indentation of a prefix, e.g. " \n \n " becomes " \n \n".
    """
    pass


def _try_relative_to(path: Path, base: Path) -> Path:
    pass
