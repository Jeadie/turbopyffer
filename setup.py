from setuptools import setup, find_packages

def parse_requirements(filename: str) -> str:
    """Load requirements from a pip requirements file."""
    with open(filename, 'r') as f:
        requirements = f.read().splitlines()

    # Filter out comments or empty lines
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]
    return requirements

def parse_markdown(path: str) -> str:
    with open(path, "r", encoding="utf8") as fh:
        return fh.read()

def setup_package():
    setup(
        name="turbopyffer",
        version="0.0.1",
        maintainer="Jack Eadie",
        maintainer_email="jackeadie@duck.com",
        author="Jack Eadie",
        url="https://github.com/Jeadie/turbopyffer",
        description="Python SDK for TurboPuffer.",
        long_description=parse_markdown("README.md"),
        long_description_content_type="text/markdown",
        packages=["src"],
        install_requires=parse_requirements('requirements.txt'),
        python_requires=">=3.8",
        platforms=["Any"],
    )


if __name__ == "__main__":
    setup_package()
