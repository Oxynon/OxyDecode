#!/usr/bin/env python3

#
# output and input are by default treated as a string.
# 
# modules can be chained and will be done in order
# from left to right.
# 
#
# oxydecode.py <input> [--module <MODULE>]
#
#

import argparse
from argparse import RawTextHelpFormatter
import sys
import binascii
from modules import Universals, View, Transform, Alphabets, Ciphers, Encoding, Modern

def wizardSetup():
	# sets the modules and output
	# via an interactive wizard
	# instead of via arguments
	None

def mainLoop():

	#print("test {}".format(arg_chain))

	if Universals.ARGS.wizard:
		wizardSetup()

	module_error = 0

	for arg in arg_chain:
		if arg == "-p":
			module_error = View.Text.run()
		elif arg == "-a":
			module_error = View.Ascii.run()
		elif arg == "-b":
			module_error = View.Bytes.run()
		elif arg == "-rp":
			module_error = Transform.Replace.run()
		elif arg == "-rv":
			module_error = Transform.Reverse.run()
		elif arg == "-cc":
			module_error = Transform.ChangeCase.run()
		elif arg == "-n":
			module_error = Transform.Numeral.run()
		elif arg == "-bw":
			modul_error = Transform.Bitwise.run()

		if module_error:
			break

if __name__ == "__main__":

	Universals.init()

	def get_chain(args):
		chain = []
		for arg in args:
			if "-" in arg:
				chain.append(arg)
		return chain


	cView = View.init()
	#print(Universals.SPACER)
	cTransform = Transform.init()

	modules = ["view", "transform", "alphabet", "cipher", "encode", "modern"]

	parser = argparse.ArgumentParser(description="A tool for simple Cryptoanalysis", formatter_class=RawTextHelpFormatter)
	parser.add_argument("input", help="your input string", action="store")
	parser.add_argument("-v", "--verbose", help="show more verbose output", action="store_true")
	parser.add_argument("--wizard", help="ignore supplied arguments and\nuse the wizard instead"+Universals.SPACER, action="store_true")

	parser.add_argument("-p", help=View.Text.help, action="store_true")

	parser.add_argument("-a", help=View.Ascii.help, action="store_true")

	parser.add_argument("-b", help=View.Bytes.help, nargs=2, metavar=("format", "groupby"), action="append")

	parser.add_argument("-rp", help=Transform.Replace.help, nargs=2, metavar=("find", "replace"), action="append")

	parser.add_argument("-rv", help=Transform.Reverse.help, action="store_true")

	parser.add_argument("-cc", help=Transform.ChangeCase.help, choices=Transform.ChangeCase.choices, dest="case", action="append")

	#parser.add_argument("-n", help=cTransform.Numeral.help, nargs=2, metavar=("read", "convertto"), action="append")
	parser.add_argument("-n", help=Transform.Numeral.help, nargs=1, metavar="type", action="append")

	parser.add_argument("-bw", help=Transform.Bitwise.help, nargs=1, metavar="operation", action="append")

	parser.add_argument("--show-prefix", help="show prefixes on all numbers except decimal", action="store_true", dest="show_prefix")

	parser.add_argument("--read-as-bin", help="read initial input as binary", action="store_true", dest="init_as_bin")
	parser.add_argument("--read-as-oct", help="read initial input as octal", action="store_true", dest="init_as_oct")
	parser.add_argument("--read-as-dec", help="read initial input as decimal", action="store_true", dest="init_as_dec")
	parser.add_argument("--read-as-hex", help="read initial input as hexadecimal", action="store_true", dest="init_as_hex")
	parser.add_argument("--read-as-roman", help="read initial input as roman numerals", action="store_true", dest="init_as_roman")

	#parser.add_argument("--byte-in", help="treat input as bytes", action="store_true")
	#parser.add_argument("--byte-out", help="treat output as bytes", action="store_true")
	#subparsers = parser.add_subparsers(help="specify a module\nuse '<module> -h' to get more info")

	#mText.parser = subparsers.add_parser("text", help=mText.help, formatter_class=RawTextHelpFormatter)
	#mText.parser.add_argument("view_true", help="True if 'view' has been supplied", action="store_true")
	
	#mBytes.parser = subparsers.add_parser("bytes", help=mBytes.help, formatter_class=RawTextHelpFormatter)
	#mBytes.parser.add_argument("format", help=mBytes.help_format, choices=mBytes.format_choices, action="store")
	#mBytes.parser.add_argument("groupby", help=mBytes.help_groupby, choices=mBytes.groupby_choices, action="store")

	#parser_transform = subparsers.add_parser("transform", help="", formatter_class=RawTextHelpFormatter)
	#parser_transform.add_argument("module", choices=cTransform.modules, action="store")

	Universals.ARGS = parser.parse_args()
	Universals.PARSER = parser

	Universals.META_STRING = Universals.ARGS.input
	if Universals.ARGS.init_as_bin:
		Universals.META_STRING_TYPE = "binary"
	elif Universals.ARGS.init_as_oct:
		Universals.META_STRING_TYPE = "octal"
	elif Universals.ARGS.init_as_dec:
		Universals.META_STRING_TYPE = "decimal"
	elif Universals.ARGS.init_as_hex:
		Universals.META_STRING_TYPE = "hexadecimal"
	elif Universals.ARGS.init_as_roman:
		Universals.META_STRING_TYPE = "roman"
	else:
		Universals.META_STRING_TYPE = "string"
	arg_chain = get_chain(sys.argv)
	#print(Universals.ARGS)
	#print(sys.argv)
	#print(get_chain(sys.argv))
	mainLoop()
