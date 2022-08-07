import os
import re
import pandas as pd
import tabula

def type3_cat():
    #file directory and list of pdf names
    pdf2_dir = 'pdf directory'
    pdf_files = os.listdir('pdf directoru)
    #dates already covered in type1 and type2
    #load data calling item in files list and merge them
    type3_df = {}
    ierror3 =[]
    for file in pdf_files:
        print(file)
        page1 = tabula.read_pdf('%s%s'%(pdf2_dir,file), guess=True, pages = 1, stream=True ,lattice = True, encoding="utf-8", pandas_options={'header':None})
        try:
            type3_df[page1[1].iloc[2][3]] = file
        except IndexError:
            ierror3.append(file)
    return type3_df, ierror3
