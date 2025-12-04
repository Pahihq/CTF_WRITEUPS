#!/usr/bin/env python3
import os
import random
import sys
from colorama import Fore, Style, init

init(autoreset=True)

FLAG = os.getenv("FLAG", "FLAG{default_flag_value}")
FLAG_PRICE = 1000
START_COINS = 100.0


def banner():
    print(f"{Fore.CYAN}{Style.BRIGHT}\n==============================")
    print("    🎰 Welcome to the Lottery Shop! 🎰")
    print("==============================\n" + Style.RESET_ALL)


def flagforyou():
    print(f"\n{Fore.GREEN}{Style.BRIGHT}*** Here is your flag: {FLAG} ***\n")


def noflagforyou():
    print(f"{Fore.RED}No flag for you.\n")


def safe_int(x):
    """Try converting input to int, raise error if not possible."""
    try:
        return int(x)
    except Exception:
        raise


# === Main Game Logic ===
def main():
    coins = START_COINS
    banner()
    print(f"{Fore.YELLOW}You start with {coins} coins.")
    print(f"The flag costs {FLAG_PRICE} coins.{Style.RESET_ALL}\n")

    while True:
        print(f"{Fore.MAGENTA}{Style.BRIGHT}Menu:")
        print("  1) Play a round (bet & guess)")
        print("  2) Buy the flag")
        print("  3) Check coins")
        print("  4) Quit" + Style.RESET_ALL)
        choice = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip()

        if choice == "1":
            print(f"\n{Fore.BLUE}{Style.BRIGHT}--- New Round ---{Style.RESET_ALL}")
            try:
                bet = float(input("Enter your bet amount: ").strip())
            except ValueError:
                print(f"{Fore.RED}Invalid bet amount.\n")
                continue

            if bet > coins:
                print(f"{Fore.RED}Invalid bet. BET: {bet} > COINS: {coins}\n")
                continue
            
            try:
                guess = int(input("Enter your guess number: ").strip())
            except ValueError:
                print(f"{Fore.RED}Invalid guess. Please enter an integer.\n")
                continue

            winning = random.randint(0, 1_000_000)

            if guess == winning:
                coins += bet * 2
                print(f"{Fore.GREEN}🎉 You guessed it! You win {bet * 2} coins!")
                print(f"New balance: {coins}\n")
            else:
                coins -= bet
                print(f"{Fore.RED}❌ Wrong guess! The winning number was {winning}.")
                print(f"You lose {bet} coins. New balance: {coins}\n")

        elif choice == "2":
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- Buy the flag ---{Style.RESET_ALL}")
            if coins >= FLAG_PRICE:
                coins -= FLAG_PRICE
                flagforyou()
                print(f"{Fore.CYAN}Thanks for playing! Exiting...\n")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Not enough coins. You have {coins}, need {FLAG_PRICE}.\n")

        elif choice == "3":
            print(f"\n{Fore.GREEN}💰 You have {coins} coins.\n")

        elif choice == "4":
            print(f"{Fore.CYAN}Goodbye! 👋")
            break

        else:
            print(f"{Fore.RED}Invalid option.\n")


if __name__ == "__main__":
    main()
