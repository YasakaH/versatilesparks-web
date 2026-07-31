from setuptools import setup, find_packages

setup(
    name="agent-replay",
    version="0.1.0",
    description="Record, Replay, and Understand AI Agent Actions",
    long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Execution Proof",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        "openai": ["openai>=1.0"],
    },
    entry_points={
        "console_scripts": [
            "agent-replay=agent_replay.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "License :: OSI Approved :: MIT License",
    ],
)
