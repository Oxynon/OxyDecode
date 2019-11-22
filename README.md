# OxyDecode

OxyDecode is a simple Cryptoanalysis tool for cli. It's a program based on the amazing website [cryptii.com](https://cryptii.com)
This is a work in progress! Very few of the planned features are actually implemented up until now.
See the list below to get an overview of what does and doesn't work.

## Features

* = to be implemented

- Transform
  - To Ascii
  - To Bytes
  - Find and replace
  - Reverse
  - Change letter case
  - Change numeral system*
  - Bitwise operations*
- Alphabets*
- Ciphers*
- Encoding*
- Modern*
- Interactive setup*


## How to use

Since Oxydecode always requires `<input>` this should be your first argument.
Every following argument will have subcommands (exceptions are `-p, -rv, --wizard`)
For example let's say we have a string and we want to convert it from ASCII to 
hexadecimal with no spaces between byte subgroups. The command for this is:
```
Input:  ./oxydecode.py inputstring -b hex 0
Output: b> 696e707574737472696e67
```
The 0 in this case stands for no grouping, as opposed to
```
Input:  ./oxydecode.py inputstring -b hex 2B
Output: b> 696e 7075 7473 7472 696e 67
```
for a grouping of 2 Bytes.

Of course `./oxydecode.py -h` can be used to see all available commands and subcommands
