import re

with open(r"C:\imperia_v4\docs\index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the async function loadPassports and add closing brace
# The function starts with "async function loadPassports()" and needs a closing "}"
# We'll look for the pattern and add the missing brace

# Strategy: find "async function loadPassports" and ensure there's a closing brace
# before the "window.addEventListener" line

# Add missing closing brace for the async function
# Look for: "                } catch (e) {\n" followed by lines, then we need to add "            }" 
# to close the function

# Insert the function closing brace after the try/catch block
pattern = r"(\}\s+catch\s+\(e\)\s*\{[\s\S]*?\+\+\s*\+\+?\s*\})(\s+window\.addEventListener"
replacement = r"\1            }\n\2"
new_content = re.sub(pattern, replacement, content)

if new_content != content:
    with open(r"C:\imperia_v4\docs\index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Fixed: added missing function close brace")
else:
    print("Pattern not matched, trying alternative")
    # Alternative: just insert } at the right position
    # Find line with "            window.addEventListener" and insert } before it
    idx = content.find("            window.addEventListener")
    if idx > 0:
        # Insert "            }" before window.addEventListener
        insert_pos = idx
        # But we need to find the right place - after the try-catch closing
        # Let's just add the closing brace at position idx
        new_content2 = content[:insert_pos] + "            }\n" + content[insert_pos:]
        with open(r"C:\imperia_v4\docs\index.html", "w", encoding="utf-8") as f:
            f.write(new_content2)
        print("Fixed: inserted brace before window.addEventListener")