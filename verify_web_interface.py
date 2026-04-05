#!/usr/bin/env python3
"""
Web Interface Verification Script
===================================
This script verifies that all web interface files are correctly set up.
Run this before starting the web server to ensure everything is ready.
"""

import os
import sys
from pathlib import Path

def check_file(path, expected_type="file"):
    """Check if a file or directory exists."""
    full_path = Path(path)
    if expected_type == "file":
        if full_path.is_file():
            size = full_path.stat().st_size
            return True, f"✓ Found ({size} bytes)"
        else:
            return False, "✗ Not found"
    elif expected_type == "directory":
        if full_path.is_dir():
            return True, "✓ Found"
        else:
            return False, "✗ Not found"
    return False, "? Unknown"

def main():
    print("\n" + "="*70)
    print("  WEB INTERFACE VERIFICATION")
    print("="*70)
    
    base_path = Path(".")
    
    # Check directory structure
    print("\n📁 DIRECTORY STRUCTURE")
    print("-" * 70)
    
    dirs_to_check = [
        ("templates", "directory"),
        ("static", "directory"),
    ]
    
    all_good = True
    for path, dtype in dirs_to_check:
        full_path = base_path / path
        ok, msg = check_file(full_path, dtype)
        status = "✓" if ok else "✗"
        print(f"{status} {path:30} | {msg}")
        if not ok:
            all_good = False
    
    # Check core files
    print("\n🔧 CORE APPLICATION FILES")
    print("-" * 70)
    
    core_files = [
        ("enzyme_calculator.py", "file"),
        ("enzyme_calculator_web.py", "file"),
        ("enzyme_calculator_examples.py", "file"),
        ("test_enzyme_calculator.py", "file"),
        ("requirements.txt", "file"),
    ]
    
    for path, dtype in core_files:
        full_path = base_path / path
        ok, msg = check_file(full_path, dtype)
        status = "✓" if ok else "✗"
        print(f"{status} {path:30} | {msg}")
        if not ok:
            all_good = False
    
    # Check web interface files
    print("\n🌐 WEB INTERFACE FILES")
    print("-" * 70)
    
    web_files = [
        ("templates/index.html", "file"),
        ("static/style.css", "file"),
        ("static/script.js", "file"),
    ]
    
    for path, dtype in web_files:
        full_path = base_path / path
        ok, msg = check_file(full_path, dtype)
        status = "✓" if ok else "✗"
        print(f"{status} {path:30} | {msg}")
        if not ok:
            all_good = False
    
    # Check documentation
    print("\n📚 DOCUMENTATION")
    print("-" * 70)
    
    doc_files = [
        ("ENZYME_CALCULATOR_README.md", "file"),
        ("ENZYME_CALCULATOR_REFERENCE.md", "file"),
        ("WEB_INTERFACE_README.md", "file"),
    ]
    
    for path, dtype in doc_files:
        full_path = base_path / path
        ok, msg = check_file(full_path, dtype)
        status = "✓" if ok else "✗"
        print(f"{status} {path:30} | {msg}")
        # Documentation is nice-to-have, don't fail if missing
    
    # Summary
    print("\n" + "="*70)
    if all_good:
        print("  ✓ ALL CHECKS PASSED - Web interface is ready!")
        print("="*70)
        print("\n  Next: Run 'python enzyme_calculator_web.py'")
        print("  Then: Open http://localhost:5000 in your browser")
        return 0
    else:
        print("  ✗ SOME CHECKS FAILED - Please review above")
        print("="*70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
