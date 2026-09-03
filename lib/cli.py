import click
import os
import sys
from .registration import discover_tests
from .runner import run_tests

@click.command()
@click.option('-v', '--verbose', default=0, nargs=1, type=int)
@click.argument('directory', default='.', nargs=1, type=str)
def test(verbose, directory):
  root = os.path.abspath(directory)
  sys.path.insert(0, root)
  import surimi
  tests = surimi.Test()
  surimi.test = tests
  discover_tests(directory)
  run_tests(tests, verbose=verbose)

if __name__ == '__main__':
  test()
