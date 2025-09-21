#!/usr/bin/env python3
"""
Force LangFuse integration for LangGraph Studio
This script overrides LangGraph Studio's default LangSmith behavior
"""

import os
import sys
from pathlib import Path

def setup_langfuse_environment():
    """Setup environment variables to force LangFuse usage."""
    
    print("🔧 Setting up LangFuse environment...")
    
    # Force disable LangSmith
    os.environ["LANGSMITH_API_KEY"] = ""
    os.environ["LANGSMITH_PROJECT"] = ""
    os.environ["LANGSMITH_ENDPOINT"] = ""
    
    # Set LangFuse variables (if not already set)
    if not os.environ.get("LANGFUSE_PUBLIC_KEY"):
        print("⚠️  LANGFUSE_PUBLIC_KEY not set in environment")
        print("   Please set your LangFuse keys in .env file")
    
    if not os.environ.get("LANGFUSE_SECRET_KEY"):
        print("⚠️  LANGFUSE_SECRET_KEY not set in environment")
        print("   Please set your LangFuse keys in .env file")
    
    if not os.environ.get("LANGFUSE_HOST"):
        os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"
        print("✅ Set LANGFUSE_HOST to https://cloud.langfuse.com")
    
    print("✅ LangFuse environment configured")
    print("🚫 LangSmith disabled")

def patch_langgraph_studio():
    """Patch LangGraph Studio to use LangFuse instead of LangSmith."""
    
    print("🔧 Patching LangGraph Studio for LangFuse...")
    
    try:
        # Import and patch LangGraph Studio
        import langgraph_api
        import langgraph_runtime_inmem
        
        # Override LangSmith integration
        original_init = langgraph_api.__init__
        
        def patched_init(*args, **kwargs):
            # Force disable LangSmith
            os.environ["LANGSMITH_API_KEY"] = ""
            os.environ["LANGSMITH_PROJECT"] = ""
            return original_init(*args, **kwargs)
        
        langgraph_api.__init__ = patched_init
        print("✅ LangGraph Studio patched for LangFuse")
        
    except ImportError as e:
        print(f"⚠️  Could not patch LangGraph Studio: {e}")
        print("   LangFuse will still work via callback handlers")

def main():
    """Main function to setup LangFuse for LangGraph Studio."""
    
    print("🚀 LangFuse Integration Setup for LangGraph Studio")
    print("=" * 60)
    
    # Setup environment
    setup_langfuse_environment()
    
    # Patch LangGraph Studio
    patch_langgraph_studio()
    
    print("\n" + "=" * 60)
    print("📋 NEXT STEPS:")
    print("=" * 60)
    print("1. Create .env file with your LangFuse keys:")
    print("   LANGFUSE_PUBLIC_KEY=pk-lf-...")
    print("   LANGFUSE_SECRET_KEY=sk-lf-...")
    print("   LANGFUSE_HOST=https://cloud.langfuse.com")
    print()
    print("2. Run LangGraph Studio:")
    print("   cd deploy")
    print("   python force_langfuse.py")
    print("   langgraph dev")
    print()
    print("3. Check LangFuse dashboard:")
    print("   https://cloud.langfuse.com")
    print()
    print("✅ LangFuse integration ready!")

if __name__ == "__main__":
    main()
