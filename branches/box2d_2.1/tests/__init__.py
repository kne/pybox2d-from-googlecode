import os, sys
from glob import glob

tests = [os.path.filename(test) for test in 
                glob(os.path.join(sys.argv[0], "*.py"))]

for test in tests:
    __import__(test[:-3], globals(), locals(), [], -1)
