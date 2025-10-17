#!/usr/bin/env python3
"""
Root Directory Cleanup Script
=============================

This script safely reorganizes the root directory by:
1. Moving demo files to scripts/demos/
2. Moving test data to data/test/
3. Moving documentation to docs/guides/
4. Archiving unused launchers to legacy/launchers/
5. Moving utility scripts to scripts/utils/
6. Cleaning up build artifacts

All operations include validation and rollback capabilities.
"""

import shutil
import sys
from pathlib import Path
from typing import List, Dict
import json
from datetime import datetime

class RootCleanupManager:
    """Manages safe cleanup of root directory files."""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.backup_manifest = []
        self.operations_log = []
        self.dry_run = True
        
    def log(self, message: str, level: str = "INFO"):
        """Log operation with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        self.operations_log.append(log_entry)
        
    def validate_file_exists(self, file_path: Path) -> bool:
        """Validate that a file exists before moving."""
        exists = file_path.exists()
        if not exists:
            self.log(f"⚠️  File not found: {file_path}", "WARNING")
        return exists
        
    def create_directory(self, dir_path: Path) -> bool:
        """Create directory if it doesn't exist."""
        try:
            if not self.dry_run:
                dir_path.mkdir(parents=True, exist_ok=True)
            self.log(f"✓ Created directory: {dir_path.relative_to(self.root_dir)}")
            return True
        except Exception as e:
            self.log(f"✗ Failed to create directory {dir_path}: {e}", "ERROR")
            return False
            
    def move_file(self, source: Path, destination: Path) -> bool:
        """Move file with validation and logging."""
        try:
            if not self.validate_file_exists(source):
                return False
                
            # Create destination directory
            dest_dir = destination.parent
            if not dest_dir.exists() and not self.dry_run:
                dest_dir.mkdir(parents=True, exist_ok=True)
                
            # Record for potential rollback
            self.backup_manifest.append({
                "source": str(source),
                "destination": str(destination),
                "operation": "move"
            })
            
            if not self.dry_run:
                shutil.move(str(source), str(destination))
                
            rel_source = source.relative_to(self.root_dir)
            rel_dest = destination.relative_to(self.root_dir)
            self.log(f"✓ Moved: {rel_source} → {rel_dest}")
            return True
            
        except Exception as e:
            self.log(f"✗ Failed to move {source}: {e}", "ERROR")
            return False
            
    def delete_file(self, file_path: Path) -> bool:
        """Delete file with validation and logging."""
        try:
            if not self.validate_file_exists(file_path):
                return False
                
            self.backup_manifest.append({
                "source": str(file_path),
                "operation": "delete"
            })
            
            if not self.dry_run:
                file_path.unlink()
                
            rel_path = file_path.relative_to(self.root_dir)
            self.log(f"✓ Deleted: {rel_path}")
            return True
            
        except Exception as e:
            self.log(f"✗ Failed to delete {file_path}: {e}", "ERROR")
            return False
            
    def check_file_references(self, filename: str) -> List[str]:
        """Check if file is referenced in other files."""
        references = []
        search_dirs = [
            self.root_dir / "src",
            self.root_dir / "tests",
            self.root_dir / "scripts",
            self.root_dir / "docs"
        ]
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
                
            for file in search_dir.rglob("*.py"):
                try:
                    content = file.read_text(encoding='utf-8')
                    if filename in content:
                        references.append(str(file.relative_to(self.root_dir)))
                except Exception:
                    continue
                    
        return references
        
    def phase1_move_demos(self) -> Dict[str, bool]:
        """Phase 1: Move demo files to scripts/demos/"""
        self.log("\n" + "="*60)
        self.log("PHASE 1: Moving Demo Files")
        self.log("="*60)
        
        demos_dir = self.root_dir / "scripts" / "demos"
        self.create_directory(demos_dir)
        
        demo_files = [
            "demo_epic_1_6_complete.py",
            "demo_epic_1_11_rag_complete.py",
            "demo_epic_1_16_1_20_complete.py",
            "enhanced_demo_complete.py",
            "enhanced_vector_schema_demo.py",
            "stepwise_demo.py"
        ]
        
        results = {}
        for demo_file in demo_files:
            source = self.root_dir / demo_file
            destination = demos_dir / demo_file
            results[demo_file] = self.move_file(source, destination)
            
        return results
        
    def phase2_move_test_data(self) -> Dict[str, bool]:
        """Phase 2: Move test data to data/test/"""
        self.log("\n" + "="*60)
        self.log("PHASE 2: Moving Test Data")
        self.log("="*60)
        
        test_data_dir = self.root_dir / "data" / "test"
        self.create_directory(test_data_dir)
        
        test_files = [
            "comprehensive_test_data.json",
            "domains.txt",
            "rag_system_test_cases.csv",
            "rag_system_test_data.json",
            "rules_engine_test_cases.csv",
            "rules_engine_test_data.json",
            "routing_decisions.jsonl",
            "validation_results.json"
        ]
        
        results = {}
        for test_file in test_files:
            source = self.root_dir / test_file
            destination = test_data_dir / test_file
            results[test_file] = self.move_file(source, destination)
            
        return results
        
    def phase3_move_documentation(self) -> Dict[str, bool]:
        """Phase 3: Move documentation to docs/guides/"""
        self.log("\n" + "="*60)
        self.log("PHASE 3: Moving Documentation")
        self.log("="*60)
        
        guides_dir = self.root_dir / "docs" / "guides"
        self.create_directory(guides_dir)
        
        doc_files = [
            "CLIENT_SETUP_GUIDE.md",
            "IMPLEMENTATION_PACKAGE.md",
            "NETWORK_WHITELIST.md",
            "SETUP_GUIDE.md"
        ]
        
        results = {}
        for doc_file in doc_files:
            source = self.root_dir / doc_file
            destination = guides_dir / doc_file
            results[doc_file] = self.move_file(source, destination)
            
        return results
        
    def phase4_archive_launchers(self) -> Dict[str, bool]:
        """Phase 4: Archive unused launchers"""
        self.log("\n" + "="*60)
        self.log("PHASE 4: Archiving Unused Launchers")
        self.log("="*60)
        
        launchers_dir = self.root_dir / "legacy" / "launchers"
        self.create_directory(launchers_dir)
        
        launcher_files = [
            "launch_demo_intelligent.py",
            "launch_enhanced_demo.py",
            "launch_safe_demo.bat"
        ]
        
        results = {}
        for launcher_file in launcher_files:
            source = self.root_dir / launcher_file
            # Check if file is referenced
            references = self.check_file_references(launcher_file)
            if references:
                self.log(f"⚠️  {launcher_file} is referenced in: {', '.join(references)}", "WARNING")
                self.log("   Skipping move. Review references first.", "WARNING")
                results[launcher_file] = False
                continue
                
            destination = launchers_dir / launcher_file
            results[launcher_file] = self.move_file(source, destination)
            
        return results
        
    def phase5_move_utilities(self) -> Dict[str, bool]:
        """Phase 5: Move utility scripts"""
        self.log("\n" + "="*60)
        self.log("PHASE 5: Moving Utility Scripts")
        self.log("="*60)
        
        utils_dir = self.root_dir / "scripts" / "utils"
        self.create_directory(utils_dir)
        
        utility_files = [
            "test_data_generator.py",
            "validate_setup.py",
            "validation_summary.py",
            "validate_test_data.py"
        ]
        
        results = {}
        for util_file in utility_files:
            source = self.root_dir / util_file
            
            # Check if similar file exists in scripts/
            potential_duplicate = self.root_dir / "scripts" / util_file
            if potential_duplicate.exists():
                self.log(f"⚠️  Duplicate found: scripts/{util_file} already exists", "WARNING")
                self.log("   Skipping move. Review duplicates first.", "WARNING")
                results[util_file] = False
                continue
                
            destination = utils_dir / util_file
            results[util_file] = self.move_file(source, destination)
            
        return results
        
    def phase6_move_test_scripts(self) -> Dict[str, bool]:
        """Phase 6: Move test scripts to tests/integration/"""
        self.log("\n" + "="*60)
        self.log("PHASE 6: Moving Test Scripts")
        self.log("="*60)
        
        integration_tests_dir = self.root_dir / "tests" / "integration"
        self.create_directory(integration_tests_dir)
        
        test_files = [
            "test_enhanced_routing_intelligence.py",
            "test_full_pinecone.py",
            "test_pinecone_connection.py",
            "test_regions.py",
            "test_vector_operations.py",
            "quick_pinecone_test.py"
        ]
        
        results = {}
        for test_file in test_files:
            source = self.root_dir / test_file
            destination = integration_tests_dir / test_file
            results[test_file] = self.move_file(source, destination)
            
        return results
        
    def phase7_move_setup_scripts(self) -> Dict[str, bool]:
        """Phase 7: Move setup scripts to scripts/setup/"""
        self.log("\n" + "="*60)
        self.log("PHASE 7: Moving Setup Scripts")
        self.log("="*60)
        
        setup_dir = self.root_dir / "scripts" / "setup"
        self.create_directory(setup_dir)
        
        setup_files = [
            "setup_env.py",
            "quick_setup.py"
        ]
        
        results = {}
        for setup_file in setup_files:
            source = self.root_dir / setup_file
            destination = setup_dir / setup_file
            results[setup_file] = self.move_file(source, destination)
            
        return results
        
    def phase8_move_migration_scripts(self) -> Dict[str, bool]:
        """Phase 8: Move migration scripts to scripts/migrations/"""
        self.log("\n" + "="*60)
        self.log("PHASE 8: Moving Migration Scripts")
        self.log("="*60)
        
        migrations_dir = self.root_dir / "scripts" / "migrations"
        self.create_directory(migrations_dir)
        
        migration_files = [
            "vector_routing_intelligence_migration.py"
        ]
        
        results = {}
        for migration_file in migration_files:
            source = self.root_dir / migration_file
            destination = migrations_dir / migration_file
            results[migration_file] = self.move_file(source, destination)
            
        return results
        
    def phase9_cleanup_artifacts(self) -> Dict[str, bool]:
        """Phase 9: Clean up build artifacts"""
        self.log("\n" + "="*60)
        self.log("PHASE 9: Cleaning Build Artifacts")
        self.log("="*60)
        
        artifacts = [
            ".coverage",
            "coverage.xml"
        ]
        
        results = {}
        for artifact in artifacts:
            file_path = self.root_dir / artifact
            if file_path.exists():
                results[artifact] = self.delete_file(file_path)
            else:
                self.log(f"✓ Artifact not found (already clean): {artifact}")
                results[artifact] = True
                
        # Update .gitignore
        gitignore_path = self.root_dir / ".gitignore"
        if gitignore_path.exists():
            try:
                content = gitignore_path.read_text(encoding='utf-8')
                updates_needed = []
                
                if ".coverage" not in content:
                    updates_needed.append(".coverage")
                if "coverage.xml" not in content:
                    updates_needed.append("coverage.xml")
                    
                if updates_needed and not self.dry_run:
                    with open(gitignore_path, 'a', encoding='utf-8') as f:
                        f.write("\n# Coverage reports\n")
                        for item in updates_needed:
                            f.write(f"{item}\n")
                    self.log(f"✓ Updated .gitignore with: {', '.join(updates_needed)}")
                elif updates_needed:
                    self.log(f"✓ Would update .gitignore with: {', '.join(updates_needed)}")
                else:
                    self.log("✓ .gitignore already contains coverage entries")
                    
            except Exception as e:
                self.log(f"✗ Failed to update .gitignore: {e}", "ERROR")
                
        return results
        
    def phase10_evaluate_packages_txt(self) -> Dict[str, bool]:
        """Phase 10: Evaluate packages.txt"""
        self.log("\n" + "="*60)
        self.log("PHASE 10: Evaluating packages.txt")
        self.log("="*60)
        
        packages_txt = self.root_dir / "packages.txt"
        requirements_txt = self.root_dir / "requirements.txt"
        
        results = {}
        
        if packages_txt.exists() and requirements_txt.exists():
            # Compare files
            packages_content = packages_txt.read_text(encoding='utf-8').strip()
            requirements_content = requirements_txt.read_text(encoding='utf-8').strip()
            
            if packages_content == requirements_content:
                self.log("✓ packages.txt is identical to requirements.txt")
                self.log("  Recommendation: Delete packages.txt")
                results["packages.txt"] = True
            else:
                self.log("⚠️  packages.txt differs from requirements.txt", "WARNING")
                self.log("  Review differences before deletion")
                results["packages.txt"] = False
        elif not packages_txt.exists():
            self.log("✓ packages.txt not found (already clean)")
            results["packages.txt"] = True
        else:
            self.log("⚠️  requirements.txt not found", "WARNING")
            results["packages.txt"] = False
            
        return results
        
    def save_backup_manifest(self):
        """Save backup manifest for potential rollback."""
        manifest_path = self.root_dir / "cleanup_backup_manifest.json"
        
        manifest_data = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": self.dry_run,
            "operations": self.backup_manifest,
            "log": self.operations_log
        }
        
        try:
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest_data, f, indent=2)
            self.log(f"\n✓ Backup manifest saved: {manifest_path}")
        except Exception as e:
            self.log(f"✗ Failed to save backup manifest: {e}", "ERROR")
            
    def print_summary(self, all_results: Dict[str, Dict[str, bool]]):
        """Print summary of all operations."""
        self.log("\n" + "="*60)
        self.log("CLEANUP SUMMARY")
        self.log("="*60)
        
        total_operations = 0
        successful_operations = 0
        
        for phase, results in all_results.items():
            total = len(results)
            successful = sum(1 for v in results.values() if v)
            total_operations += total
            successful_operations += successful
            
            status = "✓" if successful == total else "⚠️"
            self.log(f"{status} {phase}: {successful}/{total} operations successful")
            
        self.log("\n" + "-"*60)
        self.log(f"TOTAL: {successful_operations}/{total_operations} operations successful")
        
        if self.dry_run:
            self.log("\n🔍 DRY RUN MODE - No files were actually moved")
            self.log("   Run with --execute flag to perform actual operations")
        else:
            self.log("\n✓ Cleanup completed!")
            self.log("   Review the backup manifest for rollback information")
            
    def execute_cleanup(self, dry_run: bool = True):
        """Execute all cleanup phases."""
        self.dry_run = dry_run
        
        mode = "DRY RUN" if dry_run else "EXECUTE"
        self.log("\n" + "="*60)
        self.log(f"ROOT DIRECTORY CLEANUP - {mode} MODE")
        self.log("="*60)
        self.log(f"Root directory: {self.root_dir}")
        self.log(f"Mode: {mode}")
        
        all_results = {}
        
        # Execute all phases
        all_results["Phase 1: Demo Files"] = self.phase1_move_demos()
        all_results["Phase 2: Test Data"] = self.phase2_move_test_data()
        all_results["Phase 3: Documentation"] = self.phase3_move_documentation()
        all_results["Phase 4: Launchers"] = self.phase4_archive_launchers()
        all_results["Phase 5: Utilities"] = self.phase5_move_utilities()
        all_results["Phase 6: Test Scripts"] = self.phase6_move_test_scripts()
        all_results["Phase 7: Setup Scripts"] = self.phase7_move_setup_scripts()
        all_results["Phase 8: Migration Scripts"] = self.phase8_move_migration_scripts()
        all_results["Phase 9: Build Artifacts"] = self.phase9_cleanup_artifacts()
        all_results["Phase 10: Packages.txt"] = self.phase10_evaluate_packages_txt()
        
        # Save backup manifest
        self.save_backup_manifest()
        
        # Print summary
        self.print_summary(all_results)
        
        return all_results


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Clean up root directory by organizing files into appropriate subdirectories"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the cleanup (default is dry-run mode)"
    )
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="Root directory path (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # Get root directory
    root_dir = Path(args.root).resolve()
    if not root_dir.exists():
        print(f"Error: Root directory not found: {root_dir}")
        sys.exit(1)
        
    # Create cleanup manager
    manager = RootCleanupManager(root_dir)
    
    # Execute cleanup
    results = manager.execute_cleanup(dry_run=not args.execute)
    
    # Exit with appropriate code
    all_successful = all(
        all(results[phase].values()) 
        for phase in results
    )
    
    sys.exit(0 if all_successful else 1)


if __name__ == "__main__":
    main()
