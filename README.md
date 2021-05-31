# Calculator

### Procedure

1. Tokenize the expression (convert string into list of tokens)  
    - Numbers to number token  
    `1.25` -> `{'type':'NUMBER', 'number': 1.25}`  
    - Arithmetic signs to corresponding sign token  
    `+` ->  `{'type':'PLUS'}`  
    `-` ->  `{'type':'MINUS'}`  
    `*` ->  `{'type':'MUL'}`  
    `/` ->  `{'type':'DIV'}`  
    - Nested expressions in parentheses are converted 
    into expression tokens with all of their contents 
    being recursively tokenized  
    `'(1+2)'` -> `{'type':'EXPR', 'tokens': tokenize('1+2')}`  
2. Evaluate the tokenized expression  
    - Recursively evaluate nested expressions  
    `(1+(1+(1+1)))+(3*5)-(1/2)` -> `4+15-0.5`  
    - Evaluate all the `DIV` and `MUL` tokens  
    `3*5+1-8/2` -> `15+1-4`  
    - Finally, evaluate all the `PLUS` and `MINUS` tokens  
    `1+3-5` -> `-1`  
    
    