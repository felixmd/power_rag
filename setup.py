from setuptools import setup, find_packages

setup(
    name="ragification",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "streamlit>=1.24.0",
        "sentence-transformers>=2.2.2",
        "faiss-cpu>=1.7.4",
        "numpy>=1.24.0",
        "python-pptx>=0.6.21"
    ],
) 