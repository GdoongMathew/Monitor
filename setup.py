import os
import sys
import shutil
import subprocess

from setuptools import find_packages, setup, Command
from distutils.spawn import find_executable
from distutils.command.clean import clean as _clean
from distutils.command.build_py import build_py as _build_py

NAME = "monitor"
DESCRIPTION = "Monitor which reads hardware information."
URL = "https://github.com/GdoongMathew/Monitor"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.1"

try:
    with open('requirements.txt', encoding='utf-8') as f:
        REQUIRED = f.read().split('\n')

except:
    REQUIRED = []

# Find the Protocol Compiler.
if 'PROTOC' in os.environ and os.path.exists(os.environ['PROTOC']):
    protoc = os.environ['PROTOC']
elif os.path.exists("../src/protoc"):
    protoc = "../src/protoc"
elif os.path.exists("../src/protoc.exe"):
    protoc = "../src/protoc.exe"
elif os.path.exists("../vsprojects/Debug/protoc.exe"):
    protoc = "../vsprojects/Debug/protoc.exe"
elif os.path.exists("../vsprojects/Release/protoc.exe"):
    protoc = "../vsprojects/Release/protoc.exe"
else:
    protoc = find_executable("protoc")


def generate_proto(source, require=True):
    """Generates a _pb2.py from the given .proto file.
  Does nothing if the output already exists and is newer than the input.
  Args:
      source: the .proto file path.
      require: if True, exit immediately when a path is not found.
  """

    if not require and not os.path.exists(source):
        return

    output = source.replace('.proto', '_pb2.py').replace('../src/', '')

    if (not os.path.exists(output) or
            (os.path.exists(source) and
             os.path.getmtime(source) > os.path.getmtime(output))):
        print('Generating %s...' % output)

        if not os.path.exists(source):
            sys.stderr.write("Can't find required file: %s\n" % source)
            sys.exit(-1)

        if protoc is None:
            sys.stderr.write(
                'protoc is not installed nor found in ../src.  Please compile it '
                'or install the binary package.\n')
            sys.exit(-1)

        protoc_command = [protoc, '-I../src', '-I.', '--python_out=.', source]
        if subprocess.call(protoc_command) != 0:
            sys.exit(-1)


class clean_cmd(_clean):
    """Custom clean command for building the protobuf extension."""

    def run(self):
        # Delete generated files in the code tree.
        for (dirpath, unused_dirnames, filenames) in os.walk('.'):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if (filepath.endswith('_pb2.py') or filepath.endswith('.pyc') or
                        filepath.endswith('.so') or filepath.endswith('.o')):
                    os.remove(filepath)
        # _clean is an old-style class, so super() doesn't work.
        _clean.run(self)


# List of all .proto files
proto_src = [
    'monitor/reader/proto/device.proto',
]

class build_py(_build_py):
    def run(self):
        for f in proto_src:
            generate_proto(f)
        _build_py.run(self)


class clean(_clean):
    def run(self):
        # Delete generated files in the code tree.
        for (dirpath, dirnames, filenames) in os.walk("."):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if filepath.endswith("_pb2.py"):
                    os.remove(filepath)
        # _clean is an old-style class, so super() doesn't work.
        _clean.run(self)


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    cmdclass={'clean': clean, 'build_py': build_py}
)
