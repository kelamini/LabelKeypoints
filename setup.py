import distutils.spawn
import os
import re
import shlex
import subprocess
import sys

from setuptools import find_packages
from setuptools import setup


def get_version():
    filename = "labelkeys/__init__.py"
    with open(filename, "r", encoding="utf-8") as f:
        match = re.search(
            r"""^__version__ = ['"]([^'"]*)['"]""", f.read(), re.M
        )
    if not match:
        raise RuntimeError("{} doesn't contain __version__".format(filename))
    version = match.groups()[0]
    return version


def get_install_requires():
    install_requires = [
        "imgviz>=0.11",
        "matplotlib<3.3",  # for PyInstaller
        "opencv_python==4.2.0.34",
        "natsort>=7.1.0",
        "numpy==1.21.5",
        "Pillow>=2.8",
        "PyYAML",
        "qtpy==2.3.0",
        "termcolor",
    ]

    # Find python binding for qt with priority:
    # PyQt5 -> PySide2
    # and PyQt5 is automatically installed on Python3.
    QT_BINDING = None

    try:
        import PyQt5  # NOQA

        QT_BINDING = "pyqt5"
    except ImportError:
        pass

    if QT_BINDING is None:
        try:
            import PySide2  # NOQA

            QT_BINDING = "pyside2"
        except ImportError:
            pass

    if QT_BINDING is None:
        # PyQt5 can be installed via pip for Python3
        # 5.15.3, 5.15.4 won't work with PyInstaller
        install_requires.append("PyQt5!=5.15.3,!=5.15.4")
        QT_BINDING = "pyqt5"

    del QT_BINDING

    if os.name == "nt":  # Windows
        install_requires.append("colorama")

    return install_requires


def get_long_description():
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
    try:
        # when this package is being released
        import github2pypi

        return github2pypi.replace_url(
            slug="kelamini/LabelKeypoints", content=long_description, branch="main"
        )
    except ImportError:
        # when this package is being installed
        return long_description


def main():
    version = get_version()
    if sys.argv[1] == "release":
        try:
            import github2pypi  # NOQA
        except ImportError:
            print(
                "Please install github2pypi\n\n\tpip install github2pypi\n",
                file=sys.stderr,
            )
            sys.exit(1)
        if not distutils.spawn.find_executable("twine"):
            print(
                "Please install twine:\n\n\tpip install twine\n",
                file=sys.stderr,
            )
            sys.exit(1)
        commands = [
            "git push origin main",
            "git tag v{:s}".format(version),
            "git push origin --tags",
            "python setup.py sdist",
            "twine upload dist/labelkeys-{:s}.tar.gz".format(version),
        ]
        for cmd in commands:
            print("+ {:s}".format(cmd))
            subprocess.check_call(shlex.split(cmd))
        sys.exit(0)

    setup(
        name="labelkeys",
        version=version,
        packages=find_packages(),
        description="Image Polygonal Annotation with Python",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        author="kelamini",
        author_email="www.kelamini_0216@163.com",
        url="https://github.com/kelamini/LabelKeypoints.git",
        install_requires=get_install_requires(),
        license="GPLv3",
        keywords="Image Annotation, Machine Learning",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3 :: Only",
        ],
        package_data={"labelkeys": ["icons/*"], "labelkeys": ["configs/*"]},
        entry_points={
            "console_scripts": [
                "labelkeys=labelkeys.main:main",
            ],
        },
    )


if __name__ == "__main__":
    main()
