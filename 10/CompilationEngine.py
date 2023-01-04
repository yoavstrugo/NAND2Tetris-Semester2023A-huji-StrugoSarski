"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from enum import Enum, EnumMeta

class MyEnumMeta(EnumMeta): 
    def __contains__(cls, item): 
        return item in [v.value for v in cls.__members__.values()] 

    def __eq__(cls, other):
        """Overrides the default implementation"""
        if isinstance(other, cls.__class__):
            return cls.value == other.value
        return False

class TokenTypes(Enum, metaclass=MyEnumMeta):
    IDENTIFIER = 'IDENTIFIER',
    SYMBOL = 'SYMBOL',
    KEYWORD = 'KEYWORD'

class VarTypes(Enum, metaclass=MyEnumMeta):
    INT = 'INT',
    CHAR = 'CHAR',
    BOOLEAN = 'BOOLEAN'

class Keywords(Enum, metaclass=MyEnumMeta):
    class ClassDecVar(Enum, metaclass=MyEnumMeta):
        STATIC = 'STATIC',
        FIELD = 'FIELD'
    class SubroutineDec(Enum, metaclass=MyEnumMeta):
        CONSTURCTOR = 'CONSTURCTOR',
        FUNCTION = 'FUNCTION',
        METHOD = 'METHOD'

class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.tokenizer = input_stream
        self.out = output_stream

    
    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.out.write("<class>")
        self.out.write('<keyword> class </keyword>')

        # Class name
        self.tokenizer.advance() 
        assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, f'{self.tokenizer.identifier()} is not a valid identifier'
        className = self.tokenizer.identifier()
        self.out.write(f'<identifier> {className} </identifier>')

        # Opening parenthesis
        self.tokenizer.advance() 
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == '{', 'Expected \'{\' after class decleration' + f' {className}'
        self.out.write('<symbol> { </symbol>')

        # Class var declerations compilation
        self.tokenizer.advance() 
        while True:
            token_type = self.tokenizer.token_type()
            assert token_type in {TokenTypes.KEYWORD, TokenTypes.SYMBOL}, f'Expected a keyword inside a class, got {self.tokenizer.keyword()}'

            if token_type == TokenTypes.SYMBOL and self.tokenizer.symbol() == '}':
                # closing parenthesis, end of class
                break

            keyword = self.tokenizer.keyword()
            assert keyword in Keywords.ClassDecVar or keyword in Keywords.SubroutineDec, f'Expected a class variable decleration or a sub routine decleration, got {keyword}'

            if keyword in Keywords.ClassDecVar:
                # compile var decleration
                self.compile_class_var_dec()
                pass
            elif keyword in Keywords.SubroutineDec:
                # continue to next loop to compile subroutines
                break

            self.tokenizer.advance() 
        
        # Subroutines compilation
        while True:
            token_type = self.tokenizer.token_type()
            assert token_type in {TokenTypes.KEYWORD, TokenTypes.SYMBOL}, f'Expected a keyword inside a class, got {self.tokenizer.keyword()}'

            if token_type == TokenTypes.SYMBOL and self.tokenizer.symbol() == '}':
                # closing parenthesis, end of class
                break

            keyword = self.tokenizer.keyword()
            assert keyword in Keywords.SubroutineDec, f'Expected a sub routine decleration, got {keyword}'

            self.compile_subroutine()
            self.tokenizer.advance()
                
        assert token_type == TokenTypes.SYMBOL and self.tokenizer.symbol() == '}', '\}\' expected at the end of class decleration.'
        self.out.write('<symbol> } </symbol>')
        

        self.out.write("</class>")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.out.write("<classVarDec>")
        self.out.write("</classVarDec>")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.out.write("<subroutineDec>")

        # routine type
        assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Expected a keyword'
        routine_type = self.tokenizer.keyword()
        assert routine_type in Keywords.SubroutineDec, f'keyword {routine_type} not expected here'
        self.out.write(f"<keyword> {routine_type.lower()} </keyword>")

        # return type
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Expected a keyword'
        return_type = self.tokenizer.keyword()
        assert return_type == 'VOID' or return_type in VarTypes
        self.out.write(f"<keyword> {return_type.lower()} </keyword>")

        # routine name
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Expected an identifier'
        routine_name = self.tokenizer.identifier()
        self.out.write(f"<identifier> {routine_name} </identifier>")

        # opening parenthesis
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol == '(', 'Expected \'(\''

        self.out.write("</subroutineDec>")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.out.write("<parameterList>")
        self.out.write("</parameterList>")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.out.write("<varDec>")
        self.out.write("</varDec>")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        pass

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.out.write("<doStatement>")
        self.out.write("</doStatement>")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.out.write("<letStatement>")
        self.out.write("</letStatement>")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.out.write("<whileStatement>")
        self.out.write("</whileStatement>")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.out.write("<returnStatement>")
        self.out.write("</returnStatement>")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.out.write("<ifStatement>")
        self.out.write("</ifStatement>")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        pass

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        self.out.write("<term>")
        self.out.write("</term>")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        pass
