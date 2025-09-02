import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
from setup import get_current_money, get_totals, current_row, df
from arguments_helper import arguments

args = sys.argv # lee los argumentos de la línea de comandos

try:
    try:
        try:
            for key, value in arguments.items():
                if value == args[1]:
                    translated_arg1 = key
                if value == args[2]:
                    translated_arg2 = key
        except:
            translated_arg1 = args[1] # aca estamos fornzando un error, ya que args[1] no existe
            translated_arg2 = args[2] # idem
        
        start = int(translated_arg1)  # pyright: ignore[reportPossiblyUnboundVariable]
        end = int(translated_arg2) # pyright: ignore[reportPossiblyUnboundVariable]

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
            translated_arg1 = args[1] # aca estamos fornzando un error, ya que args[1] no existe
            
        start = int(translated_arg1) # pyright: ignore[reportPossiblyUnboundVariable]
        end = start
        
        if start > current_row:
            print('Argument out of range.')
        else:
            totals_data = get_totals(start, end)
except:
    start = current_row
    end = current_row
    totals_data = get_totals(start, end)

categories = totals_data[0] # type: ignore
total_money = totals_data[1] # type: ignore
percent = totals_data[2] # type: ignore

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
plt.figure(figsize=(7, 5))
bars = plt.bar(
    filtered_categories,
    filtered_values,
    color=used_colors,
    edgecolor='white',
    linewidth=1
)

# Estilo del texto en las barras
for bar, value in zip(bars, filtered_values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f'{value:.1f}',
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold'
    )

# Título
try:
    last_result_date = df['Date'][end]
    if start != end:
        plt.title(f"{df['Date'][start]} hasta {last_result_date}", fontsize=15, fontweight='bold')
    else:
        plt.title(f"{df['Date'][start]}", fontsize=15, fontweight='bold')
except:
    pass

plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.show()
