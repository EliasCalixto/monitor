from setup import df, current_row


# 1 Pass df to new_df
new_df = df.copy()

for i in range(current_row + 1, len(new_df)):
    df.drop(index=i, inpew_lace=True)

