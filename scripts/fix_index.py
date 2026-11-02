import re

with open(r"C:\imperia_v4\docs\index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Remove orphaned code between loadPassports() and the end of the init block
# The orphaned code is between line 245 and line 284
# We need to remove: }[\s\S]{0,5000}? until the final closing

# Find the pattern: after loadPassports() async function, remove until the final }
# Strategy: find "async function loadPassports" and then find the next "}" that closes the outer block

# Actually, let's just remove the specific orphaned block by targeting the exact text
orphaned_start = "            }\n                const lat = passport.center_lat;"
orphaned_end = "            window.addEventListener('resize', () => map.invalidateSize());\n        }"

# Check if the orphaned text is present
if orphaned_start in content:
    # Find the end marker
    idx = content.index(orphaned_start)
    # Find the orphaned end
    idx_end = content.index(orphaned_end)
    # Replace the entire block
    new_content = content[:idx] + content[idx_end:]
    with open(r"C:\imperia_v4\docs\index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Fixed! Removed orphaned block")
else:
    print("Pattern not found, trying alternative...")
    # Try removing lines 245-284 by splitting
    lines = content.split("\n")
    # Keep lines 1-244 and 285+
    new_lines = lines[:245] + lines[285:]
    new_content = "\n".join(new_lines)
    with open(r"C:\imperia_v4\docs\index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Fixed! Removed lines 245-285")