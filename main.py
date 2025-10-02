#!/usr/bin/env python3
"""
🎯 Telco Call Centre Agent - Main Entry Point
Unified launcher for the telco ticket classification system

This module provides a command-line interface to:
- Launch the Streamlit demo
- Train models
- Run tests
- Validate the system

Author: Telco Call Centre Team
Date: October 2, 2025
"""

import sys
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    """Main entry point with command-line interface."""
    parser = argparse.ArgumentParser(
        description='Telco Call Centre Agent - AI-powered ticket classification system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py demo          # Launch Streamlit demo
  python main.py train         # Train classification models
  python main.py test          # Run test suite
  python main.py validate      # Validate system components
        """
    )
    
    parser.add_argument(
        'command',
        choices=['demo', 'train', 'test', 'validate'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    if args.command == 'demo':
        print("🚀 Launching Streamlit demo...")
        import launch_demo
        launch_demo.launch_demo()
    
    elif args.command == 'train':
        print("🎯 Starting model training...")
        sys.path.insert(0, str(project_root / 'scripts'))
        from train_model import main as train_main
        train_main()
    
    elif args.command == 'test':
        print("🧪 Running test suite...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'pytest', 'tests/', '-v'])
    
    elif args.command == 'validate':
        print("✅ Validating system components...")
        sys.path.insert(0, str(project_root / 'scripts'))
        from validate_demo import validate_demo_components
        validate_demo_components()


if __name__ == "__main__":
    main()
