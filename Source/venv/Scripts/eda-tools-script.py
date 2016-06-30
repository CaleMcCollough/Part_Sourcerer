#!D:\Workspace\eda-tools\source\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'EDA-Tools==0.1','console_scripts','eda-tools'
__requires__ = 'EDA-Tools==0.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('EDA-Tools==0.1', 'console_scripts', 'eda-tools')()
    )
