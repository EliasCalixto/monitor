import numpy as np
import pandas as pd

main_path = "/Users/darkesthj/Library/CloudStorage/OneDrive-Personal/Documentos/Main.xlsx"

df_raw = pd.read_excel(main_path, 'DataRaw')
df_py = pd.read_excel(main_path, 'DataPy')

for i in range(len(df_raw)):
    df
