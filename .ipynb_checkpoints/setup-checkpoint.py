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
    total_setup = round(np.sum(df['Setup'][date:current_row+1]), 2)
    total_home = round(np.sum(df['Home'][date:current_row+1]), 2)
    total_savings = round(np.sum(df['Savings'][date:current_row+1]), 2)
    total_studies = round(np.sum(df['Studies'][date:current_row+1]), 2)
    total_enjoy = round(np.sum(df['Enjoy'][date:current_row+1]), 2)
    total_others = round(np.sum(df['Others'][date:current_row+1]), 2)
    total_fixed = round(np.sum(df['Fixed'][date:current_row+1]), 2)
    total_cashout = round(np.sum(df['Cashout'][date:current_row+1]), 2)

    group_of_categories = ['Setup',
                           'Home',
                           'Savings',
                           'Studies',
                           'Enjoy',
                           'Others',
                           'Fixed',
                           'Cashout']

    group_of_totals = [total_setup, 
                       total_home,
                       total_savings,
                       total_studies, 
                       total_enjoy, 
                       total_others, 
                       total_fixed, 
                       total_cashout]

    setup_percent = round((total_setup/np.sum(group_of_totals))*100, 2)
    home_percent = round((total_home/np.sum(group_of_totals))*100, 2)
    savings_percent = round((total_savings/np.sum(group_of_totals))*100, 2)
    studies_percent = round((total_studies/np.sum(group_of_totals))*100, 2)
    enjoy_percent = round((total_enjoy/np.sum(group_of_totals))*100, 2)
    others_percent = round((total_others/np.sum(group_of_totals))*100, 2)
    fixed_percent = round((total_fixed/np.sum(group_of_totals))*100, 2)
    cashout_percent = round((total_cashout/np.sum(group_of_totals))*100, 2)

    group_of_percent = [setup_percent,
                        home_percent,
                        savings_percent,
                        studies_percent,
                        enjoy_percent,
                        others_percent,
                        fixed_percent,
                        cashout_percent]

    print(f'{df["Date"][date]}')
    print(f'Setup: {total_setup} / {setup_percent}%')
    print(f'Home: {total_home} / {home_percent}%')
    print(f'Savings: {total_savings} / {savings_percent}%')
    print(f'Studies: {total_studies} / {studies_percent}%')
    print(f'Enjoy: {total_enjoy} / {enjoy_percent}%')
    print(f'Others: {total_others} / {others_percent}%')
    print(f'Fixed: {total_fixed} / {fixed_percent}%')
    print(f'Cashout: {total_cashout} / {cashout_percent}%')

    totals_data = [group_of_categories,group_of_totals,group_of_percent]
    return totals_data
