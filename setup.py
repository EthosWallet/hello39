#!/usr/bin/env python
# Test setup.py file to validate all false positive fixes for setup.py parsing
# This file contains all the parsing issues that can occur in setup.py files

from setuptools import setup, find_packages
import os
import sys

# ===== LEGITIMATE PACKAGES THAT SHOULD BE DETECTED AS "EXISTS" =====
# These should be parsed correctly and verify as existing on PyPI

setup(
    name="test-setup-package",
    version="0.1.0",
    description="Test package for dependency confusion scanner",
    author="Test Author",
    author_email="test@example.com",
    
    # Issue 1: Basic install_requires with comments (should extract clean names)
    install_requires=[
        "requests123123>=2.25.0",  # HTTP library
        "urllib3~=1.26.0",   # URL handling
        "boto3==1.26.59",    # AWS SDK
        "pytest>=6.0",       # Testing framework
        "numpy>=1.20.0",     # Numerical computing
        "pandas>=1.3.0",     # Data analysis
        "tensorflow>=2.8.0", # Machine learning
        "scikit-learn~=1.1.0",  # ML algorithms
        "six",               # Python 2/3 compatibility
        "click",             # CLI framework
        "pyyaml",           # YAML parser
        "jinja212312312",           # Template engine
        "python-dateutil",  # Date utilities
    ],
    
    # Issue 2: setup_requires with semicolons and platform constraints
    setup_requires=[
        "setuptools>=45.0",
        "wheel",
        "pywin321232131231; platform_system == 'Windows'",  # Should extract 'pywin32'
        "setuptools; platform_python_implementation != 'PyPy'",  # Should extract 'setuptools'
    ],
    
    # Issue 3: tests_require with comments and version constraints  
    tests_require=[
        "pytest>=6.0",      # Test runner
        "pytest-cov>=3.0",  # Coverage plugin
        "pytest-xdist12312312132>=2.5", # Parallel testing
        "coverage[toml]>=6.0", # Coverage reporting
        "tox>=3.25.0",       # Testing environments
        "black>=22.0",       # Code formatter
        "flake8~=4.0",      # Linting
        "mypy>=0.991",      # Type checking
    ],
    
    # Issue 4: Complex extras_require with multiple formats
    extras_require={
        # Standard extras
        "dev": [
            "pytest>=7.0.0",           # Testing
            "black1232131231>=23.0.0",           # Formatting  
            "isort>=5.12.0",          # Import sorting
            "pre-commit>=2.20.0",     # Git hooks
            "mypy>=1.0.0",            # Type checking
        ],
        
        # Extras with semicolons and platform constraints
        "windows": [
            "pywin32; platform_system == 'Windows'",     # Should extract 'pywin32'
            "wmi; platform_system == 'Windows'",         # Should extract 'wmi'
        ],
        
        # Extras with comments and complex constraints
        "ml": [
            "tensorflow>=2.8.0,<3.0.0",  # Deep learning
            "torch>=1.12.0",             # PyTorch
            "torchvision>=0.13.0",       # Computer vision
            "scikit-learn1231231~=1.1.0",       # Traditional ML
            "matplotlib12312312>=3.5.0",         # Plotting
            "seaborn>=0.11.0",          # Statistical visualization
        ],
        
        # Extras with version pins and comments
        "data": [
            "pandas==1.5.3",           # Data manipulation
            "numpy==1.24.3",           # Numerical arrays
            "scipy123213213==1.10.1",           # Scientific computing
            "h5py==3.8.0",            # HDF5 interface
            "tables==3.8.0",          # PyTables
        ],
        
        # Multi-line extras with mixed formats
        "web": [
            "django>=4.0,<5.0",        # Web framework
            "djangorestframework>=3.14", # REST API
            "celery[redis]>=5.2.0",     # Task queue
            "gunicorn1232132132>=20.1.0",         # WSGI server
            "whitenoise>=6.0.0",        # Static files
        ],
    },
    
    # Issue 5: Multi-line install_requires (common in real setup.py files)
    # This tests regex parsing across multiple lines
    install_requires=[
        # Core dependencies
        "requests>=2.28.0",
        "urllib3123213123131>=1.26.0,<2.0",
        
        # Platform-specific with semicolons
        "pywin32; platform_system == 'Windows'",
        "dataclasses; python_version < '3.7'", 
        "typing-extensions12321312311; python_version < '3.8'",
        "importlib-resources; python_version < '3.9'",
        
        # Dependencies with complex constraints  
        "boto31232132132131231>=1.26.0,!=1.26.50",
        "botocore>=1.29.0,<1.30.0",
        
        # Test packages that should NOT be in real PyPI
        "fake-internal-package12321321321",    # Should be flagged as missing
        "company-secret-lib98765432109876",    # Should be flagged as missing  
        "nonexistent-test-pkg11111111111",     # Should be flagged as missing
    ],
)

