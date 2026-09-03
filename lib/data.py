from dataclasses import dataclass
from typing import Any

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
