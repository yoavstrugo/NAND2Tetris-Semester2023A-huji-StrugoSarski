@codeStart
0; JMP
(eq)                             	@SP                             	A=M                             	A=A-1                             	D=M                             	A=A-1                             	D=D-M                             	@neg1                             	D; JEQ                             	@pos0                             	D; JNE
(lt)                                      	@SP                                      	A=A-1                                      	D=M                                      	A=A-1                                      	D=D-M                                      	@neg1                                      	D; JLT                                      	@pos0                                      	D; JGT
(gt)                                      	@SP                                      	A=A-1                                      	D=M                                      	A=A-1                                      	D=D-M                                      	@neg1                                      	D; JGT                                      	@pos0                                      	D; JLT
(neg1)	D=-1	@END_EQ_LT_GT	0; JMP
(pos0)	D=0	@END_EQ_LT_GT	0; JMP
(END_EQ_LT_GT)	@13	A=M	0; JMP
(codeStart)
//C_PUSH constant 3030
@3030 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_POP pointer 0
@SP                         	M=M-1 // Decrease 1 from SP                         	A=M // Get the address of the stack item                         	D=M // The value is now in D                         	@R13                         	M=D // Save the value in R1                         
                        	@THIS                         	D=A // Address of local                         	@0 // Offset                        	A=D+A // Actual address                        	D=A // D is the address                        	@R14                        	M=D // address is in R2                         
                        	@R13                        	D=M // Value is in D                        	@R14 // Address is in M                        	A=M                         	M=D
//C_PUSH constant 3040
@3040 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_POP pointer 1
@SP                         	M=M-1 // Decrease 1 from SP                         	A=M // Get the address of the stack item                         	D=M // The value is now in D                         	@R13                         	M=D // Save the value in R1                         
                        	@THIS                         	D=A // Address of local                         	@1 // Offset                        	A=D+A // Actual address                        	D=A // D is the address                        	@R14                        	M=D // address is in R2                         
                        	@R13                        	D=M // Value is in D                        	@R14 // Address is in M                        	A=M                         	M=D
//C_PUSH constant 32
@32 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_POP this 2
@SP                         	M=M-1 // Decrease 1 from SP                         	A=M // Get the address of the stack item                         	D=M // The value is now in D                         	@R13                         	M=D // Save the value in R1                         
                        	@THIS                         	D=M // Address of local                         	@2 // Offset                        	A=D+A // Actual address                        	D=A // D is the address                        	@R14                        	M=D // address is in R2                         
                        	@R13                        	D=M // Value is in D                        	@R14 // Address is in M                        	A=M                         	M=D
//C_PUSH constant 46
@46 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_POP that 6
@SP                         	M=M-1 // Decrease 1 from SP                         	A=M // Get the address of the stack item                         	D=M // The value is now in D                         	@R13                         	M=D // Save the value in R1                         
                        	@THAT                         	D=M // Address of local                         	@6 // Offset                        	A=D+A // Actual address                        	D=A // D is the address                        	@R14                        	M=D // address is in R2                         
                        	@R13                        	D=M // Value is in D                        	@R14 // Address is in M                        	A=M                         	M=D
//C_PUSH pointer 0
@THIS                         	D=A // D now has the base                         	@0 // index                         	A=A+D // A now has the value's address                         	D=M // D now has the value it self                         
                        	@SP                         	A=M // A has the address of the next slot in the stack                         	M=D // Put the value into the next stack's slot                         	@SP                         	M=M+1 // Increase SP by 1
//C_PUSH pointer 1
@THIS                         	D=A // D now has the base                         	@1 // index                         	A=A+D // A now has the value's address                         	D=M // D now has the value it self                         
                        	@SP                         	A=M // A has the address of the next slot in the stack                         	M=D // Put the value into the next stack's slot                         	@SP                         	M=M+1 // Increase SP by 1
//add
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M+D // Preform the operation, x op y
//C_PUSH this 2
@THIS                         	D=M // D now has the base                         	@2 // index                         	A=A+D // A now has the value's address                         	D=M // D now has the value it self                         
                        	@SP                         	A=M // A has the address of the next slot in the stack                         	M=D // Put the value into the next stack's slot                         	@SP                         	M=M+1 // Increase SP by 1
//sub
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M-D // Preform the operation, x op y
//C_PUSH that 6
@THAT                         	D=M // D now has the base                         	@6 // index                         	A=A+D // A now has the value's address                         	D=M // D now has the value it self                         
                        	@SP                         	A=M // A has the address of the next slot in the stack                         	M=D // Put the value into the next stack's slot                         	@SP                         	M=M+1 // Increase SP by 1
//add
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M+D // Preform the operation, x op y
(finalLoop)                             	@finalLoop                             	0; JMP
