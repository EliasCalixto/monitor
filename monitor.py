import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
from setup import get_current_money, get_totals, current_row, df

try:
    try:
        args = sys.argv
        start = int(args[1])
        end = int(args[2])

        if start > current_row:
            print('Argument out of range.')
        else:
            totals_data = get_totals(start, end)
    except:
        args = sys.argv
        start = int(args[1])
        end = start
        
        if start > current_row:
            print('Argument out of range.')
        else:
            totals_data = get_totals(start, end)
except:
    start = current_row
    end = current_row
    totals_data = get_totals(start, end)

categories = totals_data[0]
total_money = totals_data[1]
percent = totals_data[2]

my_money = get_current_money()

mpl.rcParams['font.family'] = 'Helvetica Neue'

# Filtramos categorías con valor 0 para evitar NaN o % inválidos
filtered = [(cat, val) for cat, val in zip(categories, total_money) if val > 0]
filtered_categories, filtered_values = zip(*filtered)

# Colores bonitos (Apple style)
colors = {
    'Savings': '#8dbad6',  # Savings
    'Setup': '#9bc2e7',  # Setup
    'Home': '#8ea9db',  # Home
    'Studies': '#abb9d4',  # Studies
    'Enjoy': '#b9f5c4',  # Enjoy
    'Others': '#fd9a9a',  # Others
    'Fixed': '#f8ccad',  # Fixed
    'Cashout': '#fef2cb',  # Cashout
}
# Cortamos a solo las categorías que se están usando
used_colors = []
for i in filtered_categories:
    if i in colors:
        used_colors.append(colors[i])
    else:
        pass

# Dibujamos el gráfico
plt.figure(figsize=(6,5))
wedges, texts, autotexts = plt.pie(
    filtered_values,
    labels=filtered_categories,
    autopct='%1.1f%%',
    startangle=90,
    colors=used_colors,
    wedgeprops={'edgecolor': 'white', 'linewidth': 1}
)

# Estilo del texto
for text in texts:
    text.set_fontsize(10)
    text.set_fontweight('medium')
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight('bold')

last_result_date = df['Date'][end]

if start != end:
    plt.title(f"{df['Date'][start]} hasta {last_result_date}", fontsize=15, fontweight='bold')
else:
    plt.title(f"{df['Date'][start]}", fontsize=15, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()

# aqui poner una funcion bla bla bla