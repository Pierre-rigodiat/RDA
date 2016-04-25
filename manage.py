#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if '-t' in sys.argv or 'test' in sys.argv:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mgi.settings_test")
        if '-t' in sys.argv:
            sys.argv = sys.argv[:-1]
    #elif sys.argv[2] == '-p':
    #    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mgi.settings_production")
    #    sys.argv = sys.argv[:-1]
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mgi.settings")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
