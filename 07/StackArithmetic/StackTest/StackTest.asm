@codeStart
0; JMP
(eq)                             	@SP                             	A=M                             	A=A-1                             	D=M                             	A=A-1                             	D=D-M                             	@neg1                             	D; JEQ                             	@pos0                             	D; JNE
(lt)                                      	@SP                                      	A=A-1                                      	D=M                                      	A=A-1                                      	D=D-M                                      	@neg1                                      	D; JLT                                      	@pos0                                      	D; JGT
(gt)                                      	@SP                                      	A=A-1                                      	D=M                                      	A=A-1                                      	D=D-M                                      	@neg1                                      	D; JGT                                      	@pos0                                      	D; JLT
(neg1)	D=-1	@END_EQ_LT_GT	0; JMP
(pos0)	D=0	@END_EQ_LT_GT	0; JMP
(END_EQ_LT_GT)	@13	A=M	0; JMP
(codeStart)
//C_PUSH constant 17
@17 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 17
@17 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//eq
@label_0_eq                   	D=A                   	@R13                   	M=D                   	@eq                   	0;JMP                   	(label_0_eq)
//C_PUSH constant 17
@17 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 16
@16 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//eq
@label_1_eq                   	D=A                   	@R13                   	M=D                   	@eq                   	0;JMP                   	(label_1_eq)
//C_PUSH constant 16
@16 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 17
@17 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//eq
@label_2_eq                   	D=A                   	@R13                   	M=D                   	@eq                   	0;JMP                   	(label_2_eq)
//C_PUSH constant 892
@892 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 891
@891 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//lt
@label_3_lt                   	D=A                   	@R13                   	M=D                   	@lt                   	0;JMP                   	(label_3_lt)
//C_PUSH constant 891
@891 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 892
@892 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//lt
@label_4_lt                   	D=A                   	@R13                   	M=D                   	@lt                   	0;JMP                   	(label_4_lt)
//C_PUSH constant 891
@891 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 891
@891 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//lt
@label_5_lt                   	D=A                   	@R13                   	M=D                   	@lt                   	0;JMP                   	(label_5_lt)
//C_PUSH constant 32767
@32767 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 32766
@32766 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//gt
@label_6_gt                   	D=A                   	@R13                   	M=D                   	@gt                   	0;JMP                   	(label_6_gt)
//C_PUSH constant 32766
@32766 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 32767
@32767 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//gt
@label_7_gt                   	D=A                   	@R13                   	M=D                   	@gt                   	0;JMP                   	(label_7_gt)
//C_PUSH constant 32766
@32766 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 32766
@32766 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//gt
@label_8_gt                   	D=A                   	@R13                   	M=D                   	@gt                   	0;JMP                   	(label_8_gt)
//C_PUSH constant 57
@57 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 31
@31 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//C_PUSH constant 53
@53 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//add
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M+D // Preform the operation, x op y
//C_PUSH constant 112
@112 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//sub
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M-D // Preform the operation, x op y
//neg
@SP                              M=M-1                              A=M                              M=-M
//and
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M&D // Preform the operation, x op y
//C_PUSH constant 82
@82 
                                	D=A                                 	@SP                                 	A=M                                 	M=D                                 	@SP                                 	M=M+1
//or
@SP                   	M=M-1 // Point to the top of the stack (y)                   	A=M // A points to the next slot                   	D=M // D is one of the values (y)                   	A=A-1 // A points to next value (x)                   	M=M|D // Preform the operation, x op y
//not
@SP                              M=M-1                              A=M                              M=!M
(finalLoop)                             	@finalLoop                             	0; JMP
