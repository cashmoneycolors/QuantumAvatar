#!/usr/bin/env python3
"""
SIMPLE TEST SCRIPT - QUantum Avatar Business Empire Test
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all important imports"""
    print("🧪 TESTING CASH MONEY COLORS APP IMPORTS")

    try:
        # Core imports
        import sqlite3
        print("✅ SQLite3 available")

        import tkinter as tk
        print("✅ Tkinter available")

        # Database
        from db.manager import get_database
        db = get_database()
        print("✅ Database manager loaded")

        # Config
        from core.config import API_CONFIG, create_config_structure
        print("✅ Config system loaded")

        # AI Manager
        from ai.manager import AIManager
        ai_mgr = AIManager(db)
        print("✅ AI Manager loaded")

        # Logger
        from utils.logger import log_system_health, get_logger_instance
        print("✅ Logging system loaded")

        print("\n🚀 ALL IMPORTS SUCCESSFUL!")
        return True

    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dependencies():
    """Test important dependencies"""
    print("\n🔧 TESTING DEPENDENCIES")

    try:
        import openai
        print("✅ OpenAI available")

        import anthropic
        print("✅ Anthropic available")

        import requests
        print("✅ Requests available")

        print("\n💎 ALL DEPENDENCIES AVAILABLE!")
        return True

    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def test_database():
    """Test database functionality"""
    print("\n🗄️ TESTING DATABASE")

    try:
        from db.manager import get_database

        db = get_database()

        # Test basic operations
        stats = db.get_stats()
        print(f"✅ Database stats: {stats}")

        # Test search
        results = db.search_knowledge("test")
        print(f"✅ Search test: {len(results)} results")

        print("\n💾 DATABASE WORKING!")
        return True

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_config():
    """Test configuration system"""
    print("\n⚙️ TESTING CONFIGURATION")

    try:
        from core.config import API_CONFIG

        print(f"✅ API Config loaded: Grok={bool(API_CONFIG.grok_key[:5] if API_CONFIG.grok_key else False)}...")

        print("\n🔧 CONFIGURATION WORKING!")
        return True

    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def main():
    """Main test function"""
    print("*** QUANTUM AVATAR BUSINESS EMPIRE - SYSTEM TEST ***")
    print("===================================================")

    all_tests_passed = True

    # Run all tests
    all_tests_passed &= test_imports()
    all_tests_passed &= test_dependencies()
    all_tests_passed &= test_database()
    all_tests_passed &= test_config()

    if all_tests_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("💎 YOUR QUANTUM AVATAR BUSINESS EMPIRE IS READY!")
        print("\n🔥 TO START THE APP:")
        print("python main.py")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("Please fix the errors above before launching.")

if __name__ == "__main__":
    main()
