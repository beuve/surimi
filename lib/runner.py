from dataclasses import dataclass
import sys
from io import StringIO
import time
from .data import TestResult
from .decorators import TestInfos, Test
from rich.console import Console
from .formater import format_module_result, format_failed

def run_single_test(test_info: TestInfos) -> TestResult:
  old_stdout = sys.stdout
  old_stderr = sys.stderr
  captured_stdout = StringIO()
  captured_stderr = StringIO()
  
  try:
    sys.stdout = captured_stdout
    sys.stderr = captured_stderr
    
    start_time = time.time()
    test_info()
    execution_time = time.time() - start_time
    
    return TestResult(
      name=test_info.name,
      fail_with=test_info.fail_with,
      location=test_info.location,
      failed=test_info.fail_with != None,
      stdout=captured_stdout.getvalue(),
      stderr=captured_stderr.getvalue(),
      execution_time=execution_time,
      exception=None
    )

  except Exception as e:
    execution_time = time.time() - start_time
    return TestResult(
      name=test_info.name,
      fail_with=test_info.fail_with,
      location=test_info.location,
      failed=type(e) != test_info.fail_with,
      stdout=captured_stdout.getvalue(),
      stderr=captured_stderr.getvalue(),
      execution_time=execution_time,
      exception=e
    )
  
  finally:
    sys.stdout = old_stdout
    sys.stderr = old_stderr


def run_tests(test: Test, verbose):
  console = Console()
  for num_module, module in enumerate(test.registered_tests):
    tests = test.registered_tests[module]
    results = []
    failed = False
    total_time = 0
    for t in tests:
      res = run_single_test(t)
      if not res.failed: failed = True
      total_time += res.execution_time
      results.append(res)

    format_module_result(console, num_module+1, len(test.registered_tests), module, not failed, total_time)

    first = True
    for res in results:
      if res.failed: format_failed(console, res, verbose)
