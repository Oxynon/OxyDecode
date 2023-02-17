from modules import Universals

def init():


	class cReplace:
		
		def __init__(self):
			self.help = ("find a substring and"
						"\nreplace it with something"
						"\n\ntwo arguments required:"
						"\nfind -> the substring to find"
						"\nreplace -> string to replace with"+Universals.SPACER)

			self.runcount = 0
			self.check_ok = False
			self.multi_arg = False

		def run(self):

			if not self.check_ok:
				if any(isinstance(i, list) for i in Universals.ARGS.rp):
					self.multi_arg = True
					self.check_ok = True

			# check if multiple -rp options have been supplied
			if self.multi_arg:
				find, replace = Universals.ARGS.rp[self.runcount]
				self.runcount += 1
			else:
				find, replace = Universals.ARGS.rp

			if find not in Universals.META_STRING:
				print("Error - '{}' not found in '{}'".format(find, Universals.META_STRING))
				if Universals.args.verbose:
					print("rp failed // find:{} // replace:{}\nold string: {}".format(find, replace, Universals.META_STRING))
				return 1
			else:
				# the actual magic
				Universals.META_STRING = Universals.META_STRING.replace(find, replace)
				if Universals.ARGS.verbose:
					print("rp successful // find:{} // replace:{}\nNew string: {}".format(find, replace, Universals.META_STRING))
				return 0

	class cReverse:
		# reversing a file could be a future feature
		# for now it only reverses strings
		def __init__(self):
			self.help = "reverses the currently used string"+Universals.SPACER
			#self.check_ok = False
			#self.multi_arg = False

		def run(self):

			old_string = Universals.META_STRING

			Universals.META_STRING = Universals.META_STRING[::-1]

			if Universals.ARGS.verbose:
				print("rv> old string: {}\nrv> new string: {}".format(old_string, Universals.META_STRING))

	class cChangeCase:
		def __init__(self):
			self.help = ("changes the case of the current string"
						"\n\nrequired argument:"
						"\nlower, l -> make string lower case"
						"\nupper, u -> make string upper case"
						"\ncapitalize, c -> capitalize a string"
						"\nalternating, a -> alternate case (lower, upper)"
						"\ninverse, i -> invert case on string"+Universals.SPACER)
			self.choices=["lower", "upper", "capitalize", "alternating", "inverse", "l", "u", "c", "a", "i"]
			self.check_ok = False
			self.multi_arg = False
			self.runcount = 0

		def run(self):

			old_string = Universals.META_STRING

			if not self.check_ok:
				if any(isinstance(i, list) for i in Universals.ARGS.case):
					self.multi_arg = True

			# check if multiple -cc options have been supplied
			if self.multi_arg:
				option = Universals.ARGS.case[self.runcount]
				self.runcount += 1
			else:
				option = Universals.ARGS.case[0]

			if option in ["lower", "l"]:
				Universals.META_STRING = Universals.META_STRING.lower()
			elif option in ["upper", "u"]:
				Universals.META_STRING = Universals.META_STRING.upper()
			elif option in ["capitalize", "c"]:
				Universals.META_STRING = Universals.META_STRING.capitalize()
			elif option in ["alternating", "a"]:
				Universals.META_STRING = list(Universals.META_STRING)
				i = 0
				while i < len(Universals.META_STRING):
					if i%2 == 0:
						Universals.META_STRING[i] = Universals.META_STRING[i].lower()
					else:
						Universals.META_STRING[i] = Universals.META_STRING[i].upper()
					i+=1
				Universals.META_STRING = "".join(Universals.META_STRING)

			elif option in ["inverse", "i"]:
				Universals.META_STRING = Universals.META_STRING.swapcase()

			if Universals.ARGS.verbose:
				print("cc> old string: {}\ncc> new string: {}".format(old_string, Universals.META_STRING))

	class cNumeral:
		def __init__(self):
			self.help = "converts numerals from one base to another"+Universals.SPACER
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

			def int_to_roman(mstring):
				None

			def mutate_string(mstring, option, base):

				if option == "bin":
					Universals.META_STRING_TYPE = "binary"
					mstring = str(bin(int(mstring, base)))[2:]
				elif option == "oct":
					Universals.META_STRING_TYPE = "octal"
					mstring = str(oct(int(mstring, base)))[2:]
				elif option == "dec":
					Universals.META_STRING_TYPE = "decimal"
					mstring = str(int(mstring, base))
				elif option == "hex":
					Universals.META_STRING_TYPE = "hexadecimal"
					mstring = str(hex(int(mstring, base)))[2:]
				elif option == "roman":
					Universals.META_STRING_TYPE = "roman"
					########## TO BE IMPLEMENTED
					Universals.PARSER.error("conversion to roman numerals is not yet implemented")

				return mstring

			#print(Universals.ARGS.n)
			if not self.check_ok:
				if any(isinstance(i, list) for i in Universals.ARGS.n):
					self.multi_arg = True

			# check if multiple -n options have been supplied
			if self.multi_arg:
				convertto = Universals.ARGS.n[self.runcount][0]
				self.runcount += 1
			else:
				convertto = Universals.ARGS.n[0]

			# exclude string types from this module
			if Universals.META_STRING_TYPE == "string":
				Universals.PARSER.error("type string cannot be used with the numeral option")

			# check if args are proper
			if convertto not in self.choices:
				Universals.PARSER.error("{} is not a valid option for 'convertto'".format(convertto))
			if Universals.META_STRING_TYPE == self.convertto_dict[convertto]:
				return 0

			# remove whitespace
			Universals.META_STRING = Universals.META_STRING.replace(" ", "")

			# mutate numbers according to META_STRING_TYPE
			if Universals.META_STRING_TYPE == "binary":
				Universals.META_STRING = mutate_string(Universals.META_STRING, convertto, 2)
			elif Universals.META_STRING_TYPE == "octal":
				Universals.META_STRING = mutate_string(Universals.META_STRING, convertto, 8)
			elif Universals.META_STRING_TYPE == "decimal":
				Universals.META_STRING = mutate_string(Universals.META_STRING, convertto, 10)
			elif Universals.META_STRING_TYPE == "hexadecimal":
				Universals.META_STRING = mutate_string(Universals.META_STRING, convertto, 16)
			elif Universals.META_STRING_TYPE == "roman":
				for char in Universals.META_STRING:
					if char.lower() not in self.roman_numerals:
						Universals.PARSER.error("string contained {}, which is not a roman numeral".format(char))

	class cBitwise:
		def __init__(self):
			self.help = ("use a bitwise operation on"
						"\nthe currently worked on string."
						"\nthis requires a specification of"
						"\nthe operator and the operand B (opB)"
						"\noperand B type must be announced via"
						"\nprefixes (0b, 0o, 0d, 0x)"
						"\nexamples: \"~&0xff\""
						"\n          \"~0b1010\""
						"\nThis argument MUST be used with \" \""
						"\n\n\tNOT  : ~opB"
						"\n\tAND  : &opB"
						"\n\tOR   : |opB"
						"\n\tXOR  : ^opB"
						"\n\tNAND : ~&opB"
						"\n\tNOR  : ~|opB"
						"\n\tNXOR : ~^opB"+Universals.SPACER)
			self.check_ok = False
			self.multi_arg = False
			self.runcount = 0
			self.operations_dict = {"~":False,"&":False,"|":False,"^":False}
			self.legal_operations = list(self.operations_dict.keys())
			self.prefixes_dict = {"0b":False, "0o":False, "0d":False, "0x":False}
			self.legal_prefixes = list(self.prefixes_dict.keys())

		def run(self):

			# reset parse flags
			self.operations_dict = {"~":False,"&":False,"|":False,"^":False}
			self.prefixes_dict = {"0b":False, "0o":False, "0d":False, "0x":False}

			# check if args are nested
			if not self.check_ok:
				if any(isinstance(i, list) for i in Universals.ARGS.bw):
					self.multi_arg = True

			# check if multiple -bw options have been supplied
			if self.multi_arg:
				operation = Universals.ARGS.bw[self.runcount][0]
				self.runcount += 1
			else:
				operation = Universals.ARGS.bw[0]


			# check and parse supplied operation
			if len(operation) < 4:
				Universals.PARSER.error("operation '{}' is too short to be valid for -bw")
			if operation[:1] in self.legal_operations:
				if operation[:1] == "~":
					self.operations_dict["~"] = True
					if operation[1:2] in self.legal_operations:
						self.operations_dict[operation[1:2]] = True
						if operation[2:4] in self.legal_prefixes:
							self.prefixes_dict[operation[2:4]] = True
						else:
							Universals.PARSER.error("prefix '{}' is invalid for -bw".format(operation[2:4]))
					else:
						Universals.PARSER.error("operation '{}' is invalid for -bw".format(operation[1:2]))
				else:
					self.operations_dict[operation[:1]] = True
			else:
				Universals.PARSER.error("operation '{}' is invalid for -bw".format(operation[:1]))


	global Replace
	global Reverse
	global ChangeCase
	global Numeral
	global Bitwise

	type = "transform"
	Modules = ["replace", "reverse", "changecase", "numeral", "bitwise"]
	Replace = cReplace()
	Reverse = cReverse()
	ChangeCase = cChangeCase()
	Numeral = cNumeral()
	Bitwise = cBitwise()