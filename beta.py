import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import matplotlib.pyplot as plt
import matplotlib as mpl
from setup import get_current_money, get_totals, current_row, df
from arguments_helper import arguments
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*set_ticklabels.*")

args = sys.argv

try:
    try:
        try:
            for key, value in arguments.items():
                if value == args[1]:
                    translated_arg1 = key
                if value == args[2]:
                    translated_arg2 = key
        except:
            translated_arg1 = args[1]
            translated_arg2 = args[2]

        start = int(translated_arg1)  # pyright: ignore[reportPossiblyUnboundVariable]
        end = int(translated_arg2)    # pyright: ignore[reportPossiblyUnboundVariable]

        if start > current_row:
            print('Argument out of range.')
        else:
            totals_data = get_totals(start, end)
    except:
        try:
            for key, value in arguments.items():
                if value == args[1]:
                    translated_arg1 = key
        except:
            translated_arg1 = args[1]

        start = int(translated_arg1)  # pyright: ignore[reportPossiblyUnboundVariable]
        end = start

        if start > current_row:
            print('Argument out of range.')
        else:
            totals_data = get_totals(start, end)
except:
    start = current_row
    end = current_row
    totals_data = get_totals(start, end)

categories = totals_data[0]  # type: ignore
total_money = totals_data[1]  # type: ignore
percent = totals_data[2]  # type: ignore

my_money = get_current_money()

mpl.rcParams['font.family'] = 'Helvetica Neue'

# Filter categories with zero values
filtered = [(cat, val) for cat, val in zip(categories, total_money) if val > 0]
filtered_categories, filtered_values = zip(*filtered)

# Color mapping (Apple style)
colors = {
    'Savings': '#8dbad6',  # Savings
    'Setup': '#9bc2e7',    # Setup
    'Home': '#8ea9db',     # Home
    'Studies': '#abb9d4',  # Studies
    'Enjoy': '#b9f5c4',    # Enjoy
    'Others': '#fd9a9a',   # Others
    'Fixed': '#f8ccad',    # Fixed
    'Cashout': '#fef2cb',  # Cashout
}

used_colors = [colors[cat] for cat in filtered_categories]

# Prepare date range
date_range = df['Date'][start:end + 1]

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Bar chart
ax1 = axes[0, 0]
bars = ax1.bar(
    filtered_categories,
    filtered_values,
    color=used_colors,
    edgecolor='white',
    linewidth=1
)
for bar, value in zip(bars, filtered_values):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f'{value:.1f}',
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold'
    )
ax1.set_xticklabels(filtered_categories, rotation=45, ha='right', fontsize=10)
ax1.set_title('Total por categoría')

# Pie chart of percentages
ax2 = axes[0, 1]
ax2.pie(
    filtered_values,
    labels=filtered_categories,
    colors=used_colors,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 10}
)
ax2.axis('equal')
ax2.set_title('Distribución porcentual')

# Cash balance over time
ax3 = axes[1, 0]
cash = df['Cash'][start:end + 1]
ax3.plot(date_range, cash, marker='o')
ax3.set_title('Saldo de caja')
ax3.tick_params(axis='x', rotation=45)
ax3.grid(True)

# Cumulative spending per category
ax4 = axes[1, 1]
category_df = df.loc[start:end, ['Savings','Setup','Home','Studies','Enjoy','Others','Fixed','Cashout']]
cumulative = category_df.cumsum()
for cat in category_df.columns:
    ax4.plot(date_range, cumulative[cat], label=cat, color=colors[cat])
ax4.set_title('Gasto acumulado por categoría')
ax4.tick_params(axis='x', rotation=45)
ax4.legend(fontsize=8)
ax4.grid(True)

try:
    last_result_date = df['Date'][end]
    if start != end:
        fig.suptitle(f"{df['Date'][start]} hasta {last_result_date}", fontsize=15, fontweight='bold')
    else:
        fig.suptitle(f"{df['Date'][start]}", fontsize=15, fontweight='bold')
except:
    pass

plt.tight_layout()
plt.show()