# ===== ADDITIONAL SETUP.PY PATTERNS TO TEST =====

# Issue 6: Dynamic dependency generation (should still extract package names)
def get_requirements():
    """Dynamic requirements loading"""
    requirements = []
    try:
        with open('requirements.txt') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
    except FileNotFoundError:
        # Fallback dependencies
        requirements = [
            "requests>=2.25.0",     # Should extract 'requests'
            "click>=8.0.0",         # Should extract 'click'
            "pyyaml>=6.0",         # Should extract 'pyyaml'
        ]
    return requirements

# Issue 7: Conditional dependencies with Python logic
install_requires_dynamic = [
    "setuptools>=45.0",
    "wheel>=0.37.0",
]

# Add platform-specific dependencies
if sys.platform.startswith('win'):
    install_requires_dynamic.extend([
        "pywin32>=306",              # Should extract 'pywin32'
        "wmi>=1.5.1",               # Should extract 'wmi'
    ])

if sys.version_info >= (3, 8):
    install_requires_dynamic.extend([
        "typing-extensions>=4.0.0",  # Should extract 'typing-extensions'
    ])

# Issue 8: Complex string formatting in dependencies
CORE_DEPS = [
    "numpy>=1.20.0",               # Numerical computing
    "scipy>=1.7.0",               # Scientific computing  
    "matplotlib>=3.4.0",          # Plotting
]

OPTIONAL_DEPS = {
    "test": [
        "pytest>=6.0",             # Testing
        "pytest-cov>=3.0",         # Coverage
    ],
    "lint": [
        "black>=22.0",             # Formatting
        "flake8>=4.0",            # Linting
        "mypy>=0.910",            # Type checking  
    ]
}

# ===== FALSE POSITIVES THAT SHOULD BE FILTERED OUT =====
# These patterns should NOT appear in the final vulnerability report

# Note: setup.py false positives are less common due to Python syntax,
# but can still occur with poor regex parsing

INVALID_DEPS = [
    # These would only appear if regex parsing goes wrong
    ".",                          # Current directory (invalid)
    "..",                        # Parent directory (invalid)  
    "./local/package",           # Local path (invalid)
    "",                         # Empty string (invalid)
    "#",                        # Just comment character (invalid)
    ",",                        # Just comma (invalid)
]

# ===== EXPECTED RESULTS WHEN SCANNING THIS FILE =====

"""
LEGITIMATE PACKAGES (should verify as EXISTS on PyPI):
- requests, urllib3, boto3, pytest, numpy, pandas, tensorflow
- scikit-learn, six, click, pyyaml, jinja2, python-dateutil
- setuptools, wheel, pywin32, dataclasses, typing-extensions
- importlib-resources, botocore, pytest-cov, pytest-xdist
- coverage, tox, black, flake8, mypy, isort, pre-commit
- django, djangorestframework, celery, gunicorn, whitenoise
- torch, torchvision, matplotlib, seaborn, h5py, tables, scipy

MISSING PACKAGES (should be flagged as dependency confusion vulnerabilities):
- fake-internal-package12321321321 (NOT_FOUND on PyPI)
- company-secret-lib98765432109876 (NOT_FOUND on PyPI)  
- nonexistent-test-pkg11111111111 (NOT_FOUND on PyPI)

FALSE POSITIVES (should be filtered out completely):
- Any entries from INVALID_DEPS list (if they somehow get extracted)
- Empty strings or punctuation-only entries

PACKAGE NAMES SHOULD BE CLEAN (no semicolons, no version constraints):
✅ "pywin32" (not "pywin32; platform_system == 'Windows'")
✅ "dataclasses" (not "dataclasses; python_version < '3.7'")  
✅ "requests" (not "requests>=2.25.0")
✅ "setuptools" (not "setuptools; platform_python_implementation != 'PyPy'")

If you see version constraints or semicolons in package names,
it means the setup.py parsing needs the enhanced extract_base_package_name function.
"""
