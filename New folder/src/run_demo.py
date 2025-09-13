#!/usr/bin/env python3
"""
Simple startup script for the AI Financial Multi-Agent System.
This script handles missing configuration gracefully and provides helpful guidance.
"""

import os
import sys
from pathlib import Path

def check_and_create_env():
    """Check for .env file and create one if missing."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        print("🔧 No .env file found. Creating one from template...")
        
        if env_example.exists():
            # Copy from example
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✅ Created .env file from .env.example")
        else:
            # Create minimal .env
            minimal_env = """# AI Financial Multi-Agent System Configuration

# Environment
ENVIRONMENT=development
DEBUG=true

# API Configuration  
API_HOST=0.0.0.0
API_PORT=8000

# OpenAI Configuration (Optional for demo)
# OPENAI_API_KEY=sk-your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Security (Auto-generated for development)
# SECRET_KEY will be auto-generated if not set

# Database Configuration (Optional for demo)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=ai_financial
POSTGRES_PASSWORD=password
POSTGRES_DB=ai_financial

# Redis Configuration (Optional for demo)
REDIS_URL=redis://localhost:6379

# Monitoring (Optional)
LOG_LEVEL=INFO
"""
            
            with open(env_file, 'w') as f:
                f.write(minimal_env)
            
            print("✅ Created minimal .env file")
        
        print(f"📝 Please edit {env_file} to configure your settings")
        print("💡 The system will work in demo mode without OpenAI API key")
        return True
    
    return False

def main():
    """Main startup function."""
    print("🏦 AI Financial Multi-Agent System")
    print("=" * 50)
    
    # Check for .env file
    env_created = check_and_create_env()
    
    if env_created:
        print("\n⚠️  Configuration file created. You can:")
        print("   1. Run the demo as-is (limited functionality)")
        print("   2. Add OPENAI_API_KEY to .env for full AI capabilities")
        print("   3. Configure database connections for persistence")
        print()
    
    # Import after env setup
    try:
        from ai_financial.core.config import settings
        print(f"🔧 Environment: {settings.environment}")
        print(f"🔧 Debug mode: {settings.debug}")
        print(f"🔧 API endpoint: http://{settings.api_host}:{settings.api_port}")
        
        if settings.llm.has_openai_key:
            print("✅ OpenAI API key configured")
        else:
            print("⚠️  OpenAI API key not configured (demo mode)")
        
        print()
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your .env file configuration")
        return 1
    
    # Ask user what they want to do
    print("What would you like to do?")
    print("1. Run interactive demo")
    print("2. Start web server")
    print("3. Run CLI chat")
    print("4. Show system status")
    print("5. Exit")
    
    try:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            print("\n🚀 Starting interactive demo...")
            from demo import main as demo_main
            import asyncio
            asyncio.run(demo_main())
            
        elif choice == "2":
            print(f"\n🚀 Starting web server on http://{settings.api_host}:{settings.api_port}")
            print("Press Ctrl+C to stop")
            from ai_financial.main import run_server
            import asyncio
            asyncio.run(run_server())
            
        elif choice == "3":
            print("\n💬 Starting CLI chat...")
            from ai_financial.cli import main as cli_main
            # Simulate chat command
            sys.argv = ["ai-financial", "chat"]
            cli_main()
            
        elif choice == "4":
            print("\n📊 System status...")
            from ai_financial.cli import main as cli_main
            # Simulate status command
            sys.argv = ["ai-financial", "status"]
            cli_main()
            
        elif choice == "5":
            print("👋 Goodbye!")
            return 0
            
        else:
            print("❌ Invalid choice")
            return 1
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())