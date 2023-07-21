#!/usr/bin/env python3
"""
Generates LaTeX, Markdown, and HTML copies of my résumé.

More information is available in the README file.

"""
import argparse
import os
import sys

from contexts import CONTEXTS
from resume_generator import environment_setup, ResumeGenerator

os.environ["PATH"] += ":/Library/TeX/texbin"


class DefaultListAction(argparse.Action):
    """
    Allow a default list with argparse.

    References
    ----------
    .. [#] Stack Overflow, "python argparse - optional append argument with choices"
    http://stackoverflow.com/a/8527629

    """
    CHOICES = CONTEXTS.keys()

    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            for value in values:
                if value not in self.CHOICES:
                    message = ("invalid choice: {0!r} (choose from {1})"
                               .format(value,
                                       ", ".join([repr(action)
                                                  for action in self.CHOICES])))

                    raise argparse.ArgumentError(self, message)
            setattr(namespace, self.dest, values)


def main():
    """
    Main hook for script.

    """
    parser = argparse.ArgumentParser(
        description="Generate resumes and cover letters."
    )
    parser.add_argument("contexts", metavar="contexts", nargs="*",
                        action=DefaultListAction,
                        help="the contexts to generate (default is LaTeX)",
                        default=["latex"])
    parser.add_argument("-l", "--no-letters", action="store_false",
                        help="do not generate cover letters when running LaTeX")

    args = parser.parse_args()

    environment_setup()
    ResumeGenerator().run(context_names=args.contexts,
                          no_letters=args.no_letters)


if __name__ == "__main__":
    sys.exit(main())
