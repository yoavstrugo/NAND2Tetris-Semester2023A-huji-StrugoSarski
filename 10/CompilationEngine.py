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


class MyEnum(Enum):
    def __eq__(self, other):
        return self.value == other


class Operations(MyEnum, metaclass=MyEnumMeta):
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'
    AND = '&'
    OR = '|'
    LT = '&lt;'
    GT = '&gt;'
    EQ = '='


class UnaryOperations(MyEnum, metaclass=MyEnumMeta):
    NEG = '-'
    NOT = '~'


class TokenTypes(MyEnum, metaclass=MyEnumMeta):
    IDENTIFIER = 'IDENTIFIER'
    SYMBOL = 'SYMBOL'
    KEYWORD = 'KEYWORD'
    INTEGER_CONST = 'INT_CONST'
    STRING_CONST = 'STRING_CONST'


class VarTypes(MyEnum, metaclass=MyEnumMeta):
    INT = 'int'
    CHAR = 'char'
    BOOLEAN = 'boolean'


class Keywords:
    class ClassDecVar(MyEnum, metaclass=MyEnumMeta):
        STATIC = 'static'
        FIELD = 'field'

    class SubroutineDec(MyEnum, metaclass=MyEnumMeta):
        CONSTURCTOR = 'constructor'
        FUNCTION = 'function'
        METHOD = 'method'

    class VarDec(MyEnum, metaclass=MyEnumMeta):
        VAR = 'var'

    class Statements(MyEnum, metaclass=MyEnumMeta):
        LET = 'let'
        IF = 'if'
        WHILE = 'while'
        DO = 'do'
        RETURN = 'return'

    class Constants(MyEnum, metaclass=MyEnumMeta):
        TRUE = 'true'
        FALSE = 'false'
        NULL = 'null'
        THIS = 'this'


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
        self.tab_counter = 0

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.printOpening('class')
        self.printToken()

        # Class name
        self.tokenizer.advance()
        assert self.tokenizer.token_type(
        ) == TokenTypes.IDENTIFIER, f'{self.tokenizer.identifier()} is not a valid identifier'
        className = self.tokenizer.identifier()
        self.printToken()

        # Opening parenthesis
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol(
        ) == '{', 'Expected \'{\' after class decleration' + f' {className}'
        self.printToken()

        # Class var declerations compilation
        self.tokenizer.advance()
        while True:
            token_type = self.tokenizer.token_type()
            assert token_type == TokenTypes.KEYWORD or token_type == TokenTypes.SYMBOL, f'Expected a keyword inside a class, got {self.tokenizer.keyword()}'

            if token_type == TokenTypes.SYMBOL and self.tokenizer.symbol() == '}':
                # closing parenthesis, end of class
                break

            keyword = self.tokenizer.keyword()
            assert keyword in Keywords.ClassDecVar or keyword in Keywords.SubroutineDec, f'Expected a class variable decleration or a sub routine decleration, got {keyword}'

            if keyword in Keywords.ClassDecVar:
                # compile var decleration
                self.compile_class_var_dec()
            elif keyword in Keywords.SubroutineDec:
                # continue to next loop to compile subroutines
                break

            self.tokenizer.advance()

        # Subroutines compilation
        while True:
            token_type = self.tokenizer.token_type()
            assert token_type in {
                TokenTypes.KEYWORD.value, TokenTypes.SYMBOL.value}, f'Expected a keyword inside a class, got {self.tokenizer.keyword()}'

            if token_type == TokenTypes.SYMBOL and self.tokenizer.symbol() == '}':
                # closing parenthesis, end of class
                break

            keyword = self.tokenizer.keyword()
            assert keyword in Keywords.SubroutineDec, f'Expected a sub routine decleration, got {keyword}'

            self.compile_subroutine()
            # self.tokenizer.advance()

        assert token_type == TokenTypes.SYMBOL and self.tokenizer.symbol(
        ) == '}', '\}\' expected at the end of class decleration.'
        self.printToken()

        self.printClosing('class')

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.printOpening('classVarDec')

        assert self.tokenizer.token_value() in Keywords.ClassDecVar, 'expeceted field or static'
        self.printToken()

        self.tokenizer.advance()

        # type
        assert self.tokenizer.token_type() in {
            TokenTypes.KEYWORD.value, TokenTypes.IDENTIFIER.value}, 'keyword or identifier expected'
        if self.tokenizer.token_type() == TokenTypes.KEYWORD:
            assert self.tokenizer.token_value(
            ) in VarTypes, f'Unknown var type {self.tokenizer.token_value()}'
        self.printToken()

        # name
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
        self.printToken()

        self.tokenizer.advance()

        while True:
            if self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == ';':
                break

            # ,
            assert self.tokenizer.token_type(
            ) == TokenTypes.SYMBOL and self.tokenizer.symbol() == ',', '\',\' expected'
            self.printToken()

            # name
            self.tokenizer.advance()
            assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
            self.printToken()

            self.tokenizer.advance()

        # ;
        assert self.tokenizer.token_type(
        ) == TokenTypes.SYMBOL and self.tokenizer.token_value() == ';', '\';\' expected'
        self.printToken()
        self.printClosing('classVarDec')
        # self.tokenizer.advance()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.printOpening('subroutineDec')

        # routine type
        assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Expected a keyword'
        routine_type = self.tokenizer.keyword()
        assert routine_type in Keywords.SubroutineDec, f'keyword {routine_type} not expected here'
        self.printToken()

        # return type
        self.tokenizer.advance()
        assert self.tokenizer.token_type() in [TokenTypes.KEYWORD.value, TokenTypes.IDENTIFIER.value], 'Expected a keyword or identifier'
        return_type = self.tokenizer.keyword()
        assert return_type == 'void' or return_type in VarTypes or self.tokenizer.token_type() == TokenTypes.IDENTIFIER.value, 'Expected void or variable type'
        self.printToken()

        # routine name
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Expected an identifier'
        self.printToken()

        # opening parenthesis
        self.tokenizer.advance()
        assert self.tokenizer.token_type(
        ) == TokenTypes.SYMBOL and self.tokenizer.symbol() == '(', 'Expected \'(\''
        self.printToken()

        # paramter list
        self.tokenizer.advance()
        self.compile_parameter_list()

        # closing parenthesis
        assert self.tokenizer.token_type(
        ) == TokenTypes.SYMBOL and self.tokenizer.symbol() == ')', 'Expected \'(\''
        self.printToken()

        # routine's body
        # opening parenthesis
        self.tokenizer.advance()
        assert self.tokenizer.token_type(
        ) == TokenTypes.SYMBOL and self.tokenizer.symbol() == '{', 'Expected \'(\''
        self.printOpening('subroutineBody')
        self.printToken()

        # varDec
        self.tokenizer.advance()

        while self.tokenizer.token_type() == TokenTypes.KEYWORD and self.tokenizer.keyword() in Keywords.VarDec:
            self.compile_var_dec()

        # statements
        self.compile_statements()

        # closing parenthesis
        assert self.tokenizer.token_type(
        ) == TokenTypes.SYMBOL and self.tokenizer.symbol() == '}', 'Expected \'}\''
        self.printToken()
        self.printClosing('subroutineBody')
        self.printClosing('subroutineDec')
        self.tokenizer.advance()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.printOpening('parameterList')

        if self.tokenizer.symbol() != ')':
            # type
            assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Keyword expected'
            param_type = self.tokenizer.keyword()
            assert param_type in VarTypes, f'Unknown type {param_type}'
            self.printToken()

            # name
            self.tokenizer.advance()
            assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
            param_name = self.tokenizer.identifier()
            self.printToken()

            self.tokenizer.advance()
            while True:
                if self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == ')':
                    break

                # ,
                assert self.tokenizer.token_type(
                ) == TokenTypes.SYMBOL and self.tokenizer.symbol() == ',', '\',\' expected'
                self.printToken()
                self.tokenizer.advance()

                # type
                assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Keyword expected'
                param_type = self.tokenizer.keyword()
                assert param_type in VarTypes, f'Unknown type {param_type}'
                self.printToken()

                # name
                self.tokenizer.advance()
                assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
                param_name = self.tokenizer.identifier()
                self.printToken()
                self.tokenizer.advance()

        self.printClosing('parameterList')

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.printOpening('varDec')

        # var
        assert self.tokenizer.token_type() == TokenTypes.KEYWORD and self.tokenizer.token_value(
        ) in Keywords.VarDec, '\'var\' expected'
        self.printToken()
        self.tokenizer.advance()

        # type
        assert self.tokenizer.token_type() in {
            TokenTypes.KEYWORD.value, TokenTypes.IDENTIFIER.value}, 'keyword or identifier expected'
        if self.tokenizer.token_type() == TokenTypes.KEYWORD:
            assert self.tokenizer.token_value(
            ) in VarTypes, f'Unknown var type {self.tokenizer.token_value()}'
        self.printToken()

        # name
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
        self.printToken()

        self.tokenizer.advance()

        while True:
            if self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == ';':
                break

            # ,
            assert self.tokenizer.token_type(
            ) == TokenTypes.SYMBOL and self.tokenizer.symbol() == ',', '\',\' expected'
            self.printToken()

            # name
            self.tokenizer.advance()
            assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
            self.printToken()

            self.tokenizer.advance()

        # ;
        assert self.tokenizer.token_type(
        ) == TokenTypes.SYMBOL and self.tokenizer.token_value() == ';', '\';\' expected'
        self.printToken()
        self.printClosing('varDec')
        self.tokenizer.advance()

    def printToken(self):
        self.out.write('  '*self.tab_counter + self.tokenizer.cur_token_toString() + '\n')
        # print('  '*self.tab_counter + self.tokenizer.cur_token_toString() )

    def printOpening(self, name):
        self.out.write('  '*self.tab_counter + f"<{name}>\n")
        # print('  '*self.tab_counter + f"<{name}>")
        self.tab_counter += 1

    def printClosing(self, name):
        self.tab_counter -= 1
        # print('  '*self.tab_counter + f"</{name}>")
        self.out.write('  '*self.tab_counter + f"</{name}>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        assert (self.tokenizer.token_type() == TokenTypes.KEYWORD and self.tokenizer.keyword(
        ) in Keywords.Statements) or self.tokenizer.token_value() == '}', 'Statement expected'
        self.printOpening('statements')

        while self.tokenizer.token_type() == TokenTypes.KEYWORD and self.tokenizer.keyword() in Keywords.Statements:
            if self.tokenizer.keyword() == Keywords.Statements.LET:
                # let statement
                self.compile_let()
            elif self.tokenizer.keyword() == Keywords.Statements.IF:
                # if statement
                self.compile_if()
            elif self.tokenizer.keyword() == Keywords.Statements.WHILE:
                # while statement
                self.compile_while()
            elif self.tokenizer.keyword() == Keywords.Statements.DO:
                # do statement
                self.compile_do()
            elif self.tokenizer.keyword() == Keywords.Statements.RETURN:
                # return statement
                self.compile_return()

        self.printClosing('statements')

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.printOpening('doStatement')
        assert self.tokenizer.token_value() == Keywords.Statements.DO, 'do expected'
        self.printToken()
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'identifier expected'
        self.printToken()
        self.tokenizer.advance()

        assert self.tokenizer.token_value() in ['.', '('], '. or ( expected'
        
        if self.tokenizer.token_value() == '.':
            # it's (className|varName).subroutineName(expressionList)
            self.printToken() # print .
            self.tokenizer.advance()
            assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
            self.printToken() # print subroutineName
            self.tokenizer.advance()
            assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == '(', '\'(\' expected'

        # now only has to print (expressionList)
        self.printToken() # print (
        self.tokenizer.advance()
        self.compile_expression_list()
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == ')', '\')\' expected'
        self.printToken()
        self.tokenizer.advance()

        assert self.tokenizer.token_value() == ';', '; expected'
        self.printToken()
        self.tokenizer.advance()

        self.printClosing('doStatement')

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.printOpening('letStatement')
        # let
        assert self.tokenizer.token_type() == TokenTypes.KEYWORD and self.tokenizer.keyword(
        ) == Keywords.Statements.LET, 'let expected'
        self.printToken()

        # name
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
        self.printToken()

        # [ or =
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() in {
            '[', '='}, '\'=\' or \'[\' expected'

        if self.tokenizer.symbol() == '[':
            self.printToken()
            self.tokenizer.advance()

            # expression
            self.compile_expression()

            # ]
            assert self.tokenizer.token_type(
            ) == TokenTypes.SYMBOL and self.tokenizer.symbol() == ']', '\']\' expected'
            self.printToken()

            # =
            self.tokenizer.advance()
            assert self.tokenizer.token_type(
            ) == TokenTypes.SYMBOL and self.tokenizer.symbol() == '=', '\'=\' expected'

        # print =
        self.printToken()

        self.tokenizer.advance()

        # expression
        self.compile_expression()

        # ;
        assert self.tokenizer.token_type(
        ) == TokenTypes.SYMBOL and self.tokenizer.symbol() == ';', '\';\' expected'
        self.printToken()

        self.printClosing('letStatement')
        self.tokenizer.advance()

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.printOpening('whileStatement')
        
        assert self.tokenizer.token_value() == Keywords.Statements.WHILE, 'while expected'
        self.printToken()
        self.tokenizer.advance()
        assert self.tokenizer.token_value() == '(', '( expected'
        self.printToken()
        self.tokenizer.advance()
        self.compile_expression()
        assert self.tokenizer.token_value() == ')', ') expected'
        self.printToken()
        self.tokenizer.advance()
        assert self.tokenizer.token_value() == '{', '{ expected'
        self.printToken()
        self.tokenizer.advance()
        self.compile_statements()
        assert self.tokenizer.token_value() == '}', '} expected'
        self.printToken()
        self.tokenizer.advance()
        self.printClosing('whileStatement')

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.printOpening('returnStatement')
        
        assert self.tokenizer.token_value() == Keywords.Statements.RETURN, 'return expected'
        self.printToken()
        self.tokenizer.advance()

        if self.tokenizer.token_value() != ';':
            self.compile_expression()

        assert self.tokenizer.token_value() == ';', '; expected'
        self.printToken()
        self.tokenizer.advance()

        self.printClosing('returnStatement')

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        """ - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                statements '}')?"""
        self.printOpening('ifStatement')

        tokenizer = self.tokenizer
        self.printToken()

        self.tokenizer.advance()
        assert tokenizer.token_type(
        ) == "SYMBOL", f"Expected to get SYMBOL, instead got {tokenizer.token_type()}"
        assert tokenizer.symbol(
        ) == "(", f"Expected to get (, instead got {tokenizer.symbol()}"
        self.printToken()

        tokenizer.advance()
        self.compile_expression()

        assert tokenizer.token_type(
        ) == "SYMBOL", f"Expected to get SYMBOL, instead got {tokenizer.token_type()}"
        assert tokenizer.symbol(
        ) == ")", f"Expected to get ), instead got {tokenizer.symbol()}"
        self.printToken()

        tokenizer.advance()
        assert tokenizer.token_type(
        ) == "SYMBOL", f"Expected to get SYMBOL, instead got {tokenizer.token_type()}"
        assert tokenizer.symbol(
        ) == "{", f"Expected to get {{, instead got {tokenizer.symbol()}"
        self.printToken()

        tokenizer.advance()
        self.compile_statements()

        assert tokenizer.token_type(
        ) == "SYMBOL", f"Expected to get SYMBOL, instead got {tokenizer.token_type()}"
        assert tokenizer.symbol(
        ) == "}", f"Expected to get }}, instead got {tokenizer.symbol()}"
        self.printToken()

        tokenizer.advance()
        if tokenizer.token_type() == "KEYWORD" and tokenizer.keyword() == "else":
            self.printToken()

            tokenizer.advance()
            assert tokenizer.token_type(
            ) == "SYMBOL", f"Expected to get SYMBOL, instead got {tokenizer.token_type()}"
            assert tokenizer.symbol(
            ) == "{", f"Expected to get {{, instead got {tokenizer.symbol()}"
            self.printToken()

            tokenizer.advance()
            self.compile_statements()

            assert tokenizer.token_type(
            ) == "SYMBOL", f"Expected to get SYMBOL, instead got {tokenizer.token_type()}"
            assert tokenizer.symbol(
            ) == "}", f"Expected to get }}, instead got {tokenizer.symbol()}"
            self.printToken()
            tokenizer.advance()


        self.printClosing('ifStatement')

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.printOpening('expression')

        # self.tokenizer.advance()
        # term
        self.compile_term()

        # (op term)*
        while self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() in Operations:
            # print op
            self.printToken()

            # term
            self.tokenizer.advance()
            self.compile_term()

        self.printClosing('expression')

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
        self.printOpening('term')

        token_t = self.tokenizer.token_type()
        token = self.tokenizer.token_value()

        self.printToken()
        self.tokenizer.advance()
        
        # integer, string, keyword Constatnt had already been handeled
        if token_t == TokenTypes.SYMBOL and token == '(':
            # expression
            self.compile_expression()

            # )
            assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == ')', '\')\' expected'
            self.printToken()
            self.tokenizer.advance()
        elif token in UnaryOperations:
            # term
            self.compile_term()
        elif token_t == TokenTypes.IDENTIFIER:
            # we need to look forward
            next_token_t = self.tokenizer.token_type()
            next_token = self.tokenizer.token_value()

            if next_token_t == TokenTypes.SYMBOL and next_token == '[':
                # it's a term of type 'varName [expression]'
                self.printToken() # print [
                
                self.tokenizer.advance()
                self.compile_expression() 

                assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == ']', '\']\' expected'
                self.printToken()
                self.tokenizer.advance()
            elif next_token_t == TokenTypes.SYMBOL and (next_token == '(' or next_token == '.'):
                # it's a term of type subroutineCall
                if next_token == '.':
                    # it's (className|varName).subroutineName(expressionList)
                    self.printToken() # print .
                    self.tokenizer.advance()
                    assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
                    self.printToken() # print subroutineName
                    self.tokenizer.advance()
                    assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == '(', '\'(\' expected'

                # now only has to print (expressionList)
                self.printToken() # print (
                self.tokenizer.advance()
                self.compile_expression_list()
                assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == ')', '\')\' expected'
                self.printToken()
                self.tokenizer.advance()

            else:
                # it's just a varName, no further action needed
                pass

        
        self.printClosing('term')

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.printOpening('expressionList')
        if self.tokenizer.token_value() != ')':
            self.compile_expression()

            while self.tokenizer.token_value() == ',':
                self.printToken()
                self.tokenizer.advance()
                self.compile_expression()
        self.printClosing('expressionList')
        
