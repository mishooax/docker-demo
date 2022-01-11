from setuptools import setup, find_packages

setup(
    name="docker_demo",
    version="0.1",
    description="Dummy pytorch model for use through Docker",
    author="Mihai Alexe",
    author_email="ma@ecmwf",
    url="https://github.com/mishooax/docker-demo",
    packages=find_packages(include=["docker_demo", "docker_demo.*"]),
    entry_points={
        "console_scripts": [
            "docker-demo-train=docker_demo.train:main",
        ]
    },
)