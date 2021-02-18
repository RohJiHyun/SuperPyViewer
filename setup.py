from setuptools import setup, find_packages

setup(
    name             = 'SuperPyViewer',
    version          = '1.0',
    description      = 'python 3d viewer',
    author           = 'Ji Hyun Roh',
    author_email     = 'rohjihyun95@gmail.com',
    url              = 'https://github.com/RohJiHyun/SuperPyViewer',
    download_url     = 'https://github.com/RohJiHyun/SuperPyViewer',
    install_requires = [ ],
    packages         = find_packages(exclude = ['test*']),
    keywords         = ['viewer', '3d object'],
    python_requires  = '>=3',
    package_data     =  {
     },
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)