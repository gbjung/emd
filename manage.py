#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ


def main():
    env = environ.Env(DEBUG=(bool, False),)
    environ.Env.read_env()

    if env('ENV_SETTING') == 'dev':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emd.settings.dev")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emd.settings.production")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
