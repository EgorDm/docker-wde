import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rendertron_cache_server",
    version="0.1.0",
    author="Egor Dmitriev",
    author_email="egor.dmitriev@experius.nl",
    description="Rendertron Cache Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
