@codeStart
0; JMP
(eq)                             
	@SP                             
	A=M                             
	A=A-1                             
	D=M                             
	A=A-1                             
	D=D-M                             
	@neg1                             
	D; JEQ                             
	@pos0                             
	D; JNE
(lt)                                      
	@SP                                      
	A=M                                      
	A=A-1                                      
	D=M                                      
	A=A-1                                      
	D=M-D                                      
	@neg1                                      
	D; JLT                                      
	@pos0                                      
	D; JMP
(gt)                                      
	@SP                                      
	A=M                                      
	A=A-1                                      
	D=M                                      
	A=A-1                                      
	D=M-D                                      
	@neg1                                      
	D; JGT                                      
	@pos0                                      
	D; JMP
(neg1)                 
	D=-1                 
	@END_EQ_LT_GT                 
	0; JMP                 
(pos0)                 
	D=0                 
	@END_EQ_LT_GT                 
	0; JMP
(END_EQ_LT_GT)                 
	@SP                 
	M=M-1 // Decrease SP by 1                
	A=M                 
	A=A-1                 
	M=D // Push D to the stack                 
	@R13                 
	A=M                 
	0; JMP
(codeStart)

// BOOTSTRAP
// SP=256
@256
D=A
@SP
M=D

// call Sys.init
// Push return address
    @.$ret.0
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push LCL
    @LCL
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push ARG
    @ARG
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push THIS address
    @THIS
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push THAT address
    @THAT
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // ARG = SP-5-n_args
    @SP
    D=M
    @5
    D=D-A
    @0
    D=D-A
    @ARG
    M=D
    
    // LCL = SP
    @SP
    D=M
    @LCL
    M=D
    
    @Sys.init
    0; JMP
    (.$ret.0)

// function Main.fibonacci
(Main.fibonacci)
//C_PUSH argument 0
@ARG                         
	D=M // D now has the base                         
	@0 // index                         
	A=A+D // A now has the value's address                         
	D=M // D now has the value it self                         
                        
	@SP                         
	A=M // A has the address of the next slot in the stack                         
	M=D // Put the value into the next stack's slot                         
	@SP                         
	M=M+1 // Increase SP by 1
//C_PUSH constant 2
@2                                 
	D=A                                 
	@SP                                 
	A=M                                 
	M=D                                 
	@SP                                 
	M=M+1
//lt
@label_0_lt                   
	D=A                   
	@R13                   
	M=D                   
	@lt                   
	0;JMP                   
	(label_0_lt)
// if-goto IF_TRUE

    @SP
    A=M
    A=A-1
    D=M
    (Main.Main.fibonacci$IF_TRUE)
    D; JNE

// goto IF_FALSE
@Main.Main.fibonacci$IF_FALSE
0; JMP
// label IF_TRUE
(Main.Main.fibonacci$IF_TRUE)//C_PUSH argument 0
@ARG                         
	D=M // D now has the base                         
	@0 // index                         
	A=A+D // A now has the value's address                         
	D=M // D now has the value it self                         
                        
	@SP                         
	A=M // A has the address of the next slot in the stack                         
	M=D // Put the value into the next stack's slot                         
	@SP                         
	M=M+1 // Increase SP by 1
// ret

    // ====== frame = LCL
    @LCL // A = &LCL
    D=M // D = LCL
    @R15
    M=D // frame = *R15 = LCL

    // ====== R14 = return_address = *(frame-5)
    @5
    D=A // D=5

    @R15
    A=M // A = frame
    A=A-D // A = frame-5, M = *(frame-5)
    D=M // D = *(frame-5)
    @R14
    M=D // R14 = *(frame-5)

    // ====== *ARG = pop()
    @SP
    M=M-1
    A=M // A = sp
    D=M // D = *sp
    @ARG
    M=D // *ARG = pop()

    // ====== SP = ARG + 1
    D=A // D = ARG
    D=D+1 // D= ARG + 1
    @SP
    M=D // SP = ARG + 1

    // ====== THAT = *(frame-1)
    @1 // A = 1
    D=A // D = 1
    @R15 // M=LCL = frame
    A=M // A=LCL = frame
    A=A-D // A=frame-1, M=*(frame-1)
    D=M // D=*(frame-1)
    @THAT
    M=D // THAT=*(frame-1)

    // ====== THIS = *(frame-2)
    @2 // A = 2
    D=A // D = 2
    @R15 // M=LCL = frame
    A=M // A=LCL = frame
    A=A-D // A=frame-2, M=*(frame-2)
    D=M // D=*(frame-2)
    @THIS
    M=D // THIS=*(frame-2)

    // ====== ARG = *(frame-3)
    @3 // A = 3
    D=A // D = 3
    @R15 // M=LCL = frame
    A=M // A=LCL = frame
    A=A-D // A=frame-3, M=*(frame-3)
    D=M // D=*(frame-3)
    @ARG
    M=D // ARG=*(frame-3)

    // ====== LCL = *(frame-4)
    @4 // A = 4
    D=A // D = 4
    @R15 // M=LCL = frame
    A=M // A=LCL = frame
    A=A-D // A=frame-4, M=*(frame-4)
    D=M // D=*(frame-4)
    @LCL
    M=D // LCL=*(frame-4)

    // ====== goto return_address
    @R14 // A = return_address
    0; JMP

// label IF_FALSE
(Main.Main.fibonacci$IF_FALSE)//C_PUSH argument 0
@ARG                         
	D=M // D now has the base                         
	@0 // index                         
	A=A+D // A now has the value's address                         
	D=M // D now has the value it self                         
                        
	@SP                         
	A=M // A has the address of the next slot in the stack                         
	M=D // Put the value into the next stack's slot                         
	@SP                         
	M=M+1 // Increase SP by 1
