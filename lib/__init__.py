from .decorators import proxy_test_decorator, Test, test
from .registration import discover_tests
from .formater import format_failed

try:
    from surimi._version import __version__
except ImportError:
    __version__ = "0.0.0"
