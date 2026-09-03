from rich.console import Console
from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class TestInfos:
  function: Callable[[], None]
  name: str
  location: str
  fail_with: Exception

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

def proxy_test_decorator(*args, **kwargs):
  if args and callable(args[0]):
    function = args[0]
    return function

  def register(function):
    return function
  return register
