@codeStart
0; JMP
(eq)                             
(lt)                                      
(gt)                                      
(neg1)
(pos0)
(END_EQ_LT_GT)
(codeStart)
//C_PUSH constant 111
@111 
                                
//C_PUSH constant 333
@333 
                                
//C_PUSH constant 888
@888 
                                
//C_POP static 8
@SP                         
                        
                        
//C_POP static 3
@SP                         
                        
                        
//C_POP static 1
@SP                         
                        
                        
//C_PUSH static 3
@StaticTest.3                         
                        
//C_PUSH static 1
@StaticTest.1                         
                        
//sub
@SP                   
//C_PUSH static 8
@StaticTest.8                         
                        
//add
@SP                   
(finalLoop)                             