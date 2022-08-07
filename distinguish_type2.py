import os
def type2_cat():
    #file directory
    xls_dir = 'xslx directory'
    files = os.listdir('xslx directory')
    #find files
    import pandas as pd
    import re
    type2_df = {}
    index_errors = []
    for file in files:
        print(file)
        regex = r'[\d]{1,5}[-][\d]{1,2}[-][\d]{1,2}'
        xls=pd.ExcelFile(xls_dir+file)
        if len(xls.sheet_names)==1:
            date_list = []
            df = xls.parse(xls.sheet_names[0])
            try:
                for k in range(20):
                    df_d = list(set(df.iloc[k][df.iloc[k].str.match(regex)==True]))
                    date_list.append(df_d)
                date_list = [item for sublist in date_list for item in sublist]
                date_list = list(set(date_list))
                if len(date_list)==1:
                    type2_df[date_list[0]]=file
            except IndexError as ie:
                index_errors.append(file)
    
    return type2_df, index_errors
