@codeStart
0; JMP
(eq)                             
(lt)                                      
(gt)                                      
(neg1)
(pos0)
(END_EQ_LT_GT)
(codeStart)
//C_PUSH constant 3030
@3030 
                                
//C_POP pointer 0
@SP                         
                        
                        
//C_PUSH constant 3040
@3040 
                                
//C_POP pointer 1
@SP                         
                        
                        
//C_PUSH constant 32
@32 
                                
//C_POP this 2
@SP                         
                        
                        
//C_PUSH constant 46
@46 
                                
//C_POP that 6
@SP                         
                        
                        
//C_PUSH pointer 0
@THIS                         
                        
//C_PUSH pointer 1
@THIS                         
                        
//add
@SP                   
//C_PUSH this 2
@THIS                         
                        
//sub
@SP                   
//C_PUSH that 6
@THAT                         
                        
//add
@SP                   
(finalLoop)                             