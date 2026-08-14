import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import full_compile


full_compile("Test/Basic_var.txt")
full_compile("Test/math.txt")
full_compile("Test/boolean.txt")
full_compile("Test/const.txt")
full_compile("Test/arr.txt")
full_compile("Test/loop.txt")
full_compile("Test/functions.txt")
full_compile("Test/struct.txt")
full_compile("Test/asm.txt")
full_compile("Test/pointer.txt")