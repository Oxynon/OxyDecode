from modules import Universals

def init():

	class cText:
		def __init__(self):
			self.parser = ""
			self.help = ("prints the analyzed string"
						"\nafter a module has been used."
						"\nno additional argument required"+Universals.SPACER)

		def run(self):
			if Universals.ARGS.show_prefix:
				if Universals.META_STRING_TYPE == "string":
					print("ps> "+Universals.META_STRING)
				elif Universals.META_STRING_TYPE == "binary":
					print("p0b> "+Universals.META_STRING)
				elif Universals.META_STRING_TYPE == "octal":
					print("p0o> "+Universals.META_STRING)
				elif Universals.META_STRING_TYPE == "decimal":
					print("p0d> "+Universals.META_STRING)
				elif Universals.META_STRING_TYPE == "hexadecimal":
					print("p0x> "+Universals.META_STRING)
			else:
				print("p> "+Universals.META_STRING)

			return 0

	class cAscii:
		def __init__(self):
			self.parser = ""
			self.help = "converts binary or hex to ASCII"+Universals.SPACER
			self.working_string = ""

		def run(self):

			self.working_string = Universals.META_STRING

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

			if Universals.META_STRING_TYPE not in self.allowed_types.keys():
				parser.error("type '{}' not supported by -a option".format(Universals.META_STRING_TYPE))

			if " " in self.working_string:
				self.working_string = self.working_string.replace(" ", "")

			Universals.META_STRING = self.allowed_types[Universals.META_STRING_TYPE](self.working_string)
			Universals.META_STRING_TYPE = "string"

			if Universals.ARGS.verbose:
				print("a> "+Universals.META_STRING)

			return 0

	class cBytes:
		
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
						"\n"+Universals.SPACER)

		def run(self):
			
			if not self.check_ok:
				
				# check if multiple -b options have been supplied
				if any(isinstance(i, list) for i in Universals.ARGS.b):
					self.multi_arg = True
				
					# check format & groupby value
					for parameters in Universals.ARGS.b:
						if parameters[0] not in self.format_choices:
							parser.error("{} is not a valid format".format(parameters[0]))
						if parameters[1] not in self.groupby_choices:
							parser.error("{} is not a valid groupby option".format(parameters[1]))

				self.check_ok = True

			# check if multiple -b options have been supplied
			if self.multi_arg:
				form, groupby = Universals.ARGS.b[self.runcount]
				self.runcount += 1
			else:
				form, groupby = Universals.ARGS.b

			# check format & groupby value
			if form not in self.format_choices:
				parser.error("{} is not a valid format".format(form))
			if groupby not in self.groupby_choices:
				parser.error("{} is not a valid groupby option".format(groupby))

			# reset print_str
			self.print_str = ""

			# apply format
			if form == "hex":
				if Universals.META_STRING_TYPE == "binary":
					self.print_str = hex(int(Universals.META_STRING.replace(" ", ""), 2))[2:]
				else:
					self.print_str = "".join(hex(ord(c))[2:] for c in Universals.META_STRING)
				Universals.META_STRING_TYPE = "hexadecimal"
				if groupby == "hB":
					self.print_str = " ".join(list(self.print_str))
				elif groupby == "B":
					self.print_str = " ".join([self.print_str[i:i+2] for i in range(0, len(self.print_str), 2)])
				elif groupby == "2B":
					self.print_str = " ".join([self.print_str[i:i+4] for i in range(0, len(self.print_str), 4)])
				elif groupby == "4B":
					self.print_str = " ".join([self.print_str[i:i+8] for i in range(0, len(self.print_str), 8)])

			elif form == "bin":
				if Universals.META_STRING_TYPE == "hexadecimal":
					self.print_str = bin(int(Universals.META_STRING.replace(" ", ""), 16))[2:]
				else:
					for c in Universals.META_STRING:
						tmpvar = str(bin(ord(c))[2:])
						if len(tmpvar) < 8:
							tmpvar = ("0"*(8-len(tmpvar)))+tmpvar 
						self.print_str += tmpvar

				Universals.META_STRING_TYPE = "binary"
				if groupby == "hB":
					self.print_str = " ".join([self.print_str[i:i+4] for i in range(0, len(self.print_str), 4)])
				elif groupby == "B":
					self.print_str = " ".join([self.print_str[i:i+8] for i in range(0, len(self.print_str), 8)])
				elif groupby == "2B":
					self.print_str = " ".join([self.print_str[i:i+16] for i in range(0, len(self.print_str), 16)])
				elif groupby == "4B":
					self.print_str = " ".join([self.print_str[i:i+32] for i in range(0, len(self.print_str), 32)])

			if Universals.ARGS.verbose:
				print("b> "+self.print_str)

			Universals.META_STRING = self.print_str

			return 0

	global Text
	global Ascii
	global Bytes
	#type = "view"
	Text = cText()
	Ascii = cAscii()
	Bytes = cBytes()
