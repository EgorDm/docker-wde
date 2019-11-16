import setuptools

setuptools.setup(
    name="web_dev_env_tools",
    version="0.1.0",
    author="Egor Dmitriev",
    author_email="egordmitriev2@gmail.com",
    description="WebDevEnv Tools",
    long_description='WebDevEnv Tools',
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'wde = web_dev_env_tools.cli:cli'
        ]
    }
)
