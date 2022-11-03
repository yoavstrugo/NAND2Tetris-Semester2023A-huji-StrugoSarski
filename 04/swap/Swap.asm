// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.
//Go through all the stuffs keeping in mind MIN MAX MIN_POINTER MAX_POINTER
@R14
D=M
@CUR
M=D

@R15
D=D+M
@END
M=D

// Start values
@R14
D=M
@MIN_POINTER
M=D

@MAX_POINTER
M=D

A=D
D=M
@MIN
M=D

@MAX
M=D

// First increment
@CUR
M=M+1

(LOOP)
@END
D=M
@CUR
D=D-M
@FINISH
D; JEQ

//Check if [cur] is bigger then max value
@CUR
A=M
D=M
@MAX
D=D-M
@FOUND_MAX
D; JGE

//Check if [cur] is smaller then min value
@CUR
A=M
D=M
@MIN
D=D-M
@FOUND_MIN
D; JLT


// Increment
(INCREMENT)
@CUR
M=M+1
@LOOP
A; JMP
// Check if we've reached the end.


(FINISH)
@MAX
D=M
@MIN_POINTER
A=M

M=D

@MIN
D=M
@MAX_POINTER
A=M

M=D


(BLACK_HOLE)
@BLACK_HOLE
0; JMP


(FOUND_MAX)
// Swap MAX_POINTER
@CUR
D=M
@MAX_POINTER
M=D

//Swap MAX
A=D
D=M
@MAX
M=D
@INCREMENT
0; JMP

(FOUND_MIN)
// Swap MIN_POINTER
@CUR
D=M
@MIN_POINTER
M=D

//Swap MIN
A=D
D=M
@MIN
M=D
@INCREMENT
0; JMP