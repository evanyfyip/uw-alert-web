"""
Setup module that creates the
environment and installs dependencies
to use the application.
"""
from setuptools import setup, find_packages

with open('requirements.txt', mode='r', encoding=str) as f:
    requirements = f.read().splitlines()

setup(
    name="uw-alert-web",
    license="MIT",
    version="1.0",
    description="Visualize incidents/announcements from the UW Alert system",
    long_description="""
                        The goal of this tool is to display an interactive map
                        that displays incidents/announcements from the UW Alert system.
                        This allows students to see unsafe areas and avoid them.

                        The tool has 3 components:
                        - Web app that hosts the map
                        - Visual markers for impacted areas on the map
                        - Text parser to process UW Alerts message
                     """,
    author=" James Joko | John Michael | Mark Qiao | Evan Yip",
    author_email="jjoko@uw.edu, jmic94@uw.edu, mtqiao@uw.edu, eyfy@uw.edu",
    url="https://github.com/evanyfyip/uw-alert-web",
    classifiers= ["Development Status :: Alpha",
                  "Environment :: Other Audience",
                  "Intended Audience :: General",
                  "License :: OSI Approved :: MIT License",
                  "Operating System :: OS Independent",
                  'Programming Language :: Python :: 3.10',
                  'Programming Language :: Python :: 3.11',
                  "Topic :: Communications"],
    packages=find_packages(),
    install_requires=requirements,
)
