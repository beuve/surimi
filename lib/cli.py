import click
import os
import sys

@click.command()
@click.option('-v', '--verbose', default=0, nargs=1, type=int)
@click.option('-d', '--dir', default='.', nargs=1, type=str)
def test(verbose, dir):
  root = os.path.abspath(dir)
  sys.path.insert(0, root)
  import hermes
  test_runner = hermes.Test()
  hermes.test = test_runner
  hermes.register_tests(dir)
  test_runner.run_tests(verbose=verbose)

if __name__ == '__main__':
  test()
