import re
import pandas as pd

input_file_template = '1'#<00,01,02,03,09...>.csv
output_file_template = '2'


for i in years:
    #print(i)
    in_file = "{}{}.csv".format(input_file_template,i)
    print('opening{}'.format(in_file))
    inf = open(in_file,'r')
    line_number = 0    
    state = 0
    year_string = ''
    column_headers = []
    out_file = "{}{}.csv".format(output_file_template,i)
    outf = open(out_file,'w+')
    for line in inf:
        line_number += 1

        
        #determine state
        prev_state = state
        if 'text' in line:
        
        #state work
        if state==1:#
            x=1#do stuff