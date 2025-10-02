"""Update all references from framework/ to agentic-framework/."""

import os
from pathlib import Path

# Get the project root
project_root = Path(__file__).parent.parent

# Files to update with path replacements
files_to_update = [
    ".github/copilot-instructions.md",
    "README.md",
    "telco-domain/README.md",
    "docs/FRAMEWORK_REORGANIZATION.md",
]

# Patterns to replace
replacements = [
    ("framework/", "agentic-framework/"),
    ("framework\\", "agentic-framework\\"),
    ("`framework/", "`agentic-framework/"),
    ("**framework/**", "**agentic-framework/**"),
    ("in framework/", "in agentic-framework/"),
    ("the framework/", "the agentic-framework/"),
    ("from framework/", "from agentic-framework/"),
    ("See framework/", "See agentic-framework/"),
    ("Reference framework/", "Reference agentic-framework/"),
]

print("=" * 70)
print("RENAMING FRAMEWORK REFERENCES")
print("=" * 70)

for file_path in files_to_update:
    full_path = project_root / file_path
    
    if not full_path.exists():
        print(f"⚠️  {file_path} - NOT FOUND, skipping")
        continue
    
    print(f"\n📝 Processing: {file_path}")
    
    # Read the file
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    
    # Apply replacements
    for old_pattern, new_pattern in replacements:
        if old_pattern in content:
            count = content.count(old_pattern)
            content = content.replace(old_pattern, new_pattern)
            print(f"   ✓ Replaced '{old_pattern}' ({count} occurrences)")
    
    # Write back if changes were made
    if content != original_content:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   ✅ Updated {file_path}")
    else:
        print(f"   - No changes needed")

# Update agent files
print(f"\n📂 Processing agent files in agentic-framework/sub-agents/...")
agents_dir = project_root / "agentic-framework" / "sub-agents"

if agents_dir.exists():
    agent_files = list(agents_dir.glob("*.md"))
    print(f"   Found {len(agent_files)} agent files")
    
    for agent_file in agent_files:
        with open(agent_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # Update relative paths (already done, but check for any stragglers)
        content = content.replace("./development-standards/", "../standards/")
        content = content.replace("framework/standards/", "../standards/")
        
        if content != original_content:
            with open(agent_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"   ✓ Updated {agent_file.name}")

print("\n" + "=" * 70)
print("✅ ALL REFERENCES UPDATED!")
print("=" * 70)
