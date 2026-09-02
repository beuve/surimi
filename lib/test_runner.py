from dataclasses import dataclass
import sys
from io import StringIO
import time

@dataclass
class TestResult:
  name: str
  fail_with: Any
  location: str
  failed: bool
  stdout: str
  stderr: str
  execution_time: float = 0.0
  exception: Exception = None

  def __str__(self) -> str:
    if self.failed: return self._format_failed()
    else: return ''

def run_test(test_info: TestInfos) -> TestResult:
  
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
