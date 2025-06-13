from setuptools import setup, find_packages


VERSION = "0.0.1"
DESCRIPTION = "My first Python package"
LONG_DESCRIPTION = "My first Python package with a slightly longer description"


"""
config = ConfigParser(delimiters=["="])
config.read("configs.ini")
cfg = config["metadata"]


my_file = open("requirements.txt", 'r')
data = my_file.read()
my_file.close()
installrequirements = data.split("\n")

#follow code is to create list of all installed packages, but cannot use directly
import subprocess
import sys
req = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8').replace('\n', '==' ).split('==')[:-1]
def list_even(x):
    even = []
    for n in x:
        if not n % 2:
            even.append(n)
    return even
install_requirements = [req[x] for x in list_even(list(range(len(req))))]
"""

install_reqs = ['anytree', 'bokeh', 'certifi', 'charset-normalizer', 'configparser', 'contourpy', 'cycler', 'FlowIO', 'FlowKit', 'FlowUtils', 'fonttools', 'idna', 'Jinja2', 'joblib', 'kiwisolver', 'lxml', 'MarkupSafe', 'matplotlib', 'networkx', 'numpy', 'packaging', 'pandas', 'pillow', 'psutil', 'psycopg2', 'PyMySQL', 'pyodbc', 'pyparsing', 'python-dateutil', 'python-hostlist', 'python-swiftclient', 'pytz', 'PyYAML', 'requests', 'sci', 'scikit-learn', 'scipy', 'seaborn', 'setuptools', 'six', 'threadpoolctl', 'tornado', 'tzdata', 'urllib3', 'xyzservices']


# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="FACS_Visualization_Package",
        version=VERSION,
        author="Stijn Kneefel",
        author_email="stijn.kneefel@outlook.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=install_reqs, # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'FACS', 'Flow cytometry'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)


