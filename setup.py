import pandas as pd
import numpy as np

main_path = "/Users/darkesthj/Library/CloudStorage/OneDrive-Personal/Shared/Main.xlsx"
df = pd.read_excel(main_path, sheet_name="DataRaw")

# Get Current Row
current_row = 0
for i in range(len(df)):
    if sum(df.loc[i, ['Savings','Setup','Home','Studies','Enjoy','Others','Fixed','Cashout']]) != 0:
        current_row += 1

# Get Current Money
def get_current_money():
    current_money = round(df['Cash'][current_row], 2)
    print(current_money)
    return current_money

# Get Totals
def get_totals(date = 0):
    total_savings = round(np.sum(df['Savings'][date:current_row+1]), 2)
    total_setup = round(np.sum(df['Setup'][date:current_row+1]), 2)
    total_home = round(np.sum(df['Home'][date:current_row+1]), 2)
    total_studies = round(np.sum(df['Studies'][date:current_row+1]), 2)
    total_enjoy = round(np.sum(df['Enjoy'][date:current_row+1]), 2)
    total_others = round(np.sum(df['Others'][date:current_row+1]), 2)
    total_fixed = round(np.sum(df['Fixed'][date:current_row+1]), 2)
    total_cashout = round(np.sum(df['Cashout'][date:current_row+1]), 2)

    group_of_categories = ['Savings',
                           'Setup',
                           'Home',
                           'Studies',
                           'Enjoy',
                           'Others',
                           'Fixed',
                           'Cashout']

    group_of_totals = [total_savings,
                       total_setup, 
                       total_home,
                       total_studies, 
                       total_enjoy, 
                       total_others, 
                       total_fixed, 
                       total_cashout]

    savings_percent = round((total_savings/np.sum(group_of_totals))*100, 2)
    setup_percent = round((total_setup/np.sum(group_of_totals))*100, 2)
    home_percent = round((total_home/np.sum(group_of_totals))*100, 2)
    studies_percent = round((total_studies/np.sum(group_of_totals))*100, 2)
    enjoy_percent = round((total_enjoy/np.sum(group_of_totals))*100, 2)
    others_percent = round((total_others/np.sum(group_of_totals))*100, 2)
    fixed_percent = round((total_fixed/np.sum(group_of_totals))*100, 2)
    cashout_percent = round((total_cashout/np.sum(group_of_totals))*100, 2)

    group_of_percent = [savings_percent,
                        setup_percent,
                        home_percent,
                        studies_percent,
                        enjoy_percent,
                        others_percent,
                        fixed_percent,
                        cashout_percent]

    print(f'{df["Date"][date]}')
    print(f'Savings: S/.{total_savings} | {savings_percent}%')
    print(f'Setup: S/.{total_setup} | {setup_percent}%')
    print(f'Home: S/.{total_home} | {home_percent}%')
    print(f'Studies: S/.{total_studies} | {studies_percent}%')
    print(f'Enjoy: S/.{total_enjoy} | {enjoy_percent}%')
    print(f'Others: S/.{total_others} | {others_percent}%')
    print(f'Fixed: S/.{total_fixed} | {fixed_percent}%')
    print(f'Cashout: S/.{total_cashout} | {cashout_percent}%')

    totals_data = [group_of_categories,group_of_totals,group_of_percent]
    return totals_data

if __name__ == "__main__":
    print(current_row)