import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from setup import get_current_money, get_totals, current_row


def create_pie_chart(data, title=''):
    plt.figure(figsize=(6, 6))
    plt.pie(data[2], labels=data[0], autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.tight_layout()
    plt.savefig('monitor2_output.png')
    print('Graph saved to monitor2_output.png')


def main():
    try:
        limit = int(sys.argv[1])
        if limit > current_row:
            print('Argument out of range. Using current row.')
            limit = current_row
    except (IndexError, ValueError):
        limit = current_row

    data = get_totals(limit)
    get_current_money()
    create_pie_chart(data, f'Distribucion hasta fila {limit}')


if __name__ == '__main__':
    main()
