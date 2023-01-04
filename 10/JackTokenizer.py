"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Will be defined later
        self.token_list = None
        self.token = None

        # Constants
        self.keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char',
                         'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while',
                         'return']

        self.symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
        self.escaped_symbols = [f"\\{sym}" for sym in self.symbols]
        self.set_lines(input_stream.read())

        self.index = 0
        self.len = len(self.token_list)
        self.write_xml()

    def set_lines(self, input_stream):
        seperator = "\\b"
        # Remove comments.
        input_stream = re.sub(r"(\/\/)([^\n\r]+)(\n||\r)", "", input_stream)
        input_stream = re.sub(r"(\/\*{1,2})(.*?)(\*\/)", "", input_stream)
        input_stream = re.sub(r"(\n|\r)\s*(\n|\r)", "", input_stream)
        input_stream = re.sub(r"(\n|\r)", "", input_stream)  # TODO: what happens if string has linebreak?
        input_stream = re.sub(r"(\t)", "", input_stream)

        for sym in self.symbols:
            input_stream = re.sub(f"(\{sym})", f" {sym} ", input_stream)


        regex_rule = f"({seperator}" + f"{seperator}|{seperator}".join(self.keywords) + f"{seperator}|" + f"|".join(
            self.escaped_symbols) + f"{seperator})"
        lines = re.split(regex_rule, input_stream)

        suspected_token_list = []
        for line in lines:
            if not re.match("^\s*$", line):
                suspected_token_list.append(re.sub("(^\s*)|(\s*$)", "", line))

        self.token_list = []
        for token in suspected_token_list:
            if not re.match(r".*\s.*", token) or re.match(r".*\".*", token):
                self.token_list.append(token)
                continue

            self.token_list.extend(re.split(r"\s", token))

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        return self.index < self.len

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        self.token = self.token_list[self.index]
        self.index += 1

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        if self.token in self.keywords:
            return "KEYWORD"
        if self.token in self.symbols:
            return "SYMBOL"
        if re.match("^\d*$", self.token):
            return "INT_CONST"
        if re.match("^\".*\"$", self.token):
            return "STRING_CONST"
        return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        return self.token

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        replace_dic = {"<": "&lt;", ">": "&gt;"}
        if self.token in replace_dic:
            return replace_dic[self.token]
        return self.token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        # Your code goes here!
        return self.token

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        return self.token

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        return self.token

    def token_value(self):
        if self.token_type() == "KEYWORD":
            return self.keyword()
        if self.token_type() == "SYMBOL":
            return self.symbol().lower()
        if self.token_type() == "IDENTIFIER":
            return self.identifier()
        if self.token_type() == "INT_CONST":
            return self.int_val()
        if self.token_type() == "STRING_CONST":
            return re.sub("\"", "", self.string_val())

    def cur_token_type_toString(self):
        return {"KEYWORD": "keyword", "SYMBOL": "symbol", "INT_CONST": "integerConstant",
                "STRING_CONST": "stringConstant", "IDENTIFIER": "identifier"}[self.token_type()]

    def cur_token_toString(self):
        return f"<{self.cur_token_type_toString()}> {self.token_value()} </{self.cur_token_type_toString()}>"

    def write_xml(self):
        with open("Test_output.xml", "w") as f:
            f.write("<tokens>\n")
            while self.has_more_tokens():
                self.advance()

                f.write(f"{self.cur_token_toString()}\n")
            f.write("<\\tokens>\n")
