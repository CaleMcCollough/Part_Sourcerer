#!D:\Workspace\eda-tools\source\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Part-Sourcerer==0.1','console_scripts','sourcerer'
__requires__ = 'Part-Sourcerer==0.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('Part-Sourcerer==0.1', 'console_scripts', 'sourcerer')()
    )