//C_PUSH constant 2
@2                                 
	D=A                                 
	@SP                                 
	A=M                                 
	M=D                                 
	@SP                                 
	M=M+1
//sub
@SP                   
	M=M-1 // Point to the top of the stack (y)                   
	A=M // A points to the next slot                   
	D=M // D is one of the values (y)                   
	A=A-1 // A points to next value (x)                   
	M=M-D // Preform the operation, x op y
// call Main.fibonacci
// Push return address
    @Main.Main.fibonacci$ret.0
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push LCL
    @LCL
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push ARG
    @ARG
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push THIS address
    @THIS
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push THAT address
    @THAT
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // ARG = SP-5-n_args
    @SP
    D=M
    @5
    D=D-A
    @1
    D=D-A
    @ARG
    M=D
    
    // LCL = SP
    @SP
    D=M
    @LCL
    M=D
    
    @Main.fibonacci
    0; JMP
    (Main.Main.fibonacci$ret.0)

//C_PUSH argument 0
@ARG                         
	D=M // D now has the base                         
	@0 // index                         
	A=A+D // A now has the value's address                         
	D=M // D now has the value it self                         
                        
	@SP                         
	A=M // A has the address of the next slot in the stack                         
	M=D // Put the value into the next stack's slot                         
	@SP                         
	M=M+1 // Increase SP by 1
//C_PUSH constant 1
@1                                 
	D=A                                 
	@SP                                 
	A=M                                 
	M=D                                 
	@SP                                 
	M=M+1
//sub
@SP                   
	M=M-1 // Point to the top of the stack (y)                   
	A=M // A points to the next slot                   
	D=M // D is one of the values (y)                   
	A=A-1 // A points to next value (x)                   
	M=M-D // Preform the operation, x op y
// call Main.fibonacci
// Push return address
    @Main.Main.fibonacci$ret.0
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push LCL
    @LCL
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push ARG
    @ARG
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push THIS address
    @THIS
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push THAT address
    @THAT
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // ARG = SP-5-n_args
    @SP
    D=M
    @5
    D=D-A
    @1
    D=D-A
    @ARG
    M=D
    
    // LCL = SP
    @SP
    D=M
    @LCL
    M=D
    
    @Main.fibonacci
    0; JMP
    (Main.Main.fibonacci$ret.0)

//add
@SP                   
	M=M-1 // Point to the top of the stack (y)                   
	A=M // A points to the next slot                   
	D=M // D is one of the values (y)                   
	A=A-1 // A points to next value (x)                   
	M=M+D // Preform the operation, x op y
// ret

    // ====== frame = LCL
    @LCL // A = &LCL
    D=M // D = LCL
    @R15
    M=D // frame = *R15 = LCL

    // ====== R14 = return_address = *(frame-5)
    @5
    D=A // D=5

    @R15
    A=M // A = frame
    A=A-D // A = frame-5, M = *(frame-5)
    D=M // D = *(frame-5)
    @R14
    M=D // R14 = *(frame-5)

    // ====== *ARG = pop()
    @SP
    M=M-1
    A=M // A = sp
    D=M // D = *sp
    @ARG
    M=D // *ARG = pop()

    // ====== SP = ARG + 1
    D=A // D = ARG
    D=D+1 // D= ARG + 1
    @SP
    M=D // SP = ARG + 1

    // ====== THAT = *(frame-1)
    @1 // A = 1
    D=A // D = 1
    @R15 // M=LCL = frame
    A=M // A=LCL = frame
    A=A-D // A=frame-1, M=*(frame-1)
    D=M // D=*(frame-1)
    @THAT
    M=D // THAT=*(frame-1)

    // ====== THIS = *(frame-2)
    @2 // A = 2
    D=A // D = 2
    @R15 // M=LCL = frame
    A=M // A=LCL = frame
    A=A-D // A=frame-2, M=*(frame-2)
    D=M // D=*(frame-2)
    @THIS
    M=D // THIS=*(frame-2)

    // ====== ARG = *(frame-3)
    @3 // A = 3
    D=A // D = 3
    @R15 // M=LCL = frame
    A=M // A=LCL = frame
    A=A-D // A=frame-3, M=*(frame-3)
    D=M // D=*(frame-3)
    @ARG
    M=D // ARG=*(frame-3)

    // ====== LCL = *(frame-4)
    @4 // A = 4
    D=A // D = 4
    @R15 // M=LCL = frame
    A=M // A=LCL = frame
    A=A-D // A=frame-4, M=*(frame-4)
    D=M // D=*(frame-4)
    @LCL
    M=D // LCL=*(frame-4)

    // ====== goto return_address
    @R14 // A = return_address
    0; JMP

// function Sys.init
(Sys.init)
//C_PUSH constant 4
@4                                 
	D=A                                 
	@SP                                 
	A=M                                 
	M=D                                 
	@SP                                 
	M=M+1
// call Main.fibonacci
// Push return address
    @Sys.Sys.init$ret.0
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push LCL
    @LCL
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push ARG
    @ARG
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push THIS address
    @THIS
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // Push THAT address
    @THAT
    A=M
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    
    // ARG = SP-5-n_args
    @SP
    D=M
    @5
    D=D-A
    @1
    D=D-A
    @ARG
    M=D
    
    // LCL = SP
    @SP
    D=M
    @LCL
    M=D
    
    @Main.fibonacci
    0; JMP
    (Sys.Sys.init$ret.0)

// label WHILE
(Sys.Sys.init$WHILE)// goto WHILE
@Sys.Sys.init$WHILE
0; JMP
