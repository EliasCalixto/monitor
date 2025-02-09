import pandas as pd
import numpy as np


main_path = "/Users/darkesthj/Library/CloudStorage/OneDrive-Personal/Documentos/Main.xlsx"
df = pd.read_excel(main_path, sheet_name="DataRaw")

# Get Current Row
current_row = 0
counter = 0
for i in range(len(df['Income'])):
    if df['Income'][i] == 0:
        counter += 1
        current_row = i-counter

# Get Current Money
def get_current_money():
    print(round(df['Cash'][current_row], 2))

# Get Totals
def get_totals_report(date = 0):
    total_investment = np.sum(df['Investment'][date:current_row+1])
    total_productivity = np.sum(df['Productivity'][date:current_row+1])
    total_studies = np.sum(df['Studies'][date:current_row+1])
    total_fixed = np.sum(df['Fixed'][date:current_row+1])
    total_clothes = np.sum(df['Clothes'][date:current_row+1])
    total_10 = np.sum(df['10'][date:current_row+1])
    total_food = np.sum(df['Food'][date:current_row+1])
    total_others = np.sum(df['Others'][date:current_row+1])
    total_cashout = np.sum(df['Cashout'][date:current_row+1])

    group_of_totals = [total_investment, 
                       total_productivity, 
                       total_studies, 
                       total_fixed, 
                       total_clothes, 
                       total_10, 
                       total_food, 
                       total_others, 
                       total_cashout]

    investment_percent = round((total_investment/np.sum(group_of_totals))*100, 2)
    productivity_percent = round((total_productivity/np.sum(group_of_totals))*100, 2)
    studies_percent = round((total_studies/np.sum(group_of_totals))*100, 2)
    fixed_percent = round((total_fixed/np.sum(group_of_totals))*100, 2)
    clothes_percent = round((total_clothes/np.sum(group_of_totals))*100, 2)
    percent_10 = round((total_10/np.sum(group_of_totals))*100, 2)
    food_percent = round((total_food/np.sum(group_of_totals))*100, 2)
    others_percent = round((total_others/np.sum(group_of_totals))*100, 2)
    cashout_percent = round((total_cashout/np.sum(group_of_totals))*100, 2)

    print(f'Total Investment: {round(total_investment, 2)} / {investment_percent}%')
    print(f'Total Productivity: {round(total_productivity, 2)} / {productivity_percent}%')
    print(f'Total Studies: {round(total_studies, 2)} / {studies_percent}%')
    print(f'Total Fixed: {round(total_fixed, 2)} / {fixed_percent}%')
    print(f'Total Clothes: {round(total_clothes, 2)} / {clothes_percent}%')
    print(f'Total 10: {round(total_10, 2)} / {percent_10}%')
    print(f'Total Food: {round(total_food, 2)} / {food_percent}%')
    print(f'Total Others: {round(total_others, 2)} / {others_percent}%')
    print(f'Total Cashout: {round(total_cashout, 2)} / {cashout_percent}%')


