import pandas as pd
import numpy as np

main_path = "/Users/darkesthj/Library/CloudStorage/OneDrive-Personal/Shared/Main.xlsx"
df = pd.read_excel(main_path, sheet_name="DataRaw")

# Get Current Row
current_row = 0
for i in range(len(df)):
    if sum(df.iloc[i][['Savings','Setup','Home','Studies','Enjoy','Others','Fixed','Cashout']].values) != 0:
        current_row += 1

# Get Current Money
def get_current_money():
    current_money = round(df['Cash'][current_row], 2)
    print(current_money)
    return current_money

# Get Totals
def get_totals(date_start, date_end):
    total_savings = round(np.sum(df['Savings'][date_start:date_end+1]), 2)
    total_setup = round(np.sum(df['Setup'][date_start:date_end+1]), 2)
    total_home = round(np.sum(df['Home'][date_start:date_end+1]), 2)
    total_studies = round(np.sum(df['Studies'][date_start:date_end+1]), 2)
    total_enjoy = round(np.sum(df['Enjoy'][date_start:date_end+1]), 2)
    total_others = round(np.sum(df['Others'][date_start:date_end+1]), 2)
    total_fixed = round(np.sum(df['Fixed'][date_start:date_end+1]), 2)
    total_cashout = round(np.sum(df['Cashout'][date_start:date_end+1]), 2)

    # total_savings = round(np.sum(df['Savings'][date]), 2)
    # total_setup = round(np.sum(df['Setup'][date]), 2)
    # total_home = round(np.sum(df['Home'][date]), 2)
    # total_studies = round(np.sum(df['Studies'][date]), 2)
    # total_enjoy = round(np.sum(df['Enjoy'][date]), 2)
    # total_others = round(np.sum(df['Others'][date]), 2)
    # total_fixed = round(np.sum(df['Fixed'][date]), 2)
    # total_cashout = round(np.sum(df['Cashout'][date]), 2)
    
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

    print(f'Savings - {total_savings}')
    print(f'Setup - {total_setup}')
    print(f'Home - {total_home}')
    print(f'Studies - {total_studies}')
    print(f'Enjoy - {total_enjoy}')
    print(f'Others - {total_others}')
    print(f'Fixed - {total_fixed}')
    print(f'Cashout - {total_cashout}')

    totals_data = [group_of_categories,group_of_totals,group_of_percent]
    return totals_data

if __name__ == "__main__":
    print(current_row)