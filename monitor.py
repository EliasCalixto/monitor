import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mc
import colorsys
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

total_expend = sum(total_money)
my_money = get_current_money()

# prints del final

print('')
print(f'Total expended: {total_expend:.2f}')
print(f'Current money: {my_money:.2f}')

mpl.rcParams['font.family'] = 'Helvetica Neue'

# Helper to darken hex colors slightly while keeping palette
def darken(color, amount=0.15):
    try:
        c = mc.cnames.get(color, color)
        r, g, b = mc.to_rgb(c) # type: ignore
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = max(0, l * (1 - amount))
        r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
        return (r2, g2, b2)
    except Exception:
        return color

# Filter categories with zero values
filtered = [(cat, val) for cat, val in zip(categories, total_money) if val > 0]
filtered_categories, filtered_values = zip(*filtered) if filtered else ([], [])

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

used_colors = [colors[cat] for cat in filtered_categories] if filtered_categories else []

# Prepare date range
date_range = df['Date'][start:end + 1]

# Use GridSpec to make the bottom-right chart span the full bottom row
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(2, 2)

# Bar chart (top-left)
ax1 = fig.add_subplot(gs[0, 0])
if filtered_categories:
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

# Pie chart of percentages (top-right)
ax2 = fig.add_subplot(gs[0, 1])
if filtered_categories:
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

# Cumulative spending per category — spans entire bottom row
ax4 = fig.add_subplot(gs[1, :])

# Slightly darker colors while keeping palette tones
colors_for_ax4 = ['#8dbad6', "#515151", "#e4b373", "#43859a", '#b9f5c4', '#fd9a9a']
colors_for_ax4_darker = [darken(c, 0.2) for c in colors_for_ax4]

category_df = df.loc[start:end, ['Savings','Setup','Home','Studies','Enjoy','Others']]

# Make lines clearer: thicker lines, subtle markers
for i, cat in enumerate(category_df.columns):
    ax4.plot(
        date_range,
        category_df[cat],
        label=cat,
        color=colors_for_ax4_darker[i],
        linewidth=2.4,
        marker='o',
        markersize=4,
        markerfacecolor='white',
        markeredgewidth=1.2,
        alpha=0.95,
        solid_capstyle='round'
    )

ax4.set_title('Gasto acumulado por categoría')
ax4.tick_params(axis='x', rotation=45)
ax4.legend(fontsize=9, ncol=2)
ax4.grid(True, linestyle='--', alpha=0.4)

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

