import os
from setup import df, current_row
from private import pwd


# 1 clone df into new_df
new_df = df.copy()

for i in range(current_row + 1, len(new_df)):
    new_df.drop(index=i, inplace=True)

list_new_df = new_df.values.tolist()

# 2 Creating the SQL request
query = f"""USE main_db
DELETE FROM dbo.data_raw
GO

INSERT INTO dbo.data_raw (Id,DateInfo,Income,Setup,Home,Savings,Studies,Enjoy,Others,Fixed,Cashout,Cash)
VALUES 
"""

values = []

for i in range(len(list_new_df)):
    values.append(f"({list_new_df[i][0]},'{list_new_df[i][1]}',{list_new_df[i][2]},'{list_new_df[i][3]}','{list_new_df[i][4]}',{list_new_df[i][5]},{list_new_df[i][6]},{list_new_df[i][7]},{list_new_df[i][8]},{list_new_df[i][9]},{list_new_df[i][10]},{list_new_df[i][11]})")

query += ',\n'.join(values) + ";\nGO"

query += f"\n\nSELECT * FROM dbo.data_raw\nGO"

with open('update.sql', 'w') as f:
    f.write(query)
    
# 3 Ejecuting the SQL request through terminal
os.system(f"sqlcmd -S localhost,1433 -U sa -P {pwd} -d main_db -i /Users/darkesthj/dev/monitor/update.sql")
