# 🎯 Quick Reference: Root Cleanup

## One-Command Cleanup

```bash
# Execute the cleanup (conservative, 89% of files)
python scripts\cleanup_root_directory.py --execute
```

## What Happens

✅ **33 files organized automatically**  
⚠️ **4 files require manual review**

## Files Moved

- 6 demo files → `scripts/demos/`
- 8 test data → `data/test/`
- 4 docs → `docs/guides/`
- 4 utils → `scripts/utils/`
- 6 tests → `tests/integration/`
- 2 setup → `scripts/setup/`
- 1 migration → `scripts/migrations/`
- 2 artifacts deleted

## Manual Tasks (5 minutes)

### 1. Fix Test File
Edit `tests\test_enhanced_classifier.py` line 91:
```python
# Change this:
launcher_file = Path(__file__).parent / "launch_enhanced_demo.py"
# To this:
launcher_file = Path(__file__).parent.parent / "launch_enhanced_demo.py"
```

### 2. Check packages.txt
```bash
fc packages.txt requirements.txt
# If same/outdated: del packages.txt
```

### 3. Archive Old Launchers (Optional)
```bash
mkdir legacy\launchers
move launch_demo_intelligent.py legacy\launchers\
move launch_enhanced_demo.py legacy\launchers\
move launch_safe_demo.bat legacy\launchers\
```

## Verify

```bash
pytest tests\ -v
python launch_demo.py
```

## Commit

```bash
git add -A
git commit -m "refactor: reorganize root directory - moved 33 files into organized subdirectories"
```

## Rollback (if needed)

```bash
git reset --hard HEAD~1
```

---

**Ready?** Execute cleanup now! 🚀

```bash
python scripts\cleanup_root_directory.py --execute
```
