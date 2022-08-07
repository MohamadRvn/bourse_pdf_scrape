import pandas as pd
import numpy as np

def agg_type2():

    '''iterate over type2 files, seperating them into 6/7 df, adding them to a dict
    with keys associated to each df, and adding the dict with key=date to final_dict
    which will be saved into a db for later use.'''

    #load from directory
    xls_dir = 'xlsx files directory' #directory of xls files
    type2_xls_dir = 'xlsx file' #xls file containing type2 file name/date
    type2 = pd.read_excel(type2_xls_dir) #load file containing type 2 file name/date into df
    type2.drop(columns=['Unnamed: 0'], inplace=True) #drop type2's 1st col
    type2cols = type2.columns
    type2df_dict = {}
    errors = []
    #do shit
    for file in type2cols: #itterate over filenames in type2
        xls = pd.ExcelFile(xls_dir+type2[file].iloc[0]) #load file in type2 into an xls object
        print(type2[file].iloc[0])
        df = xls.parse(xls.sheet_names[0]) #create df from sheet1 of xls (type2 # of sheets:1)
        df.replace(np.nan, '#',inplace = True) #replace nan with #(str) for search/comparison convenience
        dict_file = {}

        #step 1:find گزارش خلاصه عملکرد بازار
        
        p1row = 0
        p1rows = []
        while p1row<20: #remove rows before گزارش خلاصه...
            if ('خلاصه' in str(df.iloc[p1row]['Unnamed: 0']))==False:
                p1rows.append(p1row)
                p1row+=1
            else:
                df.drop(p1rows, inplace=True)
                break
        #step 2:find خلاصه بازار
        df.reset_index(inplace=True)
        df.drop(columns=['index'], inplace=True)
        dict_file['summary']=pd.DataFrame(dict(zip(df.loc[2][['Unnamed: 0','Unnamed: 1', 'Unnamed: 2']].values,
                                                df.loc[3][['Unnamed: 0','Unnamed: 1', 'Unnamed: 2']].astype(str).values)),
                                                index=[0]).copy(deep=True)

        #step 3:find ارزش/حجم سهم حقوق/حقیقی

        df.drop([0,1,2,3], inplace=True)
        df.reset_index(inplace=True)
        df.drop(columns=['index'], inplace=True)
        p1row= 0
        p1rows = []
        while p1row<7:
            if ('حجم' in str(df.iloc[p1row]['Unnamed: 1']))==False:
                p1rows.append(p1row)
                p1row+=1
            else:
                df.drop(p1rows, inplace=True)
                break
        df.reset_index(inplace=True)
        idx_drop = df.iloc[0]['index']
        df.drop(idx_drop, inplace=True)
        df.drop(columns=['index'], inplace=True)
        df.reset_index(inplace=True)
        df.drop(columns=['index'], inplace=True)
        dict_file['ex(total vol)']= pd.DataFrame(np.array(df.iloc[1:4][['Unnamed: 0','Unnamed: 1','Unnamed: 2']].copy(deep=True)),
                    columns=np.array(df.iloc[0][['Unnamed: 0','Unnamed: 1', 'Unnamed: 2']].copy(deep=True)))
        if df.iloc[1]['Unnamed: 6'] != '#':
            if df.iloc[1]['Unnamed: 4'] == '#':
                dict_file['ex(total cost)'] = pd.DataFrame(np.array(df.iloc[1:4][['Unnamed: 5','Unnamed: 6','Unnamed: 7']].copy(deep=True)),
                                columns=np.array(df.iloc[0][['Unnamed: 5','Unnamed: 6', 'Unnamed: 7']].copy(deep=True)))
            else:
                dict_file['ex(total cost)'] = pd.DataFrame(np.array(df.iloc[1:4][['Unnamed: 4','Unnamed: 5','Unnamed: 6']].copy(deep=True)),
                                columns=np.array(df.iloc[0][['Unnamed: 4','Unnamed: 5', 'Unnamed: 6']].copy(deep=True)))
        else:
            dict_file['ex(total cost)'] = pd.DataFrame()
        
        #step 4:find top 3

        df.drop([0,1,2,3],inplace=True)
        df.reset_index(inplace=True)
        df.drop(columns=['index'], inplace=True)
        p1row= 0
        p1rows = []
        while p1row<6:
            if df.iloc[p1row]['Unnamed: 0']=='#':
                p1rows.append(p1row)
                p1row+=1
            else:
                df.drop(p1rows, inplace=True)
                break
        df.reset_index(inplace=True)
        df.drop(columns=['index'], inplace=True)
        dict_file['top 3(vol)'] = pd.DataFrame(np.array(df.iloc[1:4][['Unnamed: 0','Unnamed: 1','Unnamed: 2','Unnamed: 3']].copy(deep=True)),
                            columns=np.array(df.iloc[0][['Unnamed: 0','Unnamed: 1','Unnamed: 2','Unnamed: 3']].copy(deep=True)))
        if df.iloc[1]['Unnamed: 6'] != '#':
            if df.iloc[1]['Unnamed: 5'] == '#':
                dict_file['top 3(tc)'] = pd.DataFrame(np.array(df.iloc[1:4][['Unnamed: 6','Unnamed: 7','Unnamed: 8','Unnamed: 9']].copy(deep=True)),
                                columns=np.array(df.iloc[0][['Unnamed: 6','Unnamed: 7','Unnamed: 8','Unnamed: 9']].copy(deep=True)))
            else:
                dict_file['top 3(tc)'] = pd.DataFrame(np.array(df.iloc[1:4][['Unnamed: 5','Unnamed: 6','Unnamed: 7','Unnamed: 8']].copy(deep=True)),
                                columns=np.array(df.iloc[0][['Unnamed: 5','Unnamed: 6','Unnamed: 7','Unnamed: 8']].copy(deep=True)))
        else:
            dict_file['top 3(tc)'] = pd.DataFrame()
        
        #step 5:find vol day

        df.drop([0,1,2,3],inplace=True)
        df.reset_index(inplace=True)
        df.drop(columns=['index'], inplace=True)
        p1row = 0
        p1rows = []
        while p1row<7:
            if ('كد' in str(df.iloc[p1row]['Unnamed: 0']))==False:
                p1rows.append(p1row)
                p1row+=1
            else:
                df.drop(p1rows, inplace=True)
                break

        if df.shape[1] == 12:
            df.drop(columns=['Unnamed: 10', 'Unnamed: 11'], inplace=True)

        df.reset_index(inplace=True)
        df.drop(columns=['index'], inplace=True)
        new_cols = ['sym','name','lvolbn','rvolbn','lvolb%','rvolb%','lvolsn','rvolsn','lvols%','rvols%']
        df.rename(columns=dict(zip(df.columns,new_cols)), inplace=True)
        df.drop([0],inplace=True)
        df.reset_index(inplace=True)
        df.drop(columns=['index'], inplace=True)
        p1row = 0
        p1rows = []
        try:
            while p1row<df.shape[0]:
                if set(df.iloc[p1row].values) == {'#'}:
                    p1rows.append(p1row)
                p1row+=1
            if len(p1rows)!=0:
                dict_file['vol daily'] = df.iloc[:p1rows[0]].copy(deep=True)

                #step 6:find val day
            
                df.drop([row for row in range(p1rows[0]+3)], inplace=True)
                new_cols = ['sym','name','lvalbn','rvalbn','lvalb%','rvalb%','lvalsn','rvalsn','lvals%','rvals%']
                df.rename(columns=dict(zip(df.columns,new_cols)), inplace=True)
                dict_file['val daily'] = df.copy(deep=True)
            else:
                dict_file['vol daily'] = pd.DataFrame()
                dict_file['val daily'] = df.copy(deep=True)
        except IndexError:
            errors.append(type2[file].iloc[0])
        #save to main dict
        type2df_dict[file] = dict_file.copy()
    
    return type2df_dict, errors
