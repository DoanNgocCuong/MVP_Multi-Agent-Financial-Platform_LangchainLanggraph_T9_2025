# Package Metadata Directory

## 📁 Overview

The `ai_financial_multi_agent_system.egg-info/` directory contains package metadata generated during the installation process. This directory is automatically created when you install the package in development mode using `pip install -e .`.

## 🏗️ Directory Structure

```
ai_financial_multi_agent_system.egg-info/
├── dependency_links.txt    # External dependency links
├── entry_points.txt        # Console script entry points
├── PKG-INFO               # Package information and metadata
├── requires.txt           # Package dependencies
├── SOURCES.txt            # Source files included in package
└── top_level.txt          # Top-level package names
```

## 📋 File Descriptions

### `PKG-INFO`
Contains the main package metadata including:
- Package name and version
- Author information
- Description and long description
- License information
- Classifiers (Python version, development status, etc.)
- Keywords and project URLs

### `requires.txt`
Lists all package dependencies with version constraints:
```
fastapi>=0.104.0
langchain>=0.1.0
langgraph>=0.0.40
pydantic>=2.0.0
uvicorn>=0.24.0
```

### `dependency_links.txt`
Contains links to external dependencies (usually empty for standard packages):
```
# Empty for standard PyPI packages
```

### `entry_points.txt`
Defines console script entry points:
```
[console_scripts]
ai-financial = ai_financial.cli:main
```

### `SOURCES.txt`
Lists all source files included in the package:
```
ai_financial/__init__.py
ai_financial/main.py
ai_financial/cli.py
ai_financial/core/__init__.py
ai_financial/core/base_agent.py
# ... and more
```

### `top_level.txt`
Specifies the top-level package names:
```
ai_financial
```

## 🔧 Package Installation

### Development Installation

This directory is created when you install the package in development mode:

```bash
# Install in development mode (creates .egg-info directory)
pip install -e .

# Or install with all dependencies
pip install -e ".[dev]"
```

### Production Installation

For production installations, this directory is typically not present as the package is installed normally:

```bash
# Standard installation (no .egg-info directory)
pip install .
```

## 📦 Package Configuration

The package metadata is defined in `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ai-financial-multi-agent-system"
version = "0.1.0"
description = "AI Financial Multi-Agent System for SMBs"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.11"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]

[project.scripts]
ai-financial = "ai_financial.cli:main"
```

## 🚀 Console Scripts

The package provides a console script entry point:

```bash
# After installation, you can use:
ai-financial --help
ai-financial start
ai-financial chat
ai-financial status
```

This is defined in the `entry_points.txt` file and configured in `pyproject.toml`.

## 🔍 Package Information

### Version Information

Check the installed package version:

```bash
# Check package version
pip show ai-financial-multi-agent-system

# Or using Python
python -c "import ai_financial; print(ai_financial.__version__)"
```

### Dependencies

View package dependencies:

```bash
# List all dependencies
pip list

# Show dependency tree
pip show --verbose ai-financial-multi-agent-system
```

## 🛠️ Development Workflow

### Making Changes

When you make changes to the package:

1. **Code Changes**: Modify source files in `ai_financial/`
2. **Automatic Updates**: The `.egg-info` directory is automatically updated
3. **No Reinstallation**: Changes are immediately available (development mode)

### Updating Metadata

To update package metadata:

1. **Edit `pyproject.toml`**: Update version, dependencies, etc.
2. **Reinstall**: Run `pip install -e .` to update metadata
3. **Verify**: Check updated files in `.egg-info/`

## 📊 Package Distribution

### Building Distribution

To create distribution packages:

```bash
# Build source distribution
python -m build --sdist

# Build wheel distribution
python -m build --wheel

# Build both
python -m build
```

### Publishing

To publish to PyPI:

```bash
# Upload to PyPI
twine upload dist/*

# Upload to test PyPI first
twine upload --repository testpypi dist/*
```

## 🔧 Troubleshooting

### Common Issues

1. **Missing .egg-info Directory**
   - Run `pip install -e .` to create it
   - Ensure you're in the correct directory

2. **Outdated Metadata**
   - Reinstall with `pip install -e .`
   - Check `pyproject.toml` for correct configuration

3. **Entry Point Not Found**
   - Verify `entry_points.txt` contains the script
   - Check `pyproject.toml` configuration
   - Reinstall the package

### Cleaning Up

To remove the package and metadata:

```bash
# Uninstall package
pip uninstall ai-financial-multi-agent-system

# Remove .egg-info directory
rm -rf ai_financial_multi_agent_system.egg-info/
```

## 📚 Additional Resources

- **Setuptools Documentation**: https://setuptools.pypa.io/
- **Python Packaging Guide**: https://packaging.python.org/
- **PyPI Publishing Guide**: https://packaging.python.org/tutorials/packaging-projects/
- **Entry Points Documentation**: https://setuptools.pypa.io/en/latest/userguide/entry_point.html

## ⚠️ Important Notes

1. **Don't Edit Manually**: The files in this directory are automatically generated
2. **Version Control**: This directory is typically added to `.gitignore`
3. **Development Only**: This directory is only present in development installations
4. **Automatic Updates**: Changes to `pyproject.toml` require reinstallation to update metadata

## 🎯 Best Practices

1. **Keep pyproject.toml Updated**: Maintain accurate package metadata
2. **Version Management**: Use semantic versioning for releases
3. **Dependency Management**: Keep dependencies up to date
4. **Documentation**: Ensure README and docstrings are current
5. **Testing**: Test package installation and entry points

