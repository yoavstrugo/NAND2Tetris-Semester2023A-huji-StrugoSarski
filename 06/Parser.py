"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        raw_lines = input_file.read().splitlines()
        raw_lines = [line.replace(' ', '') for line in raw_lines]
        raw_lines = [line.replace('\t', '') for line in raw_lines]
        raw_lines = [line for line in raw_lines if line[0:1] != '//']
        self.lines = [line.split('//')[0] for line in raw_lines]
        self.lines = [line for line in self.lines if len(line) > 0]
        self.reset()

    def reset(self):
        self.cur_line = self.lines[0]
        self.cur_index = 0

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.cur_index < len(self.lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!
        self.cur_index += 1
        if self.has_more_commands():
            self.cur_line = self.lines[self.cur_index]

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        if self.cur_line[0] == '@':
            return 'A_COMMAND'
        if self.cur_line[0] == '(':
            return 'L_COMMAND'
        return 'C_COMMAND'

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        return self.cur_line.replace('(', '').replace(')', '').replace('@', '')

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if '=' in self.cur_line:
            # the command has a 'DST' field
            return self.cur_line.split('=')[0]

        return 'null'

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        comp = self.cur_line
        if '=' in comp:
            comp = comp.split('=')[1] # Remove the DST part
        return comp.split(';')[0] # If is has a JMP part it will be removed

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if ';' in self.cur_line:
            return self.cur_line.split(';')[1]

        return 'null'


# (DST=)?COMP(;JMP)?;