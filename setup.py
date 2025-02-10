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
    current_money = round(df['Cash'][current_row], 2)
    print(current_money)
    return current_money

# Get Totals
def get_totals(date = 0):
    total_investment = round(np.sum(df['Investment'][date:current_row+1]), 2)
    total_productivity = round(np.sum(df['Productivity'][date:current_row+1]), 2)
    total_studies = round(np.sum(df['Studies'][date:current_row+1]), 2)
    total_fixed = round(np.sum(df['Fixed'][date:current_row+1]), 2)
    total_clothes = round(np.sum(df['Clothes'][date:current_row+1]), 2)
    total_10 = round(np.sum(df['10'][date:current_row+1]), 2)
    total_food = round(np.sum(df['Food'][date:current_row+1]), 2)
    total_others = round(np.sum(df['Others'][date:current_row+1]), 2)
    total_cashout = round(np.sum(df['Cashout'][date:current_row+1]), 2)

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

    group_of_percent = [investment_percent,
                       productivity_percent,
                       studies_percent,
                       fixed_percent,
                       clothes_percent,
                       percent_10,
                       food_percent,
                       others_percent,
                       cashout_percent]

    print(f'Results since {df["Date"][date]}')
    print(f'Investment: {total_investment} / {investment_percent}%')
    print(f'Productivity: {total_productivity} / {productivity_percent}%')
    print(f'Studies: {total_studies} / {studies_percent}%')
    print(f'Fixed: {total_fixed} / {fixed_percent}%')
    print(f'Clothes: {total_clothes} / {clothes_percent}%')
    print(f'10: {total_10} / {percent_10}%')
    print(f'Food: {total_food} / {food_percent}%')
    print(f'Others: {total_others} / {others_percent}%')
    print(f'Cashout: {total_cashout} / {cashout_percent}%')

    totals_data = [group_of_totals,group_of_percent]
    return totals_data
