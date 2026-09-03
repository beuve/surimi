import importlib
import sys
import os
from pathlib import Path 

def discover_tests(dir: str = '.'):
  test_locations = [
      dir,
      os.path.join(dir, 'src'),
      os.path.join(dir, 'tests'),
  ]
  
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
            print(f"[red]Error importing {module_name}: {e}[/red]")

