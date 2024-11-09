from setuptools import setup, find_packages

setup(
    name="triesketch",           # Name of the project/package
    version="0.1",
    packages=find_packages(),     # Automatically finds all packages and subpackages
    install_requires=[],          # List any dependencies here
    python_requires=">=3.9",      # Specify the Python version required
    entry_points={
        "console_scripts": [
            "build_index=tests.build_index.build_index:main",  # Optional: makes `run-main` command available
        ],
    },
)