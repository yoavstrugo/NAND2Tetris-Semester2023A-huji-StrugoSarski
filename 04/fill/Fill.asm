// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// This program illustrates low-level handling of the screen and keyboard
// devices, as follows.
//
// The program runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
// 
// Assumptions:
// Your program may blacken and clear the screen's pixels in any spatial/visual
// Order, as long as pressing a key continuously for long enough results in a
// fully blackened screen, and not pressing any key for long enough results in a
// fully cleared screen.
//
// Test Scripts:
// For completeness of testing, test the Fill program both interactively and
// automatically.
// 
// The supplied FillAutomatic.tst script, along with the supplied compare file
// FillAutomatic.cmp, are designed to test the Fill program automatically, as 
// described by the test script documentation.
//
// The supplied Fill.tst script, which comes with no compare file, is designed
// to do two things:
// - Load the Fill.hack program
// - Remind you to select 'no animation', and then test the program
//   interactively by pressing and releasing some keyboard keys

// Put your code here.

// Blank the screen
(BLANK)
    @i // i refers to some mem. location.
    M=0 // i=0
(LOOP1)
    @i
    D=M // D=i
    @8192 // screen size is 8192
    D=D-A // D=i-100
    @CHCKFORKEY1
    D;JGT // If (i-100)>0 goto END
    @i
    D=M // D=i
    @SCREEN
    A=A+D
    M=0 // Set the color to white
    @i
    M=M+1 // i=i+1
    @LOOP1
    0;JMP // Goto LOOP

// Wait until key is pressed
(CHCKFORKEY1)
    // Check if a key has been pressed (keyboard word is not zero)
    @KBD // Keyboard address
    D=M // Put the keyboard 'output' into D
    @CHCKFORKEY1
    D;JEQ

// Fill the screen
(FILL)
    @i // i refers to some mem. location.
    M=0 // i=0
(LOOP2)
    @i
    D=M // D=i
    @8192 // screen size is 8192
    D=D-A // D=i-100
    @CHCKFORKEY2
    D;JGT // If (i-100)>0 goto END
    @i
    D=M // D=i
    @SCREEN
    A=A+D
    M=-1 // Set the color to black
    @i
    M=M+1 // i=i+1
    @LOOP2
    0;JMP // Goto LOOP

// Wait until key is released
(CHCKFORKEY2)
    // Check if a key has been pressed (keyboard word is not zero)
    @KBD // Keyboard address
    D=M // Put the keyboard 'output' into D
    @CHCKFORKEY2
    D;JNE

    @BLANK
    0;JMP

(END)
    @END
    0;JMP // Infinite loop