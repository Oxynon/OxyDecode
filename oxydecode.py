#!/usr/bin/env python3

#
# output and input are by default treated as a string.
# specify --byte-in to interpret the input as bytes
# specify --byte-out to convert the output to bytes
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

class View:

	def __init__(self):
		self.type = "view"
		self.Text = self.Text()
		self.Bytes = self.Bytes()

	class Text:
		def __init__(self):
			self.parser = ""
			self.help = ("prints the analyzed string"
						"\nafter a module has been used."
						"\nno additional argument required"+SPACER)
		def run(self):
			if args.show_prefix:
				if MUTA_STRING_TYPE == "string":
					print("p> "+MUTA_STRING)
				elif MUTA_STRING_TYPE == "binary":
					print("p0b> "+MUTA_STRING)
				elif MUTA_STRING_TYPE == "octal":
					print("p0o> "+MUTA_STRING)
				elif MUTA_STRING_TYPE == "decimal":
					print("p0d> "+MUTA_STRING)
				elif MUTA_STRING_TYPE == "hexadecimal":
					print("p0x> "+MUTA_STRING)
			else:
				print("p> "+MUTA_STRING)

	class Bytes:
		
		def __init__(self):
			self.parser = ""

			# runcount variable to iterate through args.b
			self.runcount = 0

			# check_ok to see if the input check was already run
			self.check_ok = False

			# multi_arg to see if -b was supplied multiple times
			self.multi_arg = False

			self.print_str = ""

			self.format_choices = ["hex", "bin"]
			self.groupby_choices = ["0", "hB", "B", "2B", "4B"]

			self.help = ("prints the analyzed string"
						"\nbut interprets them as ASCII bytes"
						"\n\nthis modules requires two additional"
						"\narguments. format & groupby"
						"\n\nformat output must be one of these:"
						"\nhex -> output hexadecimal"
						"\nbin -> output binary"
						"\n\ngroupby dictates how to"
						"\ngroup the bytes. choices are:"
						"\n0 -> no groupings"
						"\nhB -> half Byte groupings"
						"\nB -> Byte groupings"
						"\n2B -> two Byte groupings"
						"\n4B -> four Byte groupings"
						"\n\nthis module does not change"
						"\nthe currently worked-on string"
						"\nin the supplied chain"+SPACER)

		def run(self):
			
			if not self.check_ok:
				
				# check if multiple -b options have been supplied
				if any(isinstance(i, list) for i in args.b):
					self.multi_arg = True
				
					# check format & groupby value
					for parameters in args.b:
						if parameters[0] not in self.format_choices:
							parser.error("{} is not a valid format".format(parameters[0]))
						if parameters[1] not in self.groupby_choices:
							parser.error("{} is not a valid groupby option".format(parameters[1]))

				self.check_ok = True

			# check if multiple -b options have been supplied
			if self.multi_arg:
				form, groupby = args.b[self.runcount]
				self.runcount += 1
			else:
				form, groupby = args.b

			# check format & groupby value
			if form not in self.format_choices:
				parser.error("{} is not a valid format".format(form))
			if groupby not in self.groupby_choices:
				parser.error("{} is not a valid groupby option".format(groupby))

			# apply format
			if form == "hex":
				self.print_str = "".join(hex(ord(c))[2:] for c in MUTA_STRING)
				if groupby == "hB":
					self.print_str = " ".join(list(self.print_str))
				elif groupby == "B":
					self.print_str = " ".join([self.print_str[i:i+2] for i in range(0, len(self.print_str), 2)])
				elif groupby == "2B":
					self.print_str = " ".join([self.print_str[i:i+4] for i in range(0, len(self.print_str), 4)])
				elif groupby == "4B":
					self.print_str = " ".join([self.print_str[i:i+8] for i in range(0, len(self.print_str), 8)])

			elif form == "bin":
				self.print_str = "".join(bin(ord(c))[2:] for c in MUTA_STRING)
				if groupby == "hB":
					self.print_str = " ".join([self.print_str[i:i+4] for i in range(0, len(self.print_str), 4)])
				elif groupby == "B":
					self.print_str = " ".join([self.print_str[i:i+8] for i in range(0, len(self.print_str), 8)])
				elif groupby == "2B":
					self.print_str = " ".join([self.print_str[i:i+16] for i in range(0, len(self.print_str), 16)])
				elif groupby == "4B":
					self.print_str = " ".join([self.print_str[i:i+32] for i in range(0, len(self.print_str), 32)])

			print("b> "+self.print_str)

			return 0

