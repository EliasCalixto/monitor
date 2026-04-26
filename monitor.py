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

warnings.filterwarnings("ignore")

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
    'Losses': '#fd9a9a',   # Losses
    'Fixed': '#f8ccad',    # Fixed
    'Cashout': '#fef2cb',  # Cashout
}

used_colors = [colors[cat] for cat in filtered_categories] if filtered_categories else []

# Prepare date range aligned with the filtered rows
date_series = df.loc[start:end, 'Date'] if 'Date' in df.columns else df['Date'][start:end + 1]
date_labels = list(date_series)
x_positions = list(range(len(date_labels)))

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

# Monthly comparison per category — spans entire bottom row
ax4 = fig.add_subplot(gs[1, :])

category_columns = ['Savings', 'Setup', 'Home', 'Studies', 'Enjoy', 'Losses', 'Fixed', 'Cashout']
available_categories = [col for col in category_columns if col in df.columns]
category_df = df.loc[start:end, available_categories].fillna(0)
active_categories = [
    cat
    for cat in available_categories
    if category_df[cat].sum() > 0
]
category_color_map = {
    cat: darken(colors.get(cat, '#4c4c4c'), 0.2)
    for cat in available_categories
}

if not active_categories or category_df.empty:
    ax4.set_title('Sin datos disponibles para las categorías seleccionadas')
    ax4.axis('off')
else:
    category_count = len(active_categories)
    bar_width = min(0.8 / category_count, 0.12)
    category_offsets = [
        (index - (category_count - 1) / 2) * bar_width
        for index in range(category_count)
    ]

    for index, category in enumerate(active_categories):
        bar_positions = [
            position + category_offsets[index]
            for position in x_positions
        ]
        ax4.bar(
            bar_positions,
            category_df[category].to_numpy(),
            width=bar_width * 0.92,
            label=category,
            color=category_color_map.get(category, '#4c4c4c'),
            edgecolor='white',
            linewidth=0.4,
            alpha=0.95
        )

    ax4.set_title('Comparativo mensual por categoría')
    ax4.set_xticks(x_positions)
    ax4.set_xticklabels(date_labels, rotation=45, ha='right')
    ax4.set_xlim(-0.6, len(date_labels) - 0.4)
    ax4.legend(
        fontsize=8,
        ncol=min(category_count, 4),
        loc='upper right'
    )
    ax4.grid(True, axis='y', linestyle='--', alpha=0.4)

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
