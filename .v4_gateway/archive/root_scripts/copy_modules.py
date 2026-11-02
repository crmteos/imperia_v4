import shutil
import os

# Copy fresh module files to original paths
src_dir = r"c:\imperia_v4"
files_to_copy = [
    (os.path.join(src_dir, "src", "geo", "h3_vector_fresh.py"),
     os.path.join(src_dir, "src", "geo", "h3_vector.py")),
    (os.path.join(src_dir, "src", "p2p", "transport_adapter_fresh.py"),
     os.path.join(src_dir, "src", "p2p", "transport_adapter.py")),
]

for src, dst in files_to_copy:
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"Copied {src} to {dst}")
    else:
        print(f"Source not found: {src}")

# Also create test_modules.py
test_src = os.path.join(src_dir, "test_modules_fresh.py")
test_dst = os.path.join(src_dir, "test_modules.py")
if os.path.exists(test_src):
    shutil.copy(test_src, test_dst)
    print(f"Copied {test_src} to {test_dst}")

print("Done")