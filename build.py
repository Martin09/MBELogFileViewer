import sys

import matplotlib
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(includes=['matplotlibwidget'],
                    include_files=['MBELogFileViewer.ui', (matplotlib.get_data_path(), "mpl-data")], packages=[],
                    excludes=['collections.abc', 'wx', 'scipy', 'cvxopt'])

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('MBELogFileViewer.py', base=base, targetName='MBELogFileViewer.exe')
]

setup(name='MBELogFileViewer',
      version='1.1',
      description='Used to display log files in an intuitive and easy to use way. Written in Python.',
      options=dict(build_exe=buildOptions),
      executables=executables)
