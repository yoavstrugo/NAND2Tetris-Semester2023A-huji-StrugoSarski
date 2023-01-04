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

class TokenTypes(MyEnum, metaclass=MyEnumMeta):
    IDENTIFIER = 'IDENTIFIER'
    SYMBOL = 'SYMBOL'
    KEYWORD = 'KEYWORD'

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
        print('\t'*self.tab_counter +"<class>\n")
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

        # Class name
        self.tokenizer.advance() 
        assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, f'{self.tokenizer.identifier()} is not a valid identifier'
        className = self.tokenizer.identifier()
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

        # Opening parenthesis
        self.tokenizer.advance() 
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == '{', 'Expected \'{\' after class decleration' + f' {className}'
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

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
                pass
            elif keyword in Keywords.SubroutineDec:
                # continue to next loop to compile subroutines
                break

            self.tokenizer.advance() 
        
        # Subroutines compilation
        while True:
            token_type = self.tokenizer.token_type()
            assert token_type in {TokenTypes.KEYWORD.value, TokenTypes.SYMBOL.value}, f'Expected a keyword inside a class, got {self.tokenizer.keyword()}'

            if token_type == TokenTypes.SYMBOL and self.tokenizer.symbol() == '}':
                # closing parenthesis, end of class
                break

            keyword = self.tokenizer.keyword()
            assert keyword in Keywords.SubroutineDec, f'Expected a sub routine decleration, got {keyword}'

            self.compile_subroutine()
            self.tokenizer.advance()
                
        assert token_type == TokenTypes.SYMBOL and self.tokenizer.symbol() == '}', '\}\' expected at the end of class decleration.'
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())
        
        self.tab_counter-=1
        print('\t'*self.tab_counter +"</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        print('\t'*self.tab_counter +"<classVarDec>\n")
        self.tab_counter+=1

        self.tab_counter-=1
        print('\t'*self.tab_counter +"</classVarDec>\n")

        

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        print('\t'*self.tab_counter +"<subroutineDec>\n")
        self.tab_counter += 1

        # routine type
        assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Expected a keyword'
        routine_type = self.tokenizer.keyword()
        assert routine_type in Keywords.SubroutineDec, f'keyword {routine_type} not expected here'
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

        # return type
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Expected a keyword'
        return_type = self.tokenizer.keyword()
        assert return_type == 'void' or return_type in VarTypes, 'Expected void or variable type'
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

        # routine name
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Expected an identifier'
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

        # opening parenthesis
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == '(', 'Expected \'(\''
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

        # paramter list
        self.tokenizer.advance()
        self.compile_parameter_list()

        # closing parenthesis
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == ')', 'Expected \'(\''
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

        # routine's body
        # opening parenthesis
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == '{', 'Expected \'(\''
        print('\t'*self.tab_counter +"<subroutineBody>\n")
        self.tab_counter += 1
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())
        
        # varDec
        self.tokenizer.advance()

        while self.tokenizer.token_type() == TokenTypes.KEYWORD and self.tokenizer.keyword() in Keywords.VarDec:
            self.compile_var_dec()

        # statements
        # TODO

        # closing parenthesis
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == '}', 'Expected \'(\''
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())
        print('\t'*self.tab_counter + "</subroutineBody>\n")
        self.tab_counter -= 1
        print("</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        print('\t'*self.tab_counter +"<parameterList>\n")
        self.tab_counter += 1

        if self.tokenizer.symbol() != ')':
            print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())
            # type
            assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Keyword expected'
            param_type = self.tokenizer.keyword()
            assert param_type in VarTypes, f'Unknown type {param_type}'
            print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())
            
            # name
            self.tokenizer.advance()
            assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
            param_name = self.tokenizer.identifier()
            print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

            while True:
                if self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == ')':
                    break

                # ,
                assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == ',', '\',\' expected'
                print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())
                self.tokenizer.advance()

                # type
                assert self.tokenizer.token_type() == TokenTypes.KEYWORD, 'Keyword expected'
                param_type = self.tokenizer.keyword()
                assert param_type in VarTypes, f'Unknown type {param_type}'
                print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

                # name
                self.tokenizer.advance()
                assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
                param_name = self.tokenizer.identifier()
                print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

        self.tab_counter-=1
        print('\t'*self.tab_counter +"</parameterList>\n")
        

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        
        print('\t'*self.tab_counter +"<varDec>\n")
        self.tab_counter+=1

        # var
        assert self.tokenizer.token_type() == TokenTypes.KEYWORD and self.tokenizer.token_value() in Keywords.VarDec, '\'var\' expected'
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())
        self.tokenizer.advance()

        # type
        assert self.tokenizer.token_type() in {TokenTypes.KEYWORD.value, TokenTypes.IDENTIFIER.value}, 'keyword or identifier expected'
        if self.tokenizer.token_type() == TokenTypes.KEYWORD:
            assert self.tokenizer.token_value() in VarTypes, f'Unknown var type {self.tokenizer.token_value()}'
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

        # name
        self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

        self.tokenizer.advance()

        while True:
            if self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == ';':
                break
            
            # ,
            assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.symbol() == ',', '\',\' expected'
            print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

            # name
            self.tokenizer.advance()
            assert self.tokenizer.token_type() == TokenTypes.IDENTIFIER, 'Identifier expected'
            print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())

            self.tokenizer.advance()

                

        # ;
        assert self.tokenizer.token_type() == TokenTypes.SYMBOL and self.tokenizer.token_value() == ';', '\';\' expected'
        print('\t'*self.tab_counter + self.tokenizer.cur_token_toString())
        self.tab_counter-=1
        print('\t'*self.tab_counter +"</varDec>\n")
        self.tokenizer.advance()

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        pass

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        print('\t'*self.tab_counter +"<doStatement>")
        print('\t'*self.tab_counter +"</doStatement>")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        print('\t'*self.tab_counter +"<letStatement>")
        print('\t'*self.tab_counter +"</letStatement>")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        print('\t'*self.tab_counter +"<whileStatement>")
        print('\t'*self.tab_counter +"</whileStatement>")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        print('\t'*self.tab_counter +"<returnStatement>")
        print('\t'*self.tab_counter +"</returnStatement>")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        print('\t'*self.tab_counter +"<ifStatement>")
        print('\t'*self.tab_counter +"</ifStatement>")
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
        print('\t'*self.tab_counter +"<term>")
        print('\t'*self.tab_counter +"</term>")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        pass
