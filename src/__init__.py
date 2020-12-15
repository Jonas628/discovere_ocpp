import pathlib
import sys
__version__ = '0.1'

sys.path.append('../..\\')
LOGDIR = \
    pathlib.Path(__file__).parent.resolve() / pathlib.Path('data')
