# Root Directory Cleanup Guide

## 🎯 Overview

This guide explains how to safely reorganize the root directory by moving files into appropriate subdirectories. The cleanup script provides:

- ✅ **Dry-run mode** for safe preview
- ✅ **Validation checks** before moving files
- ✅ **Reference detection** to prevent breaking imports
- ✅ **Backup manifest** for potential rollback
- ✅ **Comprehensive logging** of all operations

## 📋 What Gets Moved

### Phase 1: Demo Files → `scripts/demos/`
```
demo_epic_1_6_complete.py
demo_epic_1_11_rag_complete.py
demo_epic_1_16_1_20_complete.py
enhanced_demo_complete.py
enhanced_vector_schema_demo.py
stepwise_demo.py
```

### Phase 2: Test Data → `data/test/`
```
comprehensive_test_data.json
domains.txt
rag_system_test_cases.csv
rag_system_test_data.json
rules_engine_test_cases.csv
rules_engine_test_data.json
routing_decisions.jsonl
validation_results.json
```

### Phase 3: Documentation → `docs/guides/`
```
CLIENT_SETUP_GUIDE.md
IMPLEMENTATION_PACKAGE.md
NETWORK_WHITELIST.md
SETUP_GUIDE.md
```

### Phase 4: Unused Launchers → `legacy/launchers/`
```
launch_demo_intelligent.py
launch_enhanced_demo.py
launch_safe_demo.bat
```
⚠️ **Note**: Only moved if not referenced in other files

### Phase 5: Utility Scripts → `scripts/utils/`
```
test_data_generator.py
validate_setup.py
validation_summary.py
validate_test_data.py
```
⚠️ **Note**: Skipped if duplicate exists in `scripts/`

### Phase 6: Test Scripts → `tests/integration/`
```
test_enhanced_routing_intelligence.py
test_full_pinecone.py
test_pinecone_connection.py
test_regions.py
test_vector_operations.py
quick_pinecone_test.py
```

### Phase 7: Setup Scripts → `scripts/setup/`
```
setup_env.py
quick_setup.py
```

### Phase 8: Migration Scripts → `scripts/migrations/`
```
vector_routing_intelligence_migration.py
```

### Phase 9: Build Artifacts (Deleted)
```
.coverage
coverage.xml
```
Also updates `.gitignore` to exclude these files

### Phase 10: Package Files (Evaluated)
```
packages.txt
```
Evaluates if identical to `requirements.txt` before deletion

## 🚀 Usage

### Step 1: Preview Changes (Dry Run)

First, run in dry-run mode to see what would happen:

```bash
python scripts/cleanup_root_directory.py
```

This will:
- ✅ Show all operations that would be performed
- ✅ Check for file references
- ✅ Detect potential duplicates
- ✅ Create a backup manifest preview
- ❌ **NOT** move any actual files

### Step 2: Review the Output

The script will display detailed information about:
- Which files will be moved
- Any files that are referenced in other code
- Potential duplicates that need review
- Summary of all operations

Example output:
```
============================================================
PHASE 1: Moving Demo Files
============================================================
✓ Created directory: scripts/demos
✓ Moved: demo_epic_1_6_complete.py → scripts/demos/demo_epic_1_6_complete.py
✓ Moved: demo_epic_1_11_rag_complete.py → scripts/demos/demo_epic_1_11_rag_complete.py
...

============================================================
PHASE 4: Archiving Unused Launchers
============================================================
⚠️  launch_demo_intelligent.py is referenced in: docs/README.md
   Skipping move. Review references first.
...

============================================================
CLEANUP SUMMARY
============================================================
✓ Phase 1: Demo Files: 6/6 operations successful
✓ Phase 2: Test Data: 8/8 operations successful
...
TOTAL: 45/48 operations successful

🔍 DRY RUN MODE - No files were actually moved
   Run with --execute flag to perform actual operations
```

### Step 3: Review Warnings

Pay special attention to:
- **Referenced files**: Files mentioned in other code
- **Duplicate files**: Files that exist in both locations
- **Failed operations**: Files that couldn't be moved

### Step 4: Execute Cleanup

Once you're satisfied with the dry-run results:

```bash
python scripts/cleanup_root_directory.py --execute
```

This will:
- ✅ Create all necessary directories
- ✅ Move files to new locations
- ✅ Delete build artifacts
- ✅ Update `.gitignore`
- ✅ Create backup manifest (`cleanup_backup_manifest.json`)

### Step 5: Verify Changes

After execution:

