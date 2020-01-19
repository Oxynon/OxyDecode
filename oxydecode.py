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

class View:

	def __init__(self):
		self.type = "view"
		self.Text = self.Text()
		self.Ascii = self.Ascii()
		self.Bytes = self.Bytes()

	class Text:
		def __init__(self):
			self.parser = ""
			self.help = ("prints the analyzed string"
						"\nafter a module has been used."
						"\nno additional argument required"+SPACER)
		def run(self):
			if args.show_prefix:
				if META_STRING_TYPE == "string":
					print("ps> "+META_STRING)
				elif META_STRING_TYPE == "binary":
					print("p0b> "+META_STRING)
				elif META_STRING_TYPE == "octal":
					print("p0o> "+META_STRING)
				elif META_STRING_TYPE == "decimal":
					print("p0d> "+META_STRING)
				elif META_STRING_TYPE == "hexadecimal":
					print("p0x> "+META_STRING)
			else:
				print("p> "+META_STRING)

	class Ascii:
		def __init__(self):
			self.parser = ""
			self.help = "converts binary or hex to ASCII"+SPACER
			self.working_string = ""

		def run(self):
			global META_STRING
			global META_STRING_TYPE

			self.working_string = META_STRING

			def from_bin(string):
				try:
					string = int(string, 2)
					string = string.to_bytes((string.bit_length() + 7) // 8, "big").decode("ascii")
				except UnicodeDecodeError as unicode_e:
					byte_e = str(unicode_e.object[-1:])[2:-1].replace("\\", "0") #wtf
					position_e = unicode_e.start
					parser.error("current binary value cannot be interpreted as ascii\nbyte {} at position {}".format(byte_e, position_e))

				return string

			def from_hex(string):
				try:
					string = bytes.fromhex(string).decode('ascii')
				except ValueError as value_e:
					position_e = value_e.args[0].split(" ")[-1:]
					parser.error("current hex value cannot be interpreted as ascii\nerror at position {}".format(position_e))
				except UnicodeDecodeError as unicode_e:
					byte_e = str(unicode_e.object[-1:])[2:-1].replace("\\", "0")
					position_e = unicode_e.start
					parser.error("current hex value cannot be interpreted as ascii\nbyte {} at position {}".format(byte_e, position_e))
				
				return string

			self.allowed_types = {"hexadecimal":from_hex, "binary":from_bin}

			if META_STRING_TYPE not in self.allowed_types.keys():
				parser.error("type '{}' not supported by -a option".format(META_STRING_TYPE))

			if " " in self.working_string:
				self.working_string = self.working_string.replace(" ", "")

			META_STRING = self.allowed_types[META_STRING_TYPE](self.working_string)
			META_STRING_TYPE = "string"

			if args.verbose:
				print("a> "+META_STRING)

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
						"\n"+SPACER)

		def run(self):

			global META_STRING
			global META_STRING_TYPE
			
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

			# reset print_str
			self.print_str = ""

			# apply format
			if form == "hex":
				if META_STRING_TYPE == "binary":
					self.print_str = hex(int(META_STRING.replace(" ", ""), 2))[2:]
				else:
					self.print_str = "".join(hex(ord(c))[2:] for c in META_STRING)
				META_STRING_TYPE = "hexadecimal"
				if groupby == "hB":
					self.print_str = " ".join(list(self.print_str))
				elif groupby == "B":
					self.print_str = " ".join([self.print_str[i:i+2] for i in range(0, len(self.print_str), 2)])
				elif groupby == "2B":
					self.print_str = " ".join([self.print_str[i:i+4] for i in range(0, len(self.print_str), 4)])
				elif groupby == "4B":
					self.print_str = " ".join([self.print_str[i:i+8] for i in range(0, len(self.print_str), 8)])

			elif form == "bin":
				if META_STRING_TYPE == "hexadecimal":
					self.print_str = bin(int(META_STRING.replace(" ", ""), 16))[2:]
				else:
					for c in META_STRING:
						tmpvar = str(bin(ord(c))[2:])
						if len(tmpvar) < 8:
							tmpvar = ("0"*(8-len(tmpvar)))+tmpvar 
						self.print_str += tmpvar

				META_STRING_TYPE = "binary"
				if groupby == "hB":
					self.print_str = " ".join([self.print_str[i:i+4] for i in range(0, len(self.print_str), 4)])
				elif groupby == "B":
					self.print_str = " ".join([self.print_str[i:i+8] for i in range(0, len(self.print_str), 8)])
				elif groupby == "2B":
					self.print_str = " ".join([self.print_str[i:i+16] for i in range(0, len(self.print_str), 16)])
				elif groupby == "4B":
					self.print_str = " ".join([self.print_str[i:i+32] for i in range(0, len(self.print_str), 32)])

			if args.verbose:
				print("b> "+self.print_str)

			META_STRING = self.print_str

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
			global META_STRING

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

			if find not in META_STRING:
				print("Error - '{}' not found in '{}'".format(find, META_STRING))
				if args.verbose:
					print("rp failed // find:{} // replace:{}\nold string: {}".format(find, replace, META_STRING))
				return 1
			else:
				# the actual magic
				META_STRING = META_STRING.replace(find, replace)
				if args.verbose:
					print("rp successful // find:{} // replace:{}\nNew string: {}".format(find, replace, META_STRING))
				return 0

	class Reverse:
		# reversing a file could be a future feature
		# for now it only reverses strings
		def __init__(self):
			self.help = "reverses the currently used string"+SPACER
			#self.check_ok = False
			#self.multi_arg = False

		def run(self):
			global META_STRING

			old_string = META_STRING

			META_STRING = META_STRING[::-1]

			if args.verbose:
				print("rv> old string: {}\nrv> new string: {}".format(old_string, META_STRING))

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
			global META_STRING

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
				META_STRING = META_STRING.lower()
			elif option in ["upper", "u"]:
				META_STRING = META_STRING.upper()
			elif option in ["capitalize", "c"]:
				META_STRING = META_STRING.capitalize()
			elif option in ["alternating", "a"]:
				META_STRING = list(META_STRING)
				i = 0
				while i < len(META_STRING):
					if i%2 == 0:
						META_STRING[i] = META_STRING[i].lower()
					else:
						META_STRING[i] = META_STRING[i].upper()
					i+=1
				META_STRING = "".join(META_STRING)

			elif option in ["inverse", "i"]:
				META_STRING = META_STRING.swapcase()

	class Numeral:
		def __init__(self):
			self.help = "converts numerals from one base to another"+SPACER
			self.check_ok = False
			self.multi_arg = False
			self.choices = ["bin","oct","dec","hex","roman"]
			self.readtype = ""
			self.runcount = 0
			self.roman_numerals = ["i", "v", "x", "l", "c", "d", "m"]
			self.convertto_dict = {"bin":"binary",
									"oct":"octal",
									"dec":"decimal",
									"hex":"hexadecimal",
									"roman":"roman"}

		def run(self):
			global META_STRING

			def int_to_roman(mstring):
				None

			def mutate_string(mstring, option, base):
				global META_STRING_TYPE

				if option == "bin":
					META_STRING_TYPE = "binary"
					mstring = str(bin(int(mstring, base)))[2:]
				elif option == "oct":
					META_STRING_TYPE = "octal"
					mstring = str(oct(int(mstring, base)))[2:]
				elif option == "dec":
					META_STRING_TYPE = "decimal"
					mstring = str(int(mstring, base))
				elif option == "hex":
					META_STRING_TYPE = "hexadecimal"
					mstring = str(hex(int(mstring, base)))[2:]
				elif option == "roman":
					META_STRING_TYPE = "roman"
					########## TO BE IMPLEMENTED
					parser.error("conversion to roman numerals is not yet implemented")

				return mstring

			print(args.n)
			if not self.check_ok:
				if any(isinstance(i, list) for i in args.n):
					self.multi_arg = True

			# check if multiple -n options have been supplied
			if self.multi_arg:
				convertto = args.n[self.runcount][0]
				self.runcount += 1
			else:
				convertto = args.n[0]

			# exclude string types from this module
			if META_STRING_TYPE == "string":
				parser.error("type string cannot be used with the numeral option")

			# check if args are proper
			if convertto not in self.choices:
				parser.error("{} is not a valid option for 'convertto'".format(convertto))
			if META_STRING_TYPE == self.convertto_dict[convertto]:
				return 0

			# remove whitespace
			META_STRING = META_STRING.replace(" ", "")

			# mutate numbers according to META_STRING_TYPE
			if META_STRING_TYPE == "binary":
				META_STRING = mutate_string(META_STRING, convertto, 2)
			elif META_STRING_TYPE == "octal":
				META_STRING = mutate_string(META_STRING, convertto, 8)
			elif META_STRING_TYPE == "decimal":
				META_STRING = mutate_string(META_STRING, convertto, 10)
			elif META_STRING_TYPE == "hexadecimal":
				META_STRING = mutate_string(META_STRING, convertto, 16)
			elif META_STRING_TYPE == "roman":
				for char in META_STRING:
					if char.lower() not in self.roman_numerals:
						parser.error("string contained {}, which is not a roman numeral".format(char))

	class Bitwise:
		def __init__(self):
			self.help = ("use a bitwise operation on"
						"\nthe currently worked on string."
						"\nthis requires a specification of"
						"\nthe operator and the operand B (opB)"
						"\noperand B type must be announced via"
						"\nprefixes (0b, 0o, 0d, 0x)"
						"\nexamples: ~&0xff"
						"\n          ~0b1010"
						"\n\n\tNOT  : ~opB"
						"\n\tAND  : &opB"
						"\n\tOR   : |opB"
						"\n\tXOR  : ^opB"
						"\n\tNAND : ~&opB"
						"\n\tNOR  : ~|opB"
						"\n\tNXOR : ~^opB"+SPACER)
			self.check_ok = False
			self.multi_arg = False
			self.runcount = 0
			self.legal_operations = ["~", "&", "|", "^"]

		def run(self):
			# check if args are nested
			if not self.check_ok:
				if any(isinstance(i, list) for i in args.bw):
					self.multi_arg = True

			# check if multiple -bw options have been supplied
			if self.multi_arg:
				operation = args.bw[self.runcount][0]
				self.runcount += 1
			else:
				operation = args.bw[0]




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
		elif arg == "-a":
			module_error = cView.Ascii.run()
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
		elif arg == "-bw":
			modul_error = cTransform.Bitwise.run()

		if module_error:
			break

