============
Contributing
============

Contributions are welcome and greatly appreciated! Every little bit helps, and credit will always be given.


Bug reports
===========

When `reporting a bug <https://github.com/dmpop/sonnenhut/issues>`_ please include:

    * Your operating system name and version.
    * Any details about your local setup that might be helpful in troubleshooting.
    * Detailed steps to reproduce the bug.


Feature requests and feedback
=============================

The best way to send feedback is to file an issue at https://github.com/dmpop/sonnenhut/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that code contributions are welcome :)


Development
===========

To set up `sonnenhut` for local development:

1. `Fork sonnenhut <https://github.com/openSUSE/docstats#fork-destination-box>`_.
2. Clone your fork locally::

    git clone git@github.com:your_name_here/sonnenhut.git

3. Create a branch for local development::

    git checkout -b NAME-OF-YOUR-BUGFIX-OR-FEATURE

   Now you can make your changes locally.

4. When you're done making changes, run all the checks with the commands::

    pyvenv .env
    source .env/bin/activate
    pip install -r devel_requirements.txt
    py.test -v

5. Commit your changes and push your branch to GitHub::

    git add .
    git commit -m "Your detailed description of your changes."
    git push origin NAME-OF-YOUR-BUGFIX-OR-FEATURE

6. Submit a pull request through the GitHub website.


Pull Request Guidelines
-----------------------

If you'd like to request  code review or feedback while you're working on the
code, make the pull request.

For merging, please do the following:

1. Update documentation when there's new API, functionality etc.
2. Add a note to ``CHANGELOG.rst`` about the changes.
3. Add yourself to ``AUTHORS.rst``.

