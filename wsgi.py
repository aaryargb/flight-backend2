import sys
import os

# add project root to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == "__main__":
    app.run()
