import random

MAX_LINES = 3
MIN_BET = 1
MAX_BET = 500

ROWS = 3
COLS = 3

symbol_count = {
    'A' : 2,
    'B' : 4,
    'C' : 6,
    'D' : 8
}

symbol_value = {
    'A' : 5,
    'B' : 4,
    'C' : 3,
    'D' : 2
}

#fn to get a randomised value set for each spin
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

#fn to display the spin result to the user
def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()

#fn to check if the user has gotten any winning value set
def check_winnings(cols, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = cols[0][line]
        for column in cols:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(lines)
    return winnings, winning_lines

#fn to ask user to deposit money initially
def deposit_money():
    while True:
        amount = input("How much money would you like to deposit? ")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Please input an amount greater than 0.")
        else:
            print("Please enter a number.")
    return amount

#fn to ask user number of lines they want to bet on
def num_lines():
    while True:
        lines = input("Enter the number of lines to bet on (min: 1, max:" + str(MAX_LINES) + ") ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Please input a number in the asked range.")
        else:
            print("Please enter a number.")
    return lines

#fn to take the user's bet amount per line
def get_bet():
    while True:
        bet = input(f"Enter the amount to bet (min: {MIN_BET}, max: {MAX_BET}) per line. ")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            else:
                print("Please input a BET AMOUNT in the asked range.")
        else:
            print("Please enter a number.")
    return bet

#primary fn that takes the number of lines and bet and gets the game moving
def slot_game(balance):
    lines = num_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if(total_bet > balance) :
            print(f"You cannot place a bet higher than your balance. Your balance: {balance}, your total bet: {total_bet}.")
        else:
            break
    print(f"You have placed a bet of {total_bet} on {lines} lines.")
    
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print("Winning lines:" + str(winning_lines))
    print(f"You have won ${winnings}!") if winnings else print("Sorry, you lost this round.")
    return winnings - total_bet

def main():
    balance = deposit_money()
    while True:
        print(f"Current balance is ${balance}.")
        ans = input("Do you want to continue playing? Press Enter to continue or N to quit.")
        if ans == "N" or ans == "n":
            break
        #update user's current balance
        balance += slot_game(balance)

main()