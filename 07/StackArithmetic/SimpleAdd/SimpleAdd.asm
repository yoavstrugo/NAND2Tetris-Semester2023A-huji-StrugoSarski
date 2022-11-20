@codeStart
0; JMP
(eq)                             	@SP                             	A=M                             	A=A-1                             	D=M                             	A=A-1                             	D=D-M                             	@neg1                             	D; JEQ                             	@pos0                             	D; JNE
(lt)                                      	@SP                                      	A=A-1                                      	D=M                                      	A=A-1                                      	D=D-M                                      	@neg1                                      	D; JLT                                      	@pos0                                      	D; JGT
(gt)                                      	@SP                                      	A=A-1                                      	D=M                                      	A=A-1                                      	D=D-M                                      	@neg1                                      	D; JGT                                      	@pos0                                      	D; JLT
(neg1)	D=-1	@END_EQ_LT_GT	0; JMP
(pos0)	D=0	@END_EQ_LT_GT	0; JMP
(END_EQ_LT_GT)	@13	A=M	0; JMP
(codeStart)
//C_PUSH constant 7
@7 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 8
@8 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//add
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M+D // Preform the operation, x op y
(finalLoop)                             	@finalLoop                             	0; JMP
