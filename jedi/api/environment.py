"""
Environments are a way to activate different Python versions or Virtualenvs for
static analysis. The Python binary in that environment is going to be executed.
"""
import os
import sys
import hashlib
import filecmp
from collections import namedtuple
from shutil import which
from typing import TYPE_CHECKING

from jedi.cache import memoize_method, time_cache
from jedi.inference.compiled.subprocess import CompiledSubprocess, \
    InferenceStateSameProcess, InferenceStateSubprocess

import parso

if TYPE_CHECKING:
    from jedi.inference import InferenceState


_VersionInfo = namedtuple('VersionInfo', 'major minor micro')  # type: ignore[name-match]

_SUPPORTED_PYTHONS = ['3.13', '3.12', '3.11', '3.10', '3.9', '3.8']
_SAFE_PATHS = ['/usr/bin', '/usr/local/bin']
_CONDA_VAR = 'CONDA_PREFIX'
_CURRENT_VERSION = '%s.%s' % (sys.version_info.major, sys.version_info.minor)


class InvalidPythonEnvironment(Exception):
    """
    If you see this exception, the Python executable or Virtualenv you have
    been trying to use is probably not a correct Python version.
    """


class _BaseEnvironment:
    @memoize_method
    def get_grammar(self):
        pass

    @property
    def _sha256(self):
        pass


def _get_info():
    pass


class Environment(_BaseEnvironment):
    """
    This class is supposed to be created by internal Jedi architecture. You
    should not create it directly. Please use create_environment or the other
    functions instead. It is then returned by that function.
    """
    _subprocess = None

    def __init__(self, executable, env_vars=None):
        self._start_executable = executable
        self._env_vars = env_vars
        # Initialize the environment
        self._get_subprocess()

    def _get_subprocess(self):
        if self._subprocess is not None and not self._subprocess.is_crashed:
            return self._subprocess

        try:
            self._subprocess = CompiledSubprocess(self._start_executable,
                                                  env_vars=self._env_vars)
            info = self._subprocess._send(None, _get_info)
        except Exception as exc:
            raise InvalidPythonEnvironment(
                "Could not get version information for %r: %r" % (
                    self._start_executable,
                    exc))

        # Since it could change and might not be the same(?) as the one given,
        # set it here.
        self.executable = info[0]
        """
        The Python executable, matches ``sys.executable``.
        """
        self.path = info[1]
        """
        The path to an environment, matches ``sys.prefix``.
        """
        self.version_info = _VersionInfo(*info[2])
        """
        Like :data:`sys.version_info`: a tuple to show the current
        Environment's Python version.
        """
        return self._subprocess

    def __repr__(self):
        version = '.'.join(str(i) for i in self.version_info)
        return '<%s: %s in %s>' % (self.__class__.__name__, version, self.path)

    def get_inference_state_subprocess(
        self,
        inference_state: 'InferenceState',
    ) -> InferenceStateSubprocess:
        pass

    @memoize_method
    def get_sys_path(self):
        """
        The sys path for this environment. Does not include potential
        modifications from e.g. appending to :data:`sys.path`.

        :returns: list of str
        """
        # It's pretty much impossible to generate the sys path without actually
        # executing Python. The sys path (when starting with -S) itself depends
        # on how the Python version was compiled (ENV variables).
        # If you omit -S when starting Python (normal case), additionally
        # site.py gets executed.
        return self._get_subprocess().get_sys_path()


class _SameEnvironmentMixin:
    def __init__(self):
        self._start_executable = self.executable = sys.executable
        self.path = sys.prefix
        self.version_info = _VersionInfo(*sys.version_info[:3])
        self._env_vars = None


class SameEnvironment(_SameEnvironmentMixin, Environment):
    pass


class InterpreterEnvironment(_SameEnvironmentMixin, _BaseEnvironment):
    def get_inference_state_subprocess(
        self,
        inference_state: 'InferenceState',
    ) -> InferenceStateSameProcess:
        pass

    def get_sys_path(self):
        return sys.path


def _get_virtual_env_from_var(env_var='VIRTUAL_ENV'):
    """Get virtualenv environment from VIRTUAL_ENV environment variable.

    It uses `safe=False` with ``create_environment``, because the environment
    variable is considered to be safe / controlled by the user solely.
    """
    pass


def _calculate_sha256_for_file(path):
    pass


def get_default_environment():
    """
    Tries to return an active Virtualenv or conda environment.
    If there is no VIRTUAL_ENV variable or no CONDA_PREFIX variable set
    set it will return the latest Python version installed on the system. This
    makes it possible to use as many new Python features as possible when using
    autocompletion and other functionality.

    :returns: :class:`.Environment`
    """
    pass


def _try_get_same_env():
    pass


def get_cached_default_environment():
    pass


@time_cache(seconds=10 * 60)  # 10 Minutes
def _get_cached_default_environment():
    pass


def find_virtualenvs(paths=None, *, safe=True, use_environment_vars=True):
    """
    :param paths: A list of paths in your file system to be scanned for
        Virtualenvs. It will search in these paths and potentially execute the
        Python binaries.
    :param safe: Default True. In case this is False, it will allow this
        function to execute potential `python` environments. An attacker might
        be able to drop an executable in a path this function is searching by
        default. If the executable has not been installed by root, it will not
        be executed.
    :param use_environment_vars: Default True. If True, the VIRTUAL_ENV
        variable will be checked if it contains a valid VirtualEnv.
        CONDA_PREFIX will be checked to see if it contains a valid conda
        environment.

    :yields: :class:`.Environment`
    """
    pass


def find_system_environments(*, env_vars=None):
    """
    Ignores virtualenvs and returns the Python versions that were installed on
    your system. This might return nothing, if you're running Python e.g. from
    a portable version.

    The environments are sorted from latest to oldest Python version.

    :yields: :class:`.Environment`
    """
    pass


# TODO: this function should probably return a list of environments since
# multiple Python installations can be found on a system for the same version.
def get_system_environment(version, *, env_vars=None):
    """
    Return the first Python environment found for a string of the form 'X.Y'
    where X and Y are the major and minor versions of Python.

    :raises: :exc:`.InvalidPythonEnvironment`
    :returns: :class:`.Environment`
    """
    pass


def create_environment(path, *, safe=True, env_vars=None):
    """
    Make it possible to manually create an Environment object by specifying a
    Virtualenv path or an executable path and optional environment variables.

    :raises: :exc:`.InvalidPythonEnvironment`
    :returns: :class:`.Environment`
    """
    pass


def _get_executable_path(path, safe=True):
    """
    Returns None if it's not actually a virtual env.
    """
    pass


def _get_executables_from_windows_registry(version):
    pass


def _assert_safe(executable_path, safe):
    pass


def _is_safe(executable_path):
    # Resolve sym links. A venv typically is a symlink to a known Python
    # binary. Only virtualenvs copy symlinks around.
    pass


def _is_unix_safe_simple(real_path):
    pass


def _is_unix_admin():
    pass
