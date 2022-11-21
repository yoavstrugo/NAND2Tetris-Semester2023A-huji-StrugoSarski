@codeStart
0; JMP
(eq)                             	@SP                             	A=M                             	A=A-1                             	D=M                             	A=A-1                             	D=D-M                             	@neg1                             	D; JEQ                             	@pos0                             	D; JNE
(lt)                                      	@SP                                      	A=M                                      	A=A-1                                      	D=M                                      	A=A-1                                      	D=M-D                                      	@neg1                                      	D; JLT                                      	@pos0                                      	D; JMP
(gt)                                      	@SP                                      	A=M                                      	A=A-1                                      	D=M                                      	A=A-1                                      	D=M-D                                      	@neg1                                      	D; JGT                                      	@pos0                                      	D; JMP
(neg1)                 	D=-1                 	@END_EQ_LT_GT                 	0; JMP                 
(pos0)                 	D=0                 	@END_EQ_LT_GT                 	0; JMP
(END_EQ_LT_GT)                 	@SP                 	M=M-1 // Decrease SP by 1                	A=M                 	A=A-1                 	M=D // Push D to the stack                 	@R13                 	A=M                 	0; JMP
(codeStart)
//C_PUSH constant 32767
@32767                                 	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//neg
@SP                              	A=M                              	A=A-1                              	M=-M
//C_PUSH constant 1
@1                                 	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//sub
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M-D // Preform the operation, x op y
//C_PUSH constant 32767
@32767                                 	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//lt
@label_0_lt                   	D=A                   	@R13                   	M=D                   	@lt                   	0;JMP                   	(label_0_lt)
//C_PUSH constant 32767
@32767                                 	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 32767
@32767                                 	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//neg
@SP                              	A=M                              	A=A-1                              	M=-M
//C_PUSH constant 1
@1                                 	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//sub
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M-D // Preform the operation, x op y
//gt
@label_1_gt                   	D=A                   	@R13                   	M=D                   	@gt                   	0;JMP                   	(label_1_gt)
//C_PUSH constant 20000
@20000                                 	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//neg
@SP                              	A=M                              	A=A-1                              	M=-M
//C_PUSH constant 1
@1                                 	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//sub
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M-D // Preform the operation, x op y
//C_PUSH constant 30000
@30000                                 	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//gt
@label_2_gt                   	D=A                   	@R13                   	M=D                   	@gt                   	0;JMP                   	(label_2_gt)
//C_PUSH constant 20000
@20000                                 	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 30000
@30000                                 	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//neg
@SP                              	A=M                              	A=A-1                              	M=-M
//C_PUSH constant 1
@1                                 	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//sub
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M-D // Preform the operation, x op y
//gt
@label_3_gt                   	D=A                   	@R13                   	M=D                   	@gt                   	0;JMP                   	(label_3_gt)