class Transform:

	def __init__(self):
		self.type = "transform"
		self.Modules = ["replace", "reverse", "changecase", "numeral", "bitwise"]
		self.Replace = self.Replace()
		self.Reverse = self.Reverse()
		self.ChangeCase = self.ChangeCase()
		self.Numeral = self.Numeral()
		self.Bitwise = self.Bitwise()

	class Replace:
		
		def __init__(self):
			self.help = ("find a substring and"
						"\nreplace it with something"
						"\n\ntwo arguments required:"
						"\nfind -> the substring to find"
						"\nreplace -> string to replace with"+SPACER)

			self.runcount = 0
			self.check_ok = False
			self.multi_arg = False

		def run(self):
			global MUTA_STRING

			if not self.check_ok:
				if any(isinstance(i, list) for i in args.rp):
					self.multi_arg = True
					self.check_ok = True

			# check if multiple -rp options have been supplied
			if self.multi_arg:
				find, replace = args.rp[self.runcount]
				self.runcount += 1
			else:
				find, replace = args.rp

			if find not in MUTA_STRING:
				print("Error - '{}' not found in '{}'".format(find, MUTA_STRING))
				if args.verbose:
					print("rp failed // find:{} // replace:{}\nold string: {}".format(find, replace, MUTA_STRING))
				return 1
			else:
				# the actual magic
				MUTA_STRING = MUTA_STRING.replace(find, replace)
				if args.verbose:
					print("rp successful // find:{} // replace:{}\nNew string: {}".format(find, replace, MUTA_STRING))
				return 0

	class Reverse:
		# reversing a file could be a future feature
		# for now it only reverses strings
		def __init__(self):
			self.help = "reverses the currently used string"+SPACER
			#self.check_ok = False
			#self.multi_arg = False

		def run(self):
			global MUTA_STRING

			old_string = MUTA_STRING

			MUTA_STRING = MUTA_STRING[::-1]

			if args.verbose:
				print("rv> old string: {}\nrv> new string: {}".format(old_string, MUTA_STRING))

	class ChangeCase:
		def __init__(self):
			self.help = ("changes the case of the current string"
						"\n\nrequired argument:"
						"\nlower, l -> make string lower case"
						"\nupper, u -> make string upper case"
						"\ncapitalize, c -> capitalize a string"
						"\nalternating, a -> alternate case (lower, upper)"
						"\ninverse, i -> invert case on string"+SPACER)
			self.choices=["lower", "upper", "capitalize", "alternating", "inverse", "l", "u", "c", "a", "i"]
			self.check_ok = False
			self.multi_arg = False
			self.runcount = 0

		def run(self):
			global MUTA_STRING

			if not self.check_ok:
				if any(isinstance(i, list) for i in args.case):
					self.multi_arg = True

			# check if multiple -cc options have been supplied
			if self.multi_arg:
				option = args.case[self.runcount]
				self.runcount += 1
			else:
				option = args.case[0]

			if option in ["lower", "l"]:
				MUTA_STRING = MUTA_STRING.lower()
			elif option in ["upper", "u"]:
				MUTA_STRING = MUTA_STRING.upper()
			elif option in ["capitalize", "c"]:
				MUTA_STRING = MUTA_STRING.capitalize()
			elif option in ["alternating", "a"]:
				MUTA_STRING = list(MUTA_STRING)
				i = 0
				while i < len(MUTA_STRING):
					if i%2 == 0:
						MUTA_STRING[i] = MUTA_STRING[i].lower()
					else:
						MUTA_STRING[i] = MUTA_STRING[i].upper()
					i+=1
				MUTA_STRING = "".join(MUTA_STRING)

			elif option in ["inverse", "i"]:
				MUTA_STRING = MUTA_STRING.swapcase()


	class Numeral:
		def __init__(self):
			self.help = ""
			self.check_ok = False
			self.multi_arg = False
			self.choices = ["bin", "oct", "dec", "hex", "roman"]
			self.readtype = ""
			self.runcount = 0
			self.hexchars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

		def run(self):
			global MUTA_STRING

			def mutate_string(mstring, option, base):
				global MUTA_STRING_TYPE

				if option == "bin":
					MUTA_STRING_TYPE = "binary"
					mstring = str(bin(int(mstring, base)))[2:]
				if option == "oct":
					MUTA_STRING_TYPE = "octal"
					mstring = str(oct(int(mstring, base)))[2:]
				elif option == "dec":
					MUTA_STRING_TYPE = "decimal"
					mstring = str(int(mstring, base))
				elif option == "hex":
					MUTA_STRING_TYPE = "hexadecimal"
					mstring = str(hex(int(mstring, base)))[2:]
				elif option == "roman":
					MUTA_STRING_TYPE = "roman"
					########## TO BE IMPLEMENTED
					parser.error("conversion to roman numerals is not yet implemented")

				return mstring

			# check if args are nested
			if not self.check_ok:
				if any(isinstance(i, list) for i in args.n):
					self.multi_arg = True

			# check if multiple -n options have been supplied
			if self.multi_arg:
				read, convertto = args.n[self.runcount]
				self.runcount += 1
			else:
				read, convertto = args.numeral

			# check if args are proper
			if read not in self.choices:
				parser.error("{} is not a valid option for 'read'".format(read))
			if convertto not in self.choices:
				parser.error("{} is not a valid option for 'convertto'".format(convertto))
			if read == convertto:
				return 0

			# check if args are the supplied type
			#args.read
			#args.convertto
			if read == "bin":
				
				for char in MUTA_STRING:
					if char not in ["0", "1"]:
						parser.error("string contained {}, which is not binary".format(char))

				MUTA_STRING = mutate_string(MUTA_STRING, convertto, 2)

			elif read == "oct":
				for char in MUTA_STRING:
					if char not in [str(x) for x in range(0,8)]:
						parser.error("string contained {}, which is not octal".format(char))

				MUTA_STRING = mutate_string(MUTA_STRING, convertto, 8)

			elif read == "dec":
				for char in MUTA_STRING:
					if char not in [str(x) for x in range(0,10)]:
						parser.error("string contained {}, which is not decimal".format(char))

				MUTA_STRING = mutate_string(MUTA_STRING, convertto, 10)

			elif read == "hex":
				for char in MUTA_STRING:
					if char.lower() not in self.hexchars:
						parser.error("string contained {}, which is not hexadecimal".format(char))

				MUTA_STRING = mutate_string(MUTA_STRING, convertto, 16)

			elif read == "roman":
				for char in MUTA_STRING:
					if char.lower() not in ["i", "v", "x", "l", "c", "d", "m"]:
						parser.error("string contained {}, which is not a roman numeral".format(char))


	class Bitwise:
		def __init__(self):
			self.help = ""
			self.check_ok = False
			self.multi_arg = False