1. **Check that demos still work:**
   ```bash
   python scripts/demos/demo_epic_1_6_complete.py
   ```

2. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

3. **Verify main launcher:**
   ```bash
   python launch_demo.py
   ```

4. **Check documentation links:**
   - Review `README.md` for broken links
   - Update any references to moved files

## 🔄 Rollback Instructions

If something goes wrong, you can manually rollback using the backup manifest:

1. **Open the backup manifest:**
   ```bash
   type cleanup_backup_manifest.json
   ```

2. **The manifest contains:**
   ```json
   {
     "timestamp": "2025-10-17T10:30:00",
     "operations": [
       {
         "source": "c:\\DEV\\call-centre-agent\\demo_epic_1_6_complete.py",
         "destination": "c:\\DEV\\call-centre-agent\\scripts\\demos\\demo_epic_1_6_complete.py",
         "operation": "move"
       }
     ]
   }
   ```

3. **Manually reverse operations:**
   ```bash
   move scripts\demos\demo_epic_1_6_complete.py .
   ```

## 📝 Post-Cleanup Tasks

After running the cleanup successfully:

### 1. Update Import Statements

If any files reference moved files, update their imports:

**Before:**
```python
from demo_epic_1_6_complete import SomeFunction
```

**After:**
```python
from scripts.demos.demo_epic_1_6_complete import SomeFunction
```

### 2. Update Documentation

Update references in documentation files:
- `README.md`
- `docs/*.md`
- Any tutorial files

**Search for references:**
```bash
findstr /S /I "demo_epic" *.md docs\*.md
findstr /S /I "CLIENT_SETUP_GUIDE" *.md docs\*.md
```

### 3. Update CI/CD Configuration

If you have CI/CD pipelines, update paths in:
- `.github/workflows/*.yml`
- `azure-pipelines.yml`
- Any deployment scripts

### 4. Commit Changes

```bash
git add -A
git status
git commit -m "refactor: reorganize root directory structure

- Move demo files to scripts/demos/
- Move test data to data/test/
- Move documentation to docs/guides/
- Archive unused launchers to legacy/launchers/
- Move utility scripts to scripts/utils/
- Move test scripts to tests/integration/
- Move setup scripts to scripts/setup/
- Move migration scripts to scripts/migrations/
- Clean up build artifacts and update .gitignore"
```

## ⚠️ Troubleshooting

### Issue: "File not found"
**Solution**: File may have already been moved or deleted. Check git status.

### Issue: "File is referenced in other code"
**Solution**: Update the references first, then re-run the cleanup.

### Issue: "Duplicate found"
**Solution**: Compare the files and keep the most recent version:
```bash
fc file1.py file2.py
```

### Issue: Tests fail after cleanup
**Solution**: 
1. Check for broken imports
2. Update test data paths
3. Review the backup manifest to identify what changed

## 🎯 Expected Final Structure

```
call-centre-agent/
├── .env
├── .gitignore
├── main.py
├── launch_demo.py
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── ROADMAP.md
├── BACKLOG.md
│
├── scripts/
│   ├── cleanup_root_directory.py  ← The cleanup script
│   ├── CLEANUP_README.md          ← This guide
│   ├── demos/                     ← Moved demo files
│   ├── utils/                     ← Moved utility scripts
│   ├── setup/                     ← Moved setup scripts
│   └── migrations/                ← Moved migration scripts
│
├── data/
│   └── test/                      ← Moved test data
│
├── docs/
│   └── guides/                    ← Moved documentation
│
├── tests/
│   └── integration/               ← Moved test scripts
│
└── legacy/
    └── launchers/                 ← Archived launchers
```

## 🔒 Safety Features

1. **Dry-run by default**: Won't move files unless you use `--execute`
2. **Reference checking**: Detects if files are used elsewhere
3. **Duplicate detection**: Warns about existing files
4. **Backup manifest**: Records all operations for rollback
5. **Comprehensive logging**: Detailed output of every operation
6. **Validation**: Checks file existence before moving

## 📞 Support

If you encounter issues:

1. Check the `cleanup_backup_manifest.json` for operation details
2. Review the script output for warnings
3. Manually verify file locations
4. Use git to track what changed: `git status`

## 🎉 Benefits

After cleanup, you'll have:
- ✅ Clean root directory
- ✅ Organized file structure
- ✅ Easier navigation
- ✅ Better maintainability
- ✅ Clearer project organization
- ✅ Professional appearance

---

**Last Updated**: October 17, 2025  
**Script Version**: 1.0  
**Tested on**: Windows 11, Python 3.11+
