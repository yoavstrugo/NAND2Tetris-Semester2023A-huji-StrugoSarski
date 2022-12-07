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
        output_stream.write("@codeStart\n0; JMP\n")

        output_stream.write("(eq) \
                            \r\t@SP \
                            \r\tA=M \
                            \r\tA=A-1 \
                            \r\tD=M \
                            \r\tA=A-1 \
                            \r\tD=D-M \
                            \r\t@neg1 \
                            \r\tD; JEQ \
                            \r\t@pos0 \
                            \r\tD; JNE\n")

        output_stream.write("(lt) \
                                     \r\t@SP \
                                     \r\tA=M \
                                     \r\tA=A-1 \
                                     \r\tD=M \
                                     \r\tA=A-1 \
                                     \r\tD=M-D \
                                     \r\t@neg1 \
                                     \r\tD; JLT \
                                     \r\t@pos0 \
                                     \r\tD; JMP\n")

        output_stream.write("(gt) \
                                     \r\t@SP \
                                     \r\tA=M \
                                     \r\tA=A-1 \
                                     \r\tD=M \
                                     \r\tA=A-1 \
                                     \r\tD=M-D \
                                     \r\t@neg1 \
                                     \r\tD; JGT \
                                     \r\t@pos0 \
                                     \r\tD; JMP\n")

        output_stream.write(
            '(neg1) \
                \r\tD=-1 \
                \r\t@END_EQ_LT_GT \
                \r\t0; JMP \
                \n(pos0) \
                \r\tD=0 \
                \r\t@END_EQ_LT_GT \
                \r\t0; JMP\n')

        output_stream.write(
            '(END_EQ_LT_GT) \
                \r\t@SP \
                \r\tM=M-1 // Decrease SP by 1\
                \r\tA=M \
                \r\tA=A-1 \
                \r\tM=D // Push D to the stack \
                \r\t@R13 \
                \r\tA=M \
                \r\t0; JMP\n')

        output_stream.write("(codeStart)\n")

        self.out = output_stream
        self.file_name = ""
        self.cur_label_index = 0
        self.label_dict = {}

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
        self.file_name = filename

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

        self.out.write(f'//{command}\n')  # Debugging
        if command in ["add", "sub", "and", "or"]:
            op = binary_commands_dic[command]
            self.out.write(
                f'@SP \
                  \r\tM=M-1 // Point to the top of the stack (y) \
                  \r\tA=M // A points to the next slot \
                  \r\tD=M // D is one of the values (y) \
                  \r\tA=A-1 // A points to next value (x) \
                  \r\tM=M{op}D // Preform the operation, x op y\n')
        if command in ["neg", "not"]:
            cmd = unary_commands_dic[command]
            self.out.write(f"@SP \
                             \r\tA=M \
                             \r\tA=A-1 \
                             \r\tM={cmd}M\n")
        if command in ['eq', 'lt', 'gt']:
            self.out.write(
                f"@label_{self.cur_label_index}_{command} \
                  \r\tD=A \
                  \r\t@R13 \
                  \r\tM=D \
                  \r\t@{command} \
                  \r\t0;JMP \
                  \r\t(label_{self.cur_label_index}_{command})\n")
            self.cur_label_index += 1

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
        self.out.write(f'//{command} {segment} {index}\n')  # Debugging

        if segment == 'constant':
            if command == "C_PUSH":
                self.out.write(f"@{index} \
                                \r\tD=A \
                                \r\t@SP \
                                \r\tA=M \
                                \r\tM=D \
                                \r\t@SP \
                                \r\tM=M+1\n")
        elif segment in ['temp', 'pointer']:
            # temp start at 5
            base = '5' if segment == 'temp' else 'THIS'
            if command == 'C_PUSH':
                self.out.write(
                    f'@{base} \
                        \r\tD=A // D now has the base \
                        \r\t@{index} // index \
                        \r\tA=A+D // A now has the value\'s address \
                        \r\tD=M // D now has the value it self \
                        \n\
                        \r\t@SP \
                        \r\tA=M // A has the address of the next slot in the stack \
                        \r\tM=D // Put the value into the next stack\'s slot \
                        \r\t@SP \
                        \r\tM=M+1 // Increase SP by 1\n')
            elif command == 'C_POP':
                self.out.write(
                    f'@SP \
                        \r\tM=M-1 // Decrease 1 from SP \
                        \r\tA=M // Get the address of the stack item \
                        \r\tD=M // The value is now in D \
                        \r\t@R13 \
                        \r\tM=D // Save the value in R1 \
                        \n\
                        \r\t@{base} \
                        \r\tD=A // Address of local \
                        \r\t@{index} // Offset\
                        \r\tA=D+A // Actual address\
                        \r\tD=A // D is the address\
                        \r\t@R14\
                        \r\tM=D // address is in R2 \
                        \n\
                        \r\t@R13\
                        \r\tD=M // Value is in D\
                        \r\t@R14 // Address is in M\
                        \r\tA=M \
                        \r\tM=D\n')
        else:
            label = ''
            if segment == 'static':
                label = f'{self.file_name}.{index}'
            elif segment in ['this', 'that']:
                label = segment.upper()
            elif segment in ['local', 'argument']:
                label = 'LCL' if segment == 'local' else 'ARG'
            else:
                print(f'Something is wrong here {command} {segment} {index}')

            if command == 'C_PUSH':
                self.out.write(
                    f'@{label} \
                        \r\tD=M // D now has the base \
                        \r\t@{index} // index \
                        \r\tA=A+D // A now has the value\'s address \
                        \r\tD=M // D now has the value it self \
                        \n\
                        \r\t@SP \
                        \r\tA=M // A has the address of the next slot in the stack \
                        \r\tM=D // Put the value into the next stack\'s slot \
                        \r\t@SP \
                        \r\tM=M+1 // Increase SP by 1\n')
            elif command == 'C_POP':
                self.out.write(
                    f'@SP \
                        \r\tM=M-1 // Decrease 1 from SP \
                        \r\tA=M // Get the address of the stack item \
                        \r\tD=M // The value is now in D \
                        \r\t@R13 \
                        \r\tM=D // Save the value in R1 \
                        \n\
                        \r\t@{label} \
                        \r\tD=M // Address of local \
                        \r\t@{index} // Offset\
                        \r\tA=D+A // Actual address\
                        \r\tD=A // D is the address\
                        \r\t@R14\
                        \r\tM=D // address is in R2 \
                        \n\
                        \r\t@R13\
                        \r\tD=M // Value is in D\
                        \r\t@R14 // Address is in M\
                        \r\tA=M \
                        \r\tM=D\n')

    def end_file(self):
        self.out.write("(finalLoop) \
                            \r\t@finalLoop \
                            \r\t0; JMP\n")

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
        label_name_in_file = f'{self.file_name}.{self.cur_function_name}${label}'
        self.out.write(f'({label_name_in_file})')

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        label_name_in_file = f'{self.file_name}${label}'
        self.out.write(f'0; JMP {label_name_in_file}')

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self.out.write("@SP \
                        \rM=M-1 \
                        \rA=M \
                        \rA; JNE\n")

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
        self.write(f'{function_name}\n')
        for i in range(n_vars):
            self.out.write(f"@0 \
                            \r\tD=A \
                            \r\t@SP \
                            \r\tA=M \
                            \r\tM=D \
                            \r\t@SP \
                            \r\tM=M+1\n")

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
