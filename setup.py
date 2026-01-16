#!/usr/bin/env python
from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy
#from setuptools import setup, find_packages
import re, os
def find_packages(path='.'):
    ret = []
    for root, dirs, files in os.walk(path):
        if '__init__.py' in files:
            ret.append(re.sub('^[^A-z0-9_]+', '', root.replace('/', '.')))
    return ret

python_requires = '>=3.11'
install_requires = [
    'numpy>=1.23,<3',
    'scipy>=1.10',
    'h5py>=3.8',
    'matplotlib>=3.7',
    'ipyparallel>=8.0',
    'tqdm>=4.60',
    'six>=1.16',
    'tornado>=6.0',
    'cloudpickle>=3.0',
    "alabtools>=1.1.29"
]

tests_require = [
    'mock'
]


extras_require = {
    'docs': [
        'Sphinx>=1.1', 
    ]
}

extensions = [
    Extension("igm.cython_compiled.sprite",
              ["igm/cython_compiled/sprite.pyx", "igm/cython_compiled/cpp_sprite_assignment.cpp"]),
]

extensions = cythonize(extensions)

setup(
        name = 'igm', 
        version = '2.0.2', 
        author = 'Guido Polles, Nan Hua, Lorenzo Boninsegna', 
        author_email = 'polles@usc.edu nhua@usc.edu bonimba@g.ucla.edu', 
        url = 'https://github.com/alberlab/igm', 
        description = 'Integrated Genome Modeling Plus',
        
        packages=find_packages('./igm/'),
        package_data={'igm.core' : ['defaults/*.json'],
                      'igm.ui': ['static/css/*', 'static/js/*', 'static/js/genome_visualizer/*', 'templates/*']},
        #package_data={'' : ['core/defaults/*', 'ui/static/css/*', 'ui/static/js/*', 'ui/static/js/genome_visualizer/*', 'ui/templates/*']},
        include_package_data=True,
        python_requires=python_requires,
        install_requires=install_requires,
        tests_require=tests_require,
        extras_require=extras_require,
        
        ext_modules=extensions,
        include_dirs=[numpy.get_include()],
        scripts=['bin/igm-run', 'bin/igm-run-mac', 'bin/igm-server', 'bin/igm-register-dir', 'bin/igm-info-dir',
                 'bin/igm-unregister-dir', 'bin/igm-stop', 'bin/igm-report'],
)
