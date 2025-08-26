import os
import re

# Read the models file
with open('sda_models/models.py', 'r') as f:
    content = f.read()

# Remove all ImageField imports and usage
content = re.sub(r'from django\.core\.files\.storage import.*\n', '', content)
content = re.sub(r'from django\.conf import settings\n', '', content)

# Remove all upload function definitions
content = re.sub(r'def upload_to_[^:]+:\n    """[^"]*"""\n    ext = filename\.split\(\'\.\'\)\[-1\]\n    filename = f"{uuid\.uuid4\(\)\.{ext}}"\n    return f"[^"]+"\n\n', '', content, flags=re.MULTILINE)

# Replace ImageField patterns with URLField
patterns = [
    # Remove image/photo/icon/cover_photo ImageField lines
    (r'    # File field for .*\n    \w+ = models\.ImageField\([^)]+\)\n', ''),
    (r'    \w+ = models\.ImageField\([^)]+\)\n', ''),
    
    # Remove save methods with image URL generation
    (r'    def save\(self, \*args, \*\*kwargs\):\n        # Generate URL from file if file exists\n        if self\.\w+:\n            # Use relative URL that matches backend structure\n            self\.\w+_url = f"/uploads/{\w+\.\w+\.name}"\n        super\(\)\.save\(\*args, \*\*kwargs\)\n\n', ''),
    (r'    def save\(self, \*args, \*\*kwargs\):\n        if self\.\w+:\n            self\.\w+_url = f"/uploads/{\w+\.\w+\.name}"\n        super\(\)\.save\(\*args, \*\*kwargs\)\n\n', ''),
]

for pattern, replacement in patterns:
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

# Write the cleaned content back
with open('sda_models/models.py', 'w') as f:
    f.write(content)

print("Models file cleaned successfully!")
