import numpy as np
import pandas as pd


try:
    dataFrame = pd.read_excel("C:\\Users\\elias\\OneDrive\\Documentos\\Main.xlsx", sheet_name='IngresosyGastos', engine='openpyxl')
    allData = np.array(dataFrame)
except:
    dataFrame = pd.read_excel('/Users/darkesthj/Library/CloudStorage/OneDrive-Personal/Documentos/Main.xlsx', sheet_name='IngresosyGastos', engine='openpyxl')
    allData = np.array(dataFrame)

print(allData)

# def getTotalBlue(allData):
#     totalBlue = 
#     return totalBlue
#
# def getTotalRed(allData):
#     return totalRed
#
# def getCurrentMoney(allData):
#     return currentMoney
