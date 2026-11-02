import shutil, os

src = r"c:\imperia_v4\src\swarm_inference_new.py"
dst = r"c:\imperia_v4\src\swarm_inference.py"

if os.path.exists(src):
    shutil.copy(src, dst)
    print(f"Copied {src} to {dst}")
else:
    print(f"Source not found: {src}")