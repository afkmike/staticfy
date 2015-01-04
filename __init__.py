__author__ = 'nubspnkr'
from pkgutil import extend_path

__all__ = ["file_io", "process_html", "process_py"]
    # This declares what modules will be imported with import * command

__path__ = extend_path(__path__, __name__)
    # This will add to the package's __path__ all subdirectories of directories on sys.path named after the package.