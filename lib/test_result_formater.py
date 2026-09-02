import traceback
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

def format_module_result(console: Console, num_module: int, total_modules: int, module: str, failed: bool, execution_time: float):
  if not failed : status = Text("[bold][green]PASSED[/green][/bold]")
  else: status = Text("[bold][red]FAILED[/red][/bold]")
  time_str = f"{execution_time:.2f}s"
  module = module.replace('.', '/')
  console.print(f"{num_module}/{total_modules}  {module:<35}  {status}  {time_str:>8}")

def format_failed(console: Console, test_result: TestResult, verbose: int):
  error_name = type(test_result.exception).__name__
  error = f'[red]{error_name}[/red]' if test_result.exception else "[green]No error[/green]"
  expected = f', expected [red]{test_result.fail_with.__name__}[/red]' if test_result.fail_with else ''
  
  console.print(f"  -> [red]Test [bold]{test_result.name}[/bold] failed[/red]: got {error}{expected}")
  
  if verbose >= 1:
    if test_result.stdout:
      console.print(f"     [yellow]stdout:[/yellow]")
      for line in test_result.stdout.strip().split('\n'):
        console.print(f"       {line}")
    
    if test_result.stderr:
      console.print(f"     [yellow]stderr:[/yellow]")
      for line in test_result.stderr.strip().split('\n'):
        console.print(f"       {line}")
  
  if verbose >= 2:
    if test_result.exception and test_result.exception.__traceback__:
      console.print(f"     [yellow]traceback:[/yellow]")
      tb_lines = traceback.format_tb(test_result.exception.__traceback__)
      for line in tb_lines:
        for tb_line in line.strip().split('\n'):
          console.print(f"       {tb_line}")
