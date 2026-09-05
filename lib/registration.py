import importlib
import sys
import os
from pathlib import Path 
from rich.console import Console

def discover_tests(console: Console, dir: str = None):
  test_locations = [
      './src',
      './tests',
  ]
  if dir != None : test_locations = [dir]
  for test_location in test_locations:
    if not os.path.isdir(test_location):
      continue
    
    for root, dirs, files in os.walk(test_location):
      dirs[:] = [
          d for d in dirs 
          if os.path.exists(os.path.join(root, d, "__init__.py"))
      ]
      
      for file in files:
        if file.endswith(".py"):
          rel_path = os.path.relpath(os.path.join(root, file), dir)
          module_name = rel_path.replace(os.sep, ".").replace(".py", "")
          
          try:
            importlib.import_module(module_name)
          except ImportError as e:
            console.print(f'[red]Error importing {module_name}: {e}[/red]')

