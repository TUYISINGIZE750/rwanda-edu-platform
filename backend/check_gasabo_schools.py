import pandas as pd

df = pd.read_excel('10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx', header=1)
gasabo = df[df['District '].str.contains('Gasabo', case=False, na=False)]

print('GASABO SCHOOLS WITH CODES:')
for _, row in gasabo[['School code ', 'School Name ', 'District ']].drop_duplicates().iterrows():
    print(f'Code: {row["School code "]}, Name: {row["School Name "]}')