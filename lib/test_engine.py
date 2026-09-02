from dataclasses import dataclass
from typing import Any, Callable
from .test_runner import run_test
from .test_result_formater import format_failed, format_module_result
from rich.console import Console

@dataclass
class TestInfos:
  function: Callable[[], None]
  name: str
  location: str
  fail_with: Any

  def __call__(self):
    self.function()

class Test:
  def __init__(self):
    self.registered_tests: list[TestInfos] = {}
  
  def add_function(self, fun, **kwargs):
      fail_with = kwargs.get('fail_with')
      test = TestInfos(fun, fun.__name__, fun.__globals__['__file__'], fail_with)
      module_name = fun.__globals__['__name__']
      if module_name not in self.registered_tests:
        self.registered_tests[module_name] = []
      self.registered_tests[module_name].append(test)
  
  def __call__(self, *args, **kwargs):
    #@test
    if args and callable(args[0]):
      self.add_function(args[0], **kwargs)
      return args[0]

    #@test(...)
    def register(function):
      self.add_function(function, **kwargs)
      return function

    return register

  def run_tests(self, verbose):
    console = Console()
    for num_module, module in enumerate(self.registered_tests):
      tests = self.registered_tests[module]
      results = []
      failed = False
      total_time = 0
      for test in tests:
        res = run_test(test)
        if not res.failed: failed = True
        total_time += res.execution_time
        results.append(res)

      format_module_result(console, num_module+1, len(self.registered_tests), module, not failed, total_time)

      first = True
      for res in results:
        if res.failed: format_failed(console, res, verbose)

def proxy_test_decorator(*args, **kwargs):
  if args and callable(args[0]):
    function = args[0]
    return function

  def register(function):
    return function
  return register
