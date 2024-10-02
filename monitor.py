from tools.emoticons import *
from tools.moneyStatus import getTotalBlue, getTotalRed, getCurrentMoney
from tools.notion import get_notion_count


def monitor():
    # last print 
    print(f'[{moneyRed}{getTotalRed()} {money}{getCurrentMoney()}]'.expandtabs(2), end='')
    print(f'')


if __name__ == '__main__':
    monitor()
