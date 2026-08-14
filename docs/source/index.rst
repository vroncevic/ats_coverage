Generate code coverage and update README.md
---------------------------------------------

**ats_coverage** is toolset for generation of code coverage and update README.md.

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|ats_coverage python checker| |ats_coverage python package| |github issues| |documentation status| |github contributors|

.. |ats_coverage python checker| image:: https://github.com/vroncevic/ats_coverage/actions/workflows/ats_coverage_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/ats_coverage/actions/workflows/ats_coverage_python_checker.yml

.. |ats_coverage python package| image:: https://github.com/vroncevic/ats_coverage/actions/workflows/ats_coverage_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/ats_coverage/actions/workflows/ats_coverage_package.yml

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/ats_coverage.svg
   :target: https://github.com/vroncevic/ats_coverage/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/ats_coverage.svg
   :target: https://github.com/vroncevic/ats_coverage/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/ats_coverage/badge/?version=latest
   :target: https://ats-coverage.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

🚀 Installation
-----------------

|ats_coverage python3 build|

.. |ats_coverage python3 build| image:: https://github.com/vroncevic/ats_coverage/actions/workflows/ats_coverage_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/ats_coverage/actions/workflows/ats_coverage_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/ats_coverage/releases

To install **ats_coverage** type the following

.. code-block:: bash

    tar xvzf ats_coverage-x.y.z.tar.gz
    cd ats_coverage-x.y.z/
    # python3
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py 
    python3 -m pip install --upgrade setuptools
    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade build
    pip3 install -r requirements.txt
    python3 -m build --no-isolation --wheel
    pip3 install ./dist/ats_coverage-*-py3-none-any.whl
    rm -f get-pip.py
    chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/ats_coverage_run.py
    ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/ats_coverage_run.py /usr/local/bin/ats_coverage_run.py

You can use Docker to create image/container, or You can use pip to install

.. code-block:: bash

    # pyton3
    pip3 install ats_coverage

📦 Dependencies
-----------------

**ats_coverage** requires next modules and libraries

* `coverage - Code coverage measurement for Python <https://pypi.org/project/coverage/>`_
* `pathlib - Object-oriented filesystem paths <https://pypi.org/project/pathlib/>`_


📁 Tool structure
-------------------

**ats_coverage** is based on OOP.

Tool structure

.. code-block:: bash

    ats_coverage.py

     0 directories, 1 files

