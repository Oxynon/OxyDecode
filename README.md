# OxyDecode

OxyDecode is a simple Cryptoanalysis tool for cli. It's a program based on the amazing website [cryptii.com](https://cryptii.com)
This is a work in progress! Very few of the planned features are actually implemented up until now.
See the list below to get an overview of what does and doesn't work.

## Features

\* = to be implemented

- Print current string
- Transform
  - To Ascii
  - To Bytes
  - Find and replace
  - Reverse
  - Change letter case
  - Change numeral system
  	- Binary
  	- Octal
  	- Decimal
  	- Hexadecimal
  	- Roman Letters*
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
hexadecimal with no spaces between byte groups. The command for this is:
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

What makes [cryptii.com](https://cryptii.com) so powerful a tool is that the user is given the ability 
to chain these different modules together. 
The same can also be done with Oxydecode. An example:
```
Input:  ./oxydecode.py string --show-prefix -v -p -rv -b hex B -rp 6e 90 -p -b bin 0 -p
Output: p> string
        rv> old string: string
        rv> new string: gnirts
        b> 67 6e 69 72 74 73
        rp successful // find:6e // replace:90
        New string: 67 90 69 72 74 73
        p0x> 67 90 69 72 74 73
        b> 11001111001000001101001011100100111010001110011
        p0b> 11001111001000001101001011100100111010001110011
```
Let's break down what's happening. We start Oxydecode with the input `string`, we then use
`--show-prefix` to enable the `p0x> p0b>` information on the print command `-p`.
`-v` or `--verbose` gives us extra information like the `rv>` printed message.
`-b` should already be familiar to you, we use it to change the string to hexadecimal, byte-sized chunks.
`-rp` stands for 'replace' and allows you to find and replace chars on the current string.
In this case we exchange the byte `6e` with `90` and then print the result with `-p`.
The two last steps use `-b bin 0` to convert the hexadecimal bytes to binary bytes with no spacing.
And last but not least a `-p` for good measure. 
As you can see by the generated output, the commands were executed in order as written in the command.


Of course `./oxydecode.py -h` can be used to see all available commands and subcommands
