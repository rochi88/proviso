from setuptools import setup, find_packages
import codecs
import os


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('README.md') as readme_file:
    README = readme_file.read()

with open('CHANGELOG.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='proviso',
    version=read('proviso/VERSION.txt'),
    description='A utility for Stock price prediction with keras',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Raisul Islam',
    author_email='raisul.exe@gmail.com',
    keywords=['deep learning','ai'],
    url='https://github.com/rochi88/proviso',
    download_url='https://github.com/rochi88/proviso/archive/master.zip'
)

install_requires = [
		'absl-py>=0.6.1'
		'astor>=0.7.1',
		'certifi>=2018.8.24',
		'chardet>=3.0.4',
		'cycler>=0.10.0',
		'gast>=0.2.0',
		'grpcio>=1.17.1',
		'h5py>=2.9.0',
		'idna>=2.8',
		'Keras>=2.2.4',
		'Keras-Applications>=1.0.6',
		'Keras-Preprocessing>=1.0.5',
		'kiwisolver>=1.0.1',
		'Markdown>=3.0.1',
		'matplotlib>=3.0.2',
		'numpy>=1.15.4',
		'pandas>=0.23.4',
		'protobuf>=3.6.1',
		'pyparsing>=2.3.0',
		'python-dateutil>=2.7.5',
		'pytz>=2018.7',
		'PyYAML>=3.13',
		'requests>=2.21.0',
		'scikit-learn>=0.20.2',
		'scipy>=1.2.0',
		'six>=1.12.0',
		'tensorboard>=1.12.1',
		'tensorflow>=1.12.2',
		'termcolor>=1.1.0',
		'urllib3>=1.24.1',
		'Werkzeug>=0.14.1',
		'wincertstore>=0.2'
]

classifiers=[
        'Development Status :: 1 - dev',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, classifiers=classifiers)