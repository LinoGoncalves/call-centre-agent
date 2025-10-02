"""Update agent file paths to use new framework structure."""

import os
from pathlib import Path

# Get the project root
project_root = Path(__file__).parent.parent

# Directory containing agent files
agents_dir = project_root / "framework" / "sub-agents"

# Patterns to replace
replacements = [
    ("./development-standards/", "../standards/"),
    ("telco-call-centre/development-standards/", "../standards/"),
]

# Process all markdown files in sub-agents directory
for md_file in agents_dir.glob("*.md"):
    print(f"Processing {md_file.name}...")
    
    # Read the file
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Apply replacements
    original_content = content
    for old_pattern, new_pattern in replacements:
        content = content.replace(old_pattern, new_pattern)
    
    # Write back if changes were made
    if content != original_content:
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ Updated {md_file.name}")
    else:
        print(f"  - No changes needed for {md_file.name}")

print("\n✅ All agent files processed!")
