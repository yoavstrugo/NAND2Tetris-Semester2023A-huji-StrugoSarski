"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


COMP_TABLE = {
    '0':    '110101010',
    '1':    '110111111',
    '-1':   '110111010',
    'D':    '110001100',
    'A':    '110110000',
    '!D':   '110001101',
    '!A':   '110110001',
    '-D':   '110001111',
    '-A':   '110110011',
    'D+1':  '110011111',
    'A+1':  '110110111',
    'D-1':  '110001110',
    'A-1':  '110110010',
    'D+A':  '110000010',
    'D-A':  '110010011',
    'A-D':  '110000111',
    'D&A':  '110000000',
    'D|A':  '110010101',
    'M':    '111110000',
    '!M':   '111110001',
    '-M':   '111110011',
    'M+1':  '111110111',
    'M-1':  '111110010',
    'D+M':  '111000010',
    'D-M':  '111010011',
    'M-D':  '111000111',
    'D&M':  '111000000',
    'D|M':  '111010101',
    'A<<':  '010100000',
    'D<<':  '010110000',
    'M<<':  '011100000',
    'A>>':  '010000000',
    'D>>':  '010010000',
    'M>>':  '011000000'
}

DST_TABLE = {
    'null': '000',
    'M':    '001',
    'D':    '010',
    'MD':   '011',
    'A':    '100',
    'AM':   '101',
    'AD':   '110',
    'AMD':  '111'
}

JMP_TABLE = {
    'null': '000',
    'JGT':  '001',
    'JEQ':  '010',
    'JGE':  '011',
    'JLT':  '100',
    'JNE':  '101',
    'JLE':  '110',
    'JMP':  '111'
}

def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    program_counter = 0
    sym_table = SymbolTable()
    parser = Parser(input_file)
    # First pass
    while parser.has_more_commands():
        comm_type = parser.command_type()
        if comm_type == 'L_COMMAND':
            sym = parser.symbol()
            if not sym_table.contains(sym):
                sym_table.add_entry(parser.symbol(), program_counter)
            else:
                assert False, f'Error: symbol \'{sym}\' is already defined'
        else:
            # Only increase the program counter if it's
            # *not* a label
            program_counter += 1

        parser.advance()

    # Second pass
    next_sym_addr = 0x10
    parser.reset() # Reset the parser
    while parser.has_more_commands():
        comm_type = parser.command_type()
        if comm_type == 'A_COMMAND':
            # 3 Options:
            # 1 - Number referencing an address
            # 2 - Symbol is in the table
            # 3 - Symbol defines a new variable

            sym = parser.symbol() # Get the symbol

            if sym.isdigit():
                # op1 - symbol is a number 
                # the symbol is an address
                output_file.write(f'{int(sym):0>16b}\n')
            elif sym_table.contains(sym):
                # op2 - symbol is in the symbol table
                # get the symbol's address and write to output
                address = sym_table.get_address(sym)
                output_file.write(f'{int(address):0>16b}\n')
            else:
                # op3 - symbol defines a new variable
                # add the symbol to the table
                sym_table.add_entry(sym, next_sym_addr)
                next_sym_addr += 1

                # get the new address of the symbol and write to the output
                address = sym_table.get_address(sym)
                output_file.write(f'{int(address):0>16b}\n')
        elif comm_type == 'C_COMMAND':
            comp = COMP_TABLE.get(parser.comp(), None)
            assert comp is not None, f'Error: unknown comp \'{parser.comp()}\' on line {parser.cur_index}'
            dst = DST_TABLE.get(parser.dest(), None)
            assert dst is not None, f'Error: unknown dest \'{parser.dest()}\' on line {parser.cur_index}'
            jmp = JMP_TABLE.get(parser.jump(), None)
            assert jmp is not None, f'Error: unknown jump \'{parser.jump()}\' on line {parser.cur_index}'
            
            # The output c_command=1bit=1, comp=9bit, dst=3bit, jmp=3bit --> total 16bits
            output_file.write(f'1{comp}{dst}{jmp}\n') 
        parser.advance()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
