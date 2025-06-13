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

install_reqs = ['anyio', 'anytree', 'argon2-cffi', 'argon2-cffi-bindings', 'arrow', 'asttokens', 'async-lru', 'attrs', 'babel', 'beautifulsoup4', 'bleach', 'bokeh', 'certifi', 'cffi', 'charset-normalizer', 'colorama', 'comm', 'configparser', 'contourpy', 'cycler', 'debugpy', 'decorator', 'defusedxml', 'executing', 'fastjsonschema', 'FlowIO', 'FlowKit', 'FlowUtils', 'fonttools', 'fqdn', 'h11', 'httpcore', 'httpx', 'idna', 'iniconfig', 'ipykernel', 'ipython', 'ipython_pygments_lexers', 'ipywidgets', 'isoduration', 'jedi', 'Jinja2', 'joblib', 'json5', 'jsonpointer', 'jsonschema', 'jsonschema-specifications', 'jupyter', 'jupyter-console', 'jupyter-events', 'jupyter-lsp', 'jupyter_client', 'jupyter_core', 'jupyter_server', 'jupyter_server_terminals', 'jupyterlab', 'jupyterlab_pygments', 'jupyterlab_server', 'jupyterlab_widgets', 'kiwisolver', 'lxml', 'MarkupSafe', 'matplotlib', 'matplotlib-inline', 'mistune', 'nbclient', 'nbconvert', 'nbformat', 'nest-asyncio', 'networkx', 'notebook', 'notebook_shim', 'numpy', 'overrides', 'packaging', 'pandas', 'pandocfilters', 'parso', 'pillow', 'platformdirs', 'pluggy', 'prometheus_client', 'prompt_toolkit', 'psutil', 'psycopg2', 'pure_eval', 'pycparser', 'Pygments', 'PyMySQL', 'pyodbc', 'pyparsing', 'pytest', 'python-dateutil', 'python-hostlist', 'python-json-logger', 'python-swiftclient', 'pytz', 'pywin32', 'pywinpty', 'PyYAML', 'pyzmq', 'referencing', 'requests', 'rfc3339-validator', 'rfc3986-validator', 'rpds-py', 'sci', 'scikit-learn', 'scipy', 'seaborn', 'Send2Trash', 'setuptools', 'six', 'sniffio', 'soupsieve', 'stack-data', 'tabulate', 'terminado', 'threadpoolctl', 'tinycss2', 'tornado', 'traitlets', 'types-python-dateutil', 'typing_extensions', 'tzdata', 'uri-template', 'urllib3', 'wcwidth', 'webcolors', 'webencodings', 'websocket-client', 'widgetsnbextension', 'xyzservices']


# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="FACS_Visualization",
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


