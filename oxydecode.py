#!/usr/bin/env python3

######################################
# OxyDecode
# A tool for simple Cryptoanalysis
# Made by Oxynon
#
#
# Examples:
#
# 	- oxydecode.py <ciphertext>
# 	  
# 	  using oxydecode in this way allows the program
#	  to move through all the features and determines
# 	  if the ciphertext can be solved by it.
#
#
#	- oxydecode.py convert <ciphertext>
#
#	  'convert' converts ASCII to Bytes (Binary/Decimal/Hex/Octal)
#	  and vice-versa. 
#
# 	- oxydecode.py cipher julius [1-23] <ciphertext>
#
#	  the keyword 'cipher' is used to specify 
#
#	  the keyword 'convert' is used 
######################################

import argparse
from argparse import RawTextHelpFormatter

class Decoder:

	def __init__(self):

		# INITIALIZE ALL CLASSES FIRST
		self.convert = self.Convert()
		self.transform = self.Transform()

		# STRINGS
		self.mode_help = "specify to use a specific mode\nuse '<keyword> -h' to get more info"

	def parse(self):
		# ARGPARSE STUFF
		self.parser = argparse.ArgumentParser(description="A tool for simple Cryptoanalysis", formatter_class=RawTextHelpFormatter)
		self.parser.add_argument("-v", "--verbose", help="show more verbose output", action="store_true")
		self.subparsers = self.parser.add_subparsers(help=self.mode_help)

		self.parser_convert = self.subparsers.add_parser("convert", help=self.convert.help, formatter_class=RawTextHelpFormatter)
		self.parser_convert.add_argument("input", help=self.convert.input.help, type=str, action="store")

		# TRANSFORM SUBPARSER
		self.parser_transform = self.subparsers.add_parser("transform", help=self.transform.help, formatter_class=RawTextHelpFormatter)
		self.subparsers_transform = self.parser_transform.add_subparsers(help=self.mode_help)

		# REPLACE SUBPARSER
		self.subparser_transform_replace = self.subparsers_transform.add_parser("replace", help=self.transform.replace.help, formatter_class=RawTextHelpFormatter)
		self.subparser_transform_replace.add_argument("text", help=self.transform.replace.help, type=str, action="store")
		self.subparser_transform_replace.add_argument("find", help=self.transform.replace.help, type=str, action="store")
		self.subparser_transform_replace.add_argument("replace", help=self.transform.replace.help, type=str, action="store")
		
		# REVERSE SUBPARSER
		self.subparser_transform_reverse = self.subparsers_transform.add_parser("reverse", help=self.transform.reverse.help, formatter_class=RawTextHelpFormatter)
		self.subparser_transform_reverse.add_argument("text", help=self.transform.reverse.help, action="store")

		# CHANGECASE SUBPARSER
		self.subparser_transform_changecase = self.subparsers_transform.add_parser("changecase", help=self.transform.changecase.help, formatter_class=RawTextHelpFormatter)
		self.subparser_transform_changecase.add_argument("casetype", choices=["lower", "upper", "capitalize", "alternate", "invert"], help=self.transform.changecase.help, action="store")
		self.subparser_transform_changecase.add_argument("text", help=self.transform.changecase.help, action="store")

		# NUMERAL SUBPARSER
		self.subparser_transform_numeral = self.subparsers_transform.add_parser("numeral", help=self.transform.numeral.help, formatter_class=RawTextHelpFormatter)
		self.subparser_transform_numeral.add_argument("in_type", choices=[2,8,10,16,"roman"], help=self.transform.numeral.help, action="store")		
		self.subparser_transform_numeral.add_argument("out_type", choices=[2,8,10,16,"roman"], help=self.transform.numeral.help, action="store")
		self.subparser_transform_numeral.add_argument("input", help=self.transform.numeral.help, action="store")
		
		# BITWISE SUBPARSER
		self.subparser_transform_bitwise = self.subparsers_transform.add_parser("bitwise", help=self.transform.bitwise.help, formatter_class=RawTextHelpFormatter)
		self.subparser_transform_bitwise.add_argument("operation", choices=["NOT", "AND", "OR", "XOR", "NAND", "NOR", "NXOR"], help=self.transform.bitwise.help, action="store")
		self.subparser_transform_bitwise.add_argument("number", help=self.transform.bitwise.help, action="store")


		self.args = self.parser.parse_args()

	class Convert:

		def __init__(self):
			self.help = "convert ASCII to bytes"
			self.input = self.Input()

		class Input:

			def __init__(self):
				self.help = ("convert - ASCII <-> (Decimal, Binary, Hexadecimal, Octal)"
						"\nOutputs all when using ASCII"
						"\nas input. When converting"
						"\nto ASCII the input must be prepended by:"
						"\n'd/' for decimal"
						"\n'b/' for binary"
						"\n'h/' for hexadecimal"
						"\n'o/' for octal")

	class Transform:

		def __init__(self):
			self.help = "multiple transformations of data"
			self.replace = self.Replace()
			self.reverse = self.Reverse()
			self.changecase = self.ChangeCase()
			self.numeral = self.Numeral()
			self.bitwise = self.Bitwise()

		class Replace:

			def __init__(self):
				self.help = ("finds a specific character or"
							"\nsequence of characters and"
							"\nreplaces them"
							"\n\nExample:"
							"\n\toxydecode.py transform -replace <input> <find> <replace>"
							"\n ")

		class Reverse:

			def __init__(self):
				self.help = ("reverses a string of characters"
							"\n\nExample:"
							"\n\toxydecode.py transform -reverse <input>"
							"\n ")

		class ChangeCase:

			def __init__(self):
				self.help = ""

		class Numeral:

			def __init__(self):
				self.help = ""

		class Bitwise:

			def __init__(self):
				self.help = ""

	class Alphabet:
		None

	class Cipher:
		None

	class Encode:
		None

	class Modern:
		None

if __name__ == "__main__":

	CHOICES=["convert", "transform", "alphabet", "cipher", "encode", "modern"]
	OD = Decoder()
	OD.parse()