class Alphabets:
	
	def __init__(self):
		self.type = "alphabet"

class Ciphers:
	
	def __init__(self):
		self.type = "cipher"

class Encoding:
	
	def __init__(self):
		self.type = "encoding"

class Modern:
	
	def __init__(self):
		self.type = "modern"

def wizardSetup():
	# sets the modules and output
	# via an interactive wizard
	# instead of via arguments
	None

def mainLoop():

	if args.wizard:
		wizardSetup()

	module_error = 0

	for arg in arg_chain:
		if arg == "-p":
			module_error = cView.Text.run()
		elif arg == "-b":
			module_error = cView.Bytes.run()
		elif arg == "-rp":
			module_error = cTransform.Replace.run()
		elif arg == "-rv":
			module_error = cTransform.Reverse.run()
		elif arg == "-cc":
			module_error = cTransform.ChangeCase.run()
		elif arg == "-n":
			module_error = cTransform.Numeral.run()

		if module_error:
			break

if __name__ == "__main__":

	SPACER = "\n "

	def get_chain(args):
		chain = []
		for arg in args:
			if "-" in arg:
				chain.append(arg)
		return chain


	cView = View()
	cTransform = Transform()

	modules = ["view", "transform", "alphabet", "cipher", "encode", "modern"]

	parser = argparse.ArgumentParser(description="A tool for simple Cryptoanalysis", formatter_class=RawTextHelpFormatter)
	parser.add_argument("input", help="your input string", action="store")
	parser.add_argument("-v", "--verbose", help="show more verbose output", action="store_true")
	parser.add_argument("--wizard", help="ignore śupplied arguments and\nuse the wizard instead"+SPACER, action="store_true")

	parser.add_argument("-p", help=cView.Text.help, action="store_true")

	parser.add_argument("-b", help=cView.Bytes.help, nargs=2, metavar=("format", "groupby"), action="append")

	parser.add_argument("-rp", help=cTransform.Replace.help, nargs=2, metavar=("find", "replace"), action="append")

	parser.add_argument("-rv", help=cTransform.Reverse.help, action="store_true")

	parser.add_argument("-cc", help=cTransform.ChangeCase.help, choices=cTransform.ChangeCase.choices, dest="case", action="append")

	parser.add_argument("-n", help=cTransform.Numeral.help, nargs=2, metavar=("read", "convertto"), action="append")

	parser.add_argument("-bw", help=cTransform.Bitwise.help, nargs=2, metavar=("operation", "operand_b"), action="append")

	parser.add_argument("--show-prefix", help="show prefixes on all numbers except decimal", action="store_true", dest="show_prefix")
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

	args = parser.parse_args()
	MUTA_STRING = args.input
	MUTA_STRING_TYPE = "string"
	arg_chain = get_chain(sys.argv)
	print(args)
	print(sys.argv)
	print(get_chain(sys.argv))
	mainLoop()
