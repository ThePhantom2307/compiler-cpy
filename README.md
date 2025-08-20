
# Compiler for CutePy Language

This project implements a simple compiler for a custom Python-like language (`.cpy`).  
It tokenizes the source, checks syntax, builds symbol tables, and emits an intermediate representation.

## Features
- Lexical analysis for keywords, identifiers, operators, separators, and blocks  
- Syntax analysis with support for functions, conditional statements, loops, and nested scopes  
- Generation of intermediate code (`.int`) and symbol tables (`.sym`)

## Requirements
- Python 3.x

## Usage
1. Place your `.cpy` source file in the project directory.
2. Run the compiler:
   ```bash
   python compiler.py yourfile.cpy
   ```
3. The compiler produces:
	 - yourfile.int – intermediate code
	 - yourfile.sym – symbol table

A sample program is available in test.cpy demonstrating functions, loops, and nested definitions.

### Example
```bash
python compiler.py test.cpy
```
