from textwrap import dedent

from parso import split_lines

from jedi import debug
from jedi.api.exceptions import RefactoringError
from jedi.api.refactoring import Refactoring, EXPRESSION_PARTS
from jedi.common import indent_block
from jedi.parser_utils import function_is_classmethod, function_is_staticmethod


_DEFINITION_SCOPES = ('suite', 'file_input')
_VARIABLE_EXCTRACTABLE = EXPRESSION_PARTS + \
    ('atom testlist_star_expr testlist test lambdef lambdef_nocond '
     'keyword name number string fstring').split()


def extract_variable(inference_state, path, module_node, name, pos, until_pos):
    pass


def _is_expression_with_error(nodes):
    """
    Returns a tuple (is_expression, error_string).
    """
    pass


def _find_nodes(module_node, pos, until_pos):
    """
    Looks up a module and tries to find the appropriate amount of nodes that
    are in there.
    """
    pass


def _replace(nodes, expression_replacement, extracted, pos,
             insert_before_leaf=None, remaining_prefix=None):
    # Now try to replace the nodes found with a variable and move the code
    # before the current statement.
    pass


def _expression_nodes_to_string(nodes):
    pass


def _suite_nodes_to_string(nodes, pos):
    pass


def _split_prefix_at(leaf, until_line):
    """
    Returns a tuple of the leaf's prefix, split at the until_line
    position.
    """
    pass


def _get_indentation(node):
    pass


def _get_parent_definition(node):
    """
    Returns the statement where a node is defined.
    """
    pass


def _remove_unwanted_expression_nodes(parent_node, pos, until_pos):
    """
    This function makes it so for `1 * 2 + 3` you can extract `2 + 3`, even
    though it is not part of the expression.
    """
    pass


def _is_not_extractable_syntax(node):
    pass


def extract_function(inference_state, path, module_context, name, pos, until_pos):
    pass


def _check_for_non_extractables(nodes):
    pass


def _is_name_input(module_context, names, first, last):
    pass


def _find_inputs_and_outputs(module_context, context, nodes):
    pass


def _find_non_global_names(nodes):
    pass


def _get_code_insertion_node(node, is_bound_method):
    pass


def _find_needed_output_variables(context, search_node, at_least_pos, return_variables):
    """
    Searches everything after at_least_pos in a node and checks if any of the
    return_variables are used in there and returns those.
    """
    pass


def _is_node_ending_return_stmt(node):
    pass
