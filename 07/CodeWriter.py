"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        output_stream.write("(eq)\n@sp\nA=A-1\nD=M\nA=A-1\nD=D-M\n@neg1\nD; JEQ\n@pos0\nD; JNE\n("
                            "lt)\n@sp\nA=A-1\nD=M\nA=A-1\nD=D-M\n@neg1\nD; JLT\n@pos0\nD; JGT\n("
                            "eq)\n@sp\nA=A-1\nD=M\nA=A-1\nD=D-M\n@pos0\nD; JEQ\n@neg1\nD; JNE\n("
                            "neg1)\nD=-1\n@END_EQ_LT_GT\n0; JMP\n(pos0)\nD=0\n@END_EQ_LT_GT\n0; JMP\n("
                            "END_EQ_LT_GT)\n@13\nA=M\n0; JMP\n")
        self.file_name = ""
        self.cur_label_index = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        pass

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        binary_commands_dic = {"add": "+", "sub": "-", "and": "&", "or": "|"}
        unary_commands_dic = {"neg": "-", "not": "!"}

        if command in ["add", "sub", "and", "or"]:
            cmd = binary_commands_dic[command]
            return f"@sp\nA=A-1\nD=M\nA=A-1\nM=M{cmd}D\n@sp\nM=M-1\n"
        if command in ["neg", "not"]:
            cmd = unary_commands_dic[command]
            return f"@sp\nA=A-1\nM={cmd}M\n"
        if command in ['eq', 'lt', 'gt']:
            return f"@label_{self.cur_label_index}_{command}\nD=A\n@13\nM=D\n@{command}\n0;JMP\n(@label_{self.cur_label_index}_{command})\n"

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        if segment == 'static':
            if command == "C_PUSH":
                return f"@{self.file_name}.{index}\nA=M\nD=M\n@sp\nA=M\nM=D\n@sp\nM=M+1\n"
            if command == "C_POP":
                return f"@{self.file_name}.{index}\nA=M\nD=M\n@sp\nA=M-1\nM=D\n@sp\nM=M-1\n"

        if segment == 'constant':
            if command == "C_PUSH":
                return f"@{index}\nD=A\n@sp\nA=M\nM=D\n@sp\nM=M+1\n"

        if segment == 'pointer':
            seg_dic = {0: "THIS", 1: "THAT"}
            seg = seg_dic[index]
            if command == "C_PUSH":
                return f"@{seg}\nA=M\nD=M\n@sp\nA=M\nM=D\n@sp\nM=M+1\n"
            if command == "C_POP":
                return f"@{seg}\nA=M\nD=M\n@sp\nA=M-1\nM=D\n@sp\nM=M-1\n"

        if segment in ['local', 'argument']:
            seg_dic = {'local': 'LCL', 'argument': 'ARG'}
            seg = seg_dic[segment]
            if command == "C_PUSH":
                return f"@{seg}\nD=M\n@{index}\nA=D+A\nD=M\n@sp\nA=M\nM=D\n@sp\nM=M+1\n"
            if command == "C_POP":
                return f"@{seg}\nD=M\n@{index}\nA=D+A\nD=M\n@sp\nA=M-1\nM=D\n@sp\nM=M-1\n"

        if segment == 'temp':
            if command == "C_PUSH":
                return f"@5\nD=M\n@{index}\nA=D+A\nD=M\n@sp\nA=M\nM=D\n@sp\nM=M+1\n"
            if command == "C_POP":
                return f"@5\nD=M\n@{index}\nA=D+A\nD=M\n@sp\nA=M-1\nM=D\n@sp\nM=M-1\n"

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass
