@codeStart
0; JMP
(eq)                             
(lt)                                      
(gt)                                      
(neg1)                 
(pos0)                 
(END_EQ_LT_GT)                 
(codeStart)
//C_PUSH constant 32767
@32767                                 
//neg
@SP                              
//C_PUSH constant 1
@1                                 
//sub
@SP                   
//C_PUSH constant 32767
@32767                                 
//lt
@label_0_lt                   
//C_PUSH constant 32767
@32767                                 
//C_PUSH constant 32767
@32767                                 
//neg
@SP                              
//C_PUSH constant 1
@1                                 
//sub
@SP                   
//gt
@label_1_gt                   
//C_PUSH constant 20000
@20000                                 
//neg
@SP                              
//C_PUSH constant 1
@1                                 
//sub
@SP                   
//C_PUSH constant 30000
@30000                                 
//gt
@label_2_gt                   
//C_PUSH constant 20000
@20000                                 
//C_PUSH constant 30000
@30000                                 
//neg
@SP                              
//C_PUSH constant 1
@1                                 
//sub
@SP                   
//gt
@label_3_gt                   