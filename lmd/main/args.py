from argparse import *


def default_arg_parser():
    parser = ArgumentParser(description='LMD interpreter')
    parser.add_argument('src', metavar='SRC', type=str,
                        nargs='+', default=None)
    return parser
