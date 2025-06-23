import glob
import py_compile


def test_handlers_compile():
    for path in glob.glob('handlers/*.py'):
        py_compile.compile(path, doraise=True)
