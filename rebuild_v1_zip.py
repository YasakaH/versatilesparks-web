import subprocess
import sys

# Simply delegate to the main rebuild_zips script to maintain single source of truth
print("Delegating to rebuild_zips.py...")
res = subprocess.run([sys.executable, "rebuild_zips.py"])
sys.exit(res.returncode)
