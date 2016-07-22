################################################################################
#
# File Name: launch_server.py
# Application: scripts
# Purpose: Python script to start a server
#
# Author: Xavier SCHMITT
#         xavier.schmitt@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

import sys, argparse

def usage():
    print "  ---------------------------------------------------------------------"
    print " | launch_server [options]                                             |"
    print " |                                                                     |"
    print " |       Options:                                                      |"
    print " |                                                                     |"
    print " |  -p  | --dir   : path to the django project folder (mandatory)      |"
    print " |  -d  | --dport : django server port (8000 if not specified)         |"
    print " |  -c  | --mconf : path to mongoDB configuration file (mandatory)     |"
    print " |  -m  | --mport : mongoDB port (27017 if not specified)              |"
    print " |  -y  | --py    : path to python (not mandatory if path configured)  |"
    print " |  -l  | --ce    : path to celery (not mandatory if path configured)  |"
    print " |  -g  | --mo    : path to mongoDB (not mandatory if path configured) |"
    print " |  -h  | --help  : help                                               |"
    print " |                                                                     |"
    print "  ---------------------------------------------------------------------"
    sys.exit()

def main(argv):
    parser = argparse.ArgumentParser(description="Curator Data Migration Tool")
    required_arguments = parser.add_argument_group("required arguments")

    # add required arguments
    required_arguments.add_argument('-p',
                                    '--dir',
                                    help='Path to the django project folder',
                                    nargs=1,
                                    required=True)
    required_arguments.add_argument('-c',
                                    '--mconf',
                                    help='Path to mongoDB configuration file',
                                    nargs=1,
                                    required=True)

    # add optional arguments
    parser.add_argument('-d',
                        '--dport',
                        help='Django server port (8000 if not specified)',
                        nargs=1)
    parser.add_argument('-m',
                        '--mport',
                        help='MongoDB port (27017 if not specified)',
                        nargs=1)
    parser.add_argument('-y',
                        '--py',
                        help='Path to Python (not mandatory if path configured)',
                        nargs=1)
    parser.add_argument('-l',
                        '--ce',
                        help='Path to Celery (not mandatory if path configured)',
                        nargs=1)
    parser.add_argument('-g',
                        '--mo',
                        help='Path to MongoDB (not mandatory if path configured)',
                        nargs=1)
    parser.add_argument('-h',
                        '--help',
                        help='Help')


    # parse arguments
    args = parser.parse_args()

    # get required arguments
    dir = args.dir[0]
    mconf = args.mconf[0]

    # get optional arguments
    if args.dport:
        dport = args.dport[0]
    else:
        dport = ''

    if args.mport:
        mport = args.mport[0]
    else:
        mport = ''

    if args.py:
        py = args.py[0]
    else:
        py = ''

    if args.ce:
        ce = args.ce[0]
    else:
        ce = ''

    if args.mo:
        mo = args.mo[0]
    else:
        mo = ''

    if args.help:
        usage()