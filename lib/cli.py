import click
import os
import sys
from .registration import discover_tests
from .runner import run_tests
from rich.console import Console

@click.command()
@click.option('-v', '--verbose', default=0, nargs=1, type=int)
@click.argument('directory', default=None, nargs=1, type=str)
def test(verbose, directory):
  console = Console()
  root = os.path.abspath(directory if directory != None else '.')
  sys.path.insert(0, root)
  import surimi
  tests = surimi.Test()
  surimi.test = tests
  discover_tests(directory)
  run_tests(tests, verbose=verbose, console=console)

if __name__ == '__main__':
  test()
