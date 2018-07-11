import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
        name='pinplot',
        version='0.1.0.post1',
        author='neophyliam',
        author_email='neophyliam@gmail.com',
        url='https://github.com/Neophyliam/pinplot',
        description='A simple tool for plotting pins '
                'in lattice of a nuclear reactor.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        py_modules=['pin_plot'],
        install_requires=['matplotlib', 'numpy'],
        classifiers=(
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            )
        )
