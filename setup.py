from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='database-artifact-factory',
    version=open('version.txt','r').read(),
    packages=find_packages(),

    entry_points={
      "console_scripts": [
        "db-artifact-builder = db_artifact_builder.build_artifact:build_artifact_cli",
        "db-artifact-converge = db_artifact.converge_artifact:converge_artifact_cli"
      ]
    },
    install_requires=[
      'boto3==1.12.26',
      'docker'
    ],

    author='Eric Kascic',
    author_email='eric.kascic@stelligent.com',
    description='An RDS database factory for rapidly creating database copies',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/stelligent/database-artifact-factory',
    license='MIT',
    package_data={'': ['Dockerfile','*.yml','*.yaml']},
    python_requires='>=3.6'
)
