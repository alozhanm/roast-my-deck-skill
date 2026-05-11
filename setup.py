from setuptools import setup, find_packages

setup(
    name="roast-my-deck-skill",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "anthropic>=0.20.0",
        "pymupdf>=1.23.0",
        "python-dotenv>=1.0.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "roast=roast:main",
        ],
    },
    python_requires=">=3.10",
    author="roast-my-deck contributors",
    description="Brutally roast your pitch deck with Claude AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alizhannurgazy/roast-my-deck-skill",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
