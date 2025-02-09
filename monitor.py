import sys
from setup import get_current_money, get_totals_report


try:
    args = sys.argv
    limit = int(args[1])
    get_totals_report(limit)
except:
    get_totals_report()

get_current_money()

