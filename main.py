from lmd.main import *
from lmd.util.source import Source

arg_parser = args.default_arg_parser()
src = arg_parser.parse_args().src
srcs = [Source.from_file(src_file) for src_file in src]
pipeline.interpret_sources(srcs)
