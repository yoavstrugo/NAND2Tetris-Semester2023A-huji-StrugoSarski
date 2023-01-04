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
        return self.name == other

class TokenTypes(MyEnum, metaclass=MyEnumMeta):
    IDENTIFIER = 'IDENTIFIER',
    SYMBOL = 'SYMBOL',
    KEYWORD = 'KEYWORD'

class VarTypes(MyEnum, metaclass=MyEnumMeta):
    INT = 'INT',
    CHAR = 'CHAR',
    BOOLEAN = 'BOOLEAN'

class Keywords(MyEnum, metaclass=MyEnumMeta):
    class ClassDecVar(MyEnum, metaclass=MyEnumMeta):
        STATIC = 'STATIC',
        FIELD = 'FIELD'
    class SubroutineDec(MyEnum, metaclass=MyEnumMeta):
        CONSTURCTOR = 'CONSTURCTOR',
        FUNCTION = 'FUNCTION',
        METHOD = 'METHOD'
    class VarDec(MyEnum, metaclass=MyEnumMeta):
        VAR = 'VAR'

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
        self.out.write('\t'*self.tab_counter +"<class>\n")
        self.out.write('\t'*self.tab_counter +'<keyword> class </keyword>\n')

        # Class name
        self.tokenizer.advance() 
        assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, f'{self.tokenizer.identifier()} is not a valid identifier'
        className = self.tokenizer.identifier()
        self.out.write('\t'*self.tab_counter + f'<identifier> {className} </identifier>\n')

        # Opening parenthesis
        self.tokenizer.advance() 
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == '{', 'Expected \'{\' after class decleration' + f' {className}'
        self.out.write('\t'*self.tab_counter +'<symbol> { </symbol>\n')

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
                self.tab_counter+=1
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

            self.tab_counter+=1
            self.compile_subroutine()
            self.tokenizer.advance()
                
        assert token_type == TokenTypes.SYMBOL and self.tokenizer.symbol() == '}', '\}\' expected at the end of class decleration.'
        self.out.write('\t'*self.tab_counter +'<symbol> } </symbol>\n')
        

        self.out.write('\t'*self.tab_counter +"</class>\n")
        self.tab_counter-=1

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.out.write('\t'*self.tab_counter +"<classVarDec>\n")

        self.out.write('\t'*self.tab_counter +"</classVarDec>\n")

        self.tab_counter-=1

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.out.write('\t'*self.tab_counter +"<subroutineDec>\n")

        # routine type
        assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Expected a keyword'
        routine_type = self.tokenizer.keyword()
        assert routine_type in Keywords.SubroutineDec, f'keyword {routine_type} not expected here'
        self.out.write('\t'*self.tab_counter +f"<keyword> {routine_type.lower()} </keyword>\n")

        # return type
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Expected a keyword'
        return_type = self.tokenizer.keyword()
        assert return_type == 'VOID' or return_type in VarTypes
        self.out.write('\t'*self.tab_counter +f"<keyword> {return_type.lower()} </keyword>\n")

        # routine name
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Expected an identifier'
        routine_name = self.tokenizer.identifier()
        self.out.write('\t'*self.tab_counter +f"<identifier> {routine_name} </identifier>\n")

        # opening parenthesis
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol == '(', 'Expected \'(\''
        self.out.write('\t'*self.tab_counter +f"<symbol> ( </symbol>\n")

        # paramter list
        self.tokenizer.advance()
        self.tab_counter+=1
        self.compile_parameter_list()

        # closing parenthesis
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol == ')', 'Expected \'(\''
        self.out.write('\t'*self.tab_counter +f"<symbol> ) </symbol>\n")

        # routine's body
        # opening parenthesis
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol == '{', 'Expected \'(\''
        self.out.write('\t'*self.tab_counter +"<subroutineBody>\n")
        self.out.write('\t'*self.tab_counter +"<symbol> { </symbol>\n")

        # varDec
        # TODO

        # closing parenthesis
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol == '}', 'Expected \'(\''
        self.out.write('\t'*self.tab_counter +"<symbol> } </symbol>\n")
        self.out.write('\t'*self.tab_counter +"</subroutineBody>\n")
        self.out.write("</subroutineDec>\n")

        self.tab_counter-=1

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.out.write('\t'*self.tab_counter +"<parameterList>\n")

        if self.tokenizer.token_type() != TokenTypes.SYMBOL and self.tokenizer.symbol == ')':
            # type
            assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Keyword expected'
            param_type = self.tokenizer.keyword()
            assert param_type in VarTypes, f'Unknown type {param_type}'
            self.out.write('\t'*self.tab_counter +f"<keyword> {param_type.lower()} </keyword>\n")

            # name
            self.tokenizer.advance()
            assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
            param_name = self.tokenizer.identifier()
            self.out.write('\t'*self.tab_counter +f"<identifier> {param_name} </identifier>\n")

            while True:
                if self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol == ')':
                    break

                # ,
                assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol == ',', '\',\' expected'
                self.out.write('\t'*self.tab_counter +f"<symbol> , </symbol>\n")
                self.tokenizer.advance()

                # type
                assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Keyword expected'
                param_type = self.tokenizer.keyword()
                assert param_type in VarTypes, f'Unknown type {param_type}'
                self.out.write('\t'*self.tab_counter +f"<keyword> {param_type.lower()} </keyword>\n")

                # name
                self.tokenizer.advance()
                assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
                param_name = self.tokenizer.identifier()
                self.out.write('\t'*self.tab_counter +f"<identifier> {param_name} </identifier>\n")

        self.out.write('\t'*self.tab_counter +"</parameterList>\n")
        self.tab_counter-=1

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.out.write('\t'*self.tab_counter +"<varDec>\n")
        self.out.write('\t'*self.tab_counter +"</varDec>\n")
        self.tab_counter-=1

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        pass

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.out.write('\t'*self.tab_counter +"<doStatement>")
        self.out.write('\t'*self.tab_counter +"</doStatement>")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.out.write('\t'*self.tab_counter +"<letStatement>")
        self.out.write('\t'*self.tab_counter +"</letStatement>")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.out.write('\t'*self.tab_counter +"<whileStatement>")
        self.out.write('\t'*self.tab_counter +"</whileStatement>")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.out.write('\t'*self.tab_counter +"<returnStatement>")
        self.out.write('\t'*self.tab_counter +"</returnStatement>")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        """ - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                statements '}')?"""
        tokenizer = self.tokenizer
        self.out.write("<ifStatement>")
        self.out.write(tokenizer.cur_token_toString())

        assert tokenizer.token_type() == "SYMBOL", f"Expected to get SYMBOL, instead got {tokenizer.token_type()}"
        assert tokenizer.symbol() == "(", f"Expected to get (, instead got {tokenizer.symbol()}"
        self.out.write(tokenizer.cur_token_toString())

        tokenizer.advance()
        self.compile_expression()

        assert tokenizer.token_type() == "SYMBOL", f"Expected to get SYMBOL, instead got {tokenizer.token_type()}"
        assert tokenizer.symbol() == ")", f"Expected to get ), instead got {tokenizer.symbol()}"
        self.out.write(tokenizer.cur_token_toString())

        tokenizer.advance()
        assert tokenizer.token_type() == "SYMBOL", f"Expected to get SYMBOL, instead got {tokenizer.token_type()}"
        assert tokenizer.symbol() == "{", f"Expected to get {{, instead got {tokenizer.symbol()}"
        self.out.write(tokenizer.cur_token_toString())

        tokenizer.advance()
        self.compile_statements()

        tokenizer.advance()
        assert tokenizer.token_type() == "SYMBOL", f"Expected to get SYMBOL, instead got {tokenizer.token_type()}"
        assert tokenizer.symbol() == "}", f"Expected to get }}, instead got {tokenizer.symbol()}"
        self.out.write(tokenizer.cur_token_toString())

        tokenizer.advance()
        if tokenizer.token_type() == "KEYWORD" and tokenizer.keyword() == "else":
            self.out.write(tokenizer.cur_token_toString())

            tokenizer.advance()
            assert tokenizer.token_type() == "SYMBOL", f"Expected to get SYMBOL, instead got {tokenizer.token_type()}"
            assert tokenizer.symbol() == "{", f"Expected to get {{, instead got {tokenizer.symbol()}"
            self.out.write(tokenizer.cur_token_toString())

            tokenizer.advance()
            self.compile_statements()

            tokenizer.advance()
            assert tokenizer.token_type() == "SYMBOL", f"Expected to get SYMBOL, instead got {tokenizer.token_type()}"
            assert tokenizer.symbol() == "{", f"Expected to get {{, instead got {tokenizer.symbol()}"
            self.out.write(tokenizer.cur_token_toString())

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
        self.out.write('\t'*self.tab_counter +"<term>")
        self.out.write('\t'*self.tab_counter +"</term>")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        pass
