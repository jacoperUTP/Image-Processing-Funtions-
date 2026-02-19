from setuptools import setup
import os

# Read README.md for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ip_functions",
    version="2.0.0",
    py_modules=["ip_functions"],
    description="Librería completa de procesamiento de imágenes - Compatible con MATLAB",
    author="Universidad Tecnológica de Pereira",
    author_email="jacoper@utp.edu.co",
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pillow>=8.0',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education",
    ],
    keywords="image processing, matlab, computer vision, segmentation, morphology, filters, transforms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacoperUTP/Image-Processing-Funtions-",
    project_urls={
        "Bug Reports": "https://github.com/jacoperUTP/Image-Processing-Funtions-/issues",
        "Source": "https://github.com/jacoperUTP/Image-Processing-Funtions-",
        "Documentation": "https://github.com/jacoperUTP/Image-Processing-Funtions-/wiki",
    },
)