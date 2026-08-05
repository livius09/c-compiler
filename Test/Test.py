import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import full_compile


full_compile("Test/Basic_var.txt")
full_compile("Test/math.txt")
full_compile("Test/.txt")
full_compile("Test/.txt")
full_compile("Test/.txt")
full_compile("Test/.txt")
full_compile("Test/.txt")
full_compile("Test/.txt")
full_compile("Test/.txt")
full_compile("Test/.txt")