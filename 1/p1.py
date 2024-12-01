import pandas as pd

df = pd.read_csv('1/data.txt', delimiter='   ', header=None)  

l0 = sorted(df.iloc[:, 0].astype(int).tolist())
l1 = sorted(df.iloc[:, 1].astype(int).tolist())

df2 = pd.DataFrame({'C0': l0, 'C1': l1})
df2['diff'] = (df2['C0'] - df2['C1']).abs()
print(df2['diff'].sum())

# ============ # 
#  second part 
# ============ # 

left_df =      df2['C0'].value_counts().reset_index()
right_counts = df2['C1'].value_counts().reset_index()
totals = pd.merge(left=left_df, right=right_counts, how='left', left_on='C0', right_on='C1' )
totals['count_y'] = totals['count_y'].fillna(0) 

print((totals['C0']*totals['count_y']).sum())
