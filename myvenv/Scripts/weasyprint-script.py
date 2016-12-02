#!c:\users\andrew\documents\github\docmerge\myvenv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'WeasyPrint==0.29','console_scripts','weasyprint'
__requires__ = 'WeasyPrint==0.29'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('WeasyPrint==0.29', 'console_scripts', 'weasyprint')()
    )
