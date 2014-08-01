# mysetup.py
from distutils.core import setup
import py2exe, sys 


includes = ["encodings", "encodings.*"]    
sys.argv.append("py2exe")  

options = {"py2exe":
            {   "compressed": 1,
                "optimize": 2,
                "includes": includes,
                "bundle_files": 1,
                 "dll_excludes": ["MSVCP90.dll"] 
            }
          }

setup(options = options,  
      zipfile=None,   
      console = [{"script":"login_score.py", 'icon_resources':[(1, 'favicon.ico')]}]) 