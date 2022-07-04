import pandas as pd

def Redata():
    data_df = pd.read_excel('Data.xlsx', sheet_name='nodes')
    Connect = pd.read_excel('Data.xlsx', sheet_name='edges')

    df = data_df.copy()
    list = df['№ узла'].tolist()

    Dir = pd.DataFrame("NaN", list, list)

    Dir2 = Dir.copy()
    connect_df = Connect.copy()

    for i in range(0,len(Dir)):
        for b in range(0,len(connect_df)):
            if(Dir.index[i] == connect_df.iloc[b,0]):
                Dir2.loc[Dir2.index[i],connect_df.iloc[b,2]] = connect_df.iloc[b,4]
    Dir2.dropna(axis='columns',how='all', inplace=True)

    writer = pd.ExcelWriter('output2.xlsx')
    Dir2.to_excel(writer)
    writer.save()

    return Dir2.shape