if __name__ == "__main__":

	SPACER = "\n "
	META_STRING = ""

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

	parser.add_argument("-a", help=cView.Ascii.help, action="store_true")

	parser.add_argument("-b", help=cView.Bytes.help, nargs=2, metavar=("format", "groupby"), action="append")

	parser.add_argument("-rp", help=cTransform.Replace.help, nargs=2, metavar=("find", "replace"), action="append")

	parser.add_argument("-rv", help=cTransform.Reverse.help, action="store_true")

	parser.add_argument("-cc", help=cTransform.ChangeCase.help, choices=cTransform.ChangeCase.choices, dest="case", action="append")

	#parser.add_argument("-n", help=cTransform.Numeral.help, nargs=2, metavar=("read", "convertto"), action="append")
	parser.add_argument("-n", help=cTransform.Numeral.help, nargs=1, metavar="type", action="append")

	parser.add_argument("-bw", help=cTransform.Bitwise.help, nargs=1, metavar="operation", action="append")

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

	args = parser.parse_args()
	META_STRING = args.input
	if args.init_as_bin:
		META_STRING_TYPE = "binary"
	elif args.init_as_oct:
		META_STRING_TYPE = "octal"
	elif args.init_as_dec:
		META_STRING_TYPE = "decimal"
	elif args.init_as_hex:
		META_STRING_TYPE = "hexadecimal"
	elif args.init_as_roman:
		META_STRING_TYPE = "roman"
	else:
		META_STRING_TYPE = "string"
	arg_chain = get_chain(sys.argv)
	#print(args)
	#print(sys.argv)
	#print(get_chain(sys.argv))
	mainLoop()
