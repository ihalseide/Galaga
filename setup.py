import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="galaga-ihalseide",
    version="0.0.1",
    author="Izak Halseide",
    author_email="halseide.izak@gmail.com",
    description="A clone of the game Galaga",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ihalseide/Galaga",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU General Public License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "pygame >= 1.9.6"
    ]
)
