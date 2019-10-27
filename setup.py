from setuptools import setup, find_packages

setup(
    name='noisy_annotation',
    version='0.0.1',
    url='https://github.com/diego-s/noisy_annotation.git',
    author='Author Name',
    author_email='author@example.com',
    description='Description of my package',
    packages=find_packages(),    
    install_requires=[
        "flashtext", 
        "jupyter", 
        "pytest", 
        "sphinx", 
        "sphinx_rtd_theme", 
    ],
)
