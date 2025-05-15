import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
from setup import get_current_money, get_totals, current_row, df

try:
    args = sys.argv
    limit = int(args[1])

    if limit > current_row:
        print('Argument out of range.')
    else:
        totals_data = get_totals(limit)
except:
    totals_data = get_totals(current_row)

categories = totals_data[0]
total_money = totals_data[1]
percent = totals_data[2]

my_money = get_current_money()

mpl.rcParams['font.family'] = 'Helvetica Neue'
title_fontsize = 20
label_fontsize = 14
autopct_fontsize = 12


# Filtramos categorías con valor 0 para evitar NaN o % inválidos
filtered = [(cat, val) for cat, val in zip(categories, total_money) if val > 0]
filtered_categories, filtered_values = zip(*filtered)

# Colores bonitos (Apple style)
colors = [
    '#8dbad6',  # Savings
    '#9bc2e7',  # Setup
    '#8ea9db',  # Home
    '#abb9d4',  # Studies
    '#b9f5c4',  # Enjoy
    '#fd9a9a',  # Others
    '#f8ccad',  # Fixed
    '#fef2cb',  # Cashout
]
# Cortamos a solo las categorías que se están usando
used_colors = colors[-len(filtered_values):]  # asegura emparejamiento

# Dibujamos el gráfico
plt.figure(figsize=(6, 6))
wedges, texts, autotexts = plt.pie(
    filtered_values,
    labels=filtered_categories,
    autopct='%1.1f%%',  # <- Este es el formato correcto
    startangle=90,
    colors=used_colors,
    wedgeprops={'edgecolor': 'white', 'linewidth': 1}
)

# Estilo del texto
for text in texts:
    text.set_fontsize(14)
    text.set_fontweight('medium')
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_fontweight('bold')

# Título grande y en negrita, estilo Apple
plt.title(f"Distribución de gastos desde {df['Date'][limit]}", fontsize=20, fontweight='bold')
plt.axis('equal')  # Mantiene forma circular
plt.tight_layout()
plt.show()