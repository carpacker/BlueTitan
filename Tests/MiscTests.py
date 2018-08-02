# Real path/relative path test
import os, sys
sys.path.append(os.path.realpath('../Components/Database-Manager'))
sys.path.append(os.path.realpath('../Components/Libraries/'))
import GeneralizedDatabase
from GeneralizedDatabase import GenDatabaseLibrary
