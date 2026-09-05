![Surimi](docs/surimi.svg)

# Installation

Surimi can be installed using `pip install surimi` or with uv using `uv add surimi`. When installed, one can verify that everything works by running `surimi --version` (or `uv run surimi --version` when using uv).

# Use

Surimi is designed to be simple. By default, surimi searches tests in two locations: a `tests` folder for integration tests and a `src` folder for unit tests.

## Custom tests folder

The folder in which tests are searched can be overridden by providing a path to the surimi CLI: `surimi $FOLDER`. Alternatively, the folders in which tests are located can be specified in a `.surimi` file at the root of the project.

Here is an example of a `.surimi` file:

```
tests
lib
bin
```

## Basic example

To flag a function as a test, simply add the `test` decorator to it. This decorator has no effect unless it is run using the `surimi` CLI, so executing it should have very limited impact on performance.

```python
@test
def foo():
  assert 2 == (1+1)
```

Test functions are run without parameters. If they require parameters, then these should be optional; otherwise a runtime error will occur.

## Fail with

When the test is expected to fail, a `fail_with` argument can be passed to the `test` decorator with the type of error that is expected. If the function fails with the provided error, the test is considered a success.

```python
@test(fail_with=AssertionError)
def foo():
  assert 2 == 3
```
