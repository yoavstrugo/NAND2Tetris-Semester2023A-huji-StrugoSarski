@codeStart
0; JMP
(eq)                             	@SP                             	A=M                             	A=A-1                             	D=M                             	A=A-1                             	D=D-M                             	@neg1                             	D; JEQ                             	@pos0                             	D; JNE
(lt)                                      	@SP                                      	A=A-1                                      	D=M                                      	A=A-1                                      	D=D-M                                      	@neg1                                      	D; JLT                                      	@pos0                                      	D; JGT
(gt)                                      	@SP                                      	A=A-1                                      	D=M                                      	A=A-1                                      	D=D-M                                      	@neg1                                      	D; JGT                                      	@pos0                                      	D; JLT
(neg1)	D=-1	@END_EQ_LT_GT	0; JMP
(pos0)	D=0	@END_EQ_LT_GT	0; JMP
(END_EQ_LT_GT)	@13	A=M	0; JMP
(codeStart)
//C_PUSH constant 111
@111 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 333
@333 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 888
@888 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_POP static 8
@SP                         	M=M-1 // Decrease 1 from SP                         	A=M // Get the address of the stack item                         	D=M // The value is now in D                         	@R13                         	M=D // Save the value in R1                         
                        	@StaticTest.8                         	D=M // Address of local                         	@8 // Offset                        	A=D+A // Actual address                        	D=A // D is the address                        	@R14                        	M=D // address is in R2                         
                        	@R13                        	D=M // Value is in D                        	@R14 // Address is in M                        	A=M                         	M=D
//C_POP static 3
@SP                         	M=M-1 // Decrease 1 from SP                         	A=M // Get the address of the stack item                         	D=M // The value is now in D                         	@R13                         	M=D // Save the value in R1                         
                        	@StaticTest.3                         	D=M // Address of local                         	@3 // Offset                        	A=D+A // Actual address                        	D=A // D is the address                        	@R14                        	M=D // address is in R2                         
                        	@R13                        	D=M // Value is in D                        	@R14 // Address is in M                        	A=M                         	M=D
//C_POP static 1
@SP                         	M=M-1 // Decrease 1 from SP                         	A=M // Get the address of the stack item                         	D=M // The value is now in D                         	@R13                         	M=D // Save the value in R1                         
                        	@StaticTest.1                         	D=M // Address of local                         	@1 // Offset                        	A=D+A // Actual address                        	D=A // D is the address                        	@R14                        	M=D // address is in R2                         
                        	@R13                        	D=M // Value is in D                        	@R14 // Address is in M                        	A=M                         	M=D
//C_PUSH static 3
@StaticTest.3                         	D=M // D now has the base                         	@3 // index                         	A=A+D // A now has the value's address                         	D=M // D now has the value it self                         
                        	@SP                         	A=M // A has the address of the next slot in the stack                         	M=D // Put the value into the next stack's slot                         	@SP                         	M=M+1 // Increase SP by 1
//C_PUSH static 1
@StaticTest.1                         	D=M // D now has the base                         	@1 // index                         	A=A+D // A now has the value's address                         	D=M // D now has the value it self                         
                        	@SP                         	A=M // A has the address of the next slot in the stack                         	M=D // Put the value into the next stack's slot                         	@SP                         	M=M+1 // Increase SP by 1
//sub
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M-D // Preform the operation, x op y
//C_PUSH static 8
@StaticTest.8                         	D=M // D now has the base                         	@8 // index                         	A=A+D // A now has the value's address                         	D=M // D now has the value it self                         
                        	@SP                         	A=M // A has the address of the next slot in the stack                         	M=D // Put the value into the next stack's slot                         	@SP                         	M=M+1 // Increase SP by 1
//add
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M+D // Preform the operation, x op y
(finalLoop)                             	@finalLoop                             	0; JMP
