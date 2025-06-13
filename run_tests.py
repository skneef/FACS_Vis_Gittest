import pytest
import sys

"""
RuntimeWarning is given in LogicleTransform when running tests, if you want to ignore these, you can use the following code:
#import warnings

#warnings.simplefilter('ignore', category=RuntimeWarning)
#warnings.filterwarnings("ignore", category=RuntimeWarning)
"""

if __name__ == '__main__':
    sys.exit(pytest.main())