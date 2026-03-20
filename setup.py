from setuptools import setup, find_packages

setup(
    name="goskill",
    version="1.0.0",
    author="Andy (AI PM)",
    author_email="andy@aipm.com",
    description="Let your Skill keep running until goal achieved",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AIPMAndy/goskill",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "goskill=goskill.cli:main",
        ],
    },
)
