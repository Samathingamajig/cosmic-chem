import os
try:
  import main
  import interactive
except ModuleNotFoundError:
  os.system("pip3 install -r requirements.txt")
