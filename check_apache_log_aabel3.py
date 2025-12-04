#!/usr/bin/env python3

# OPS435 Assignment 1
# check_apache_log_aabel3.py
# Author: Avraham Abel

import sys
import re

# Global list to store all log lines
all_log_lines = []

def load_logs(file_list):
    """Loads all lines from the given log files into the global list all_log_lines."""
    global all_log_lines
    for filename in file_list:
        print(f"Loading {filename}")
        try:
            with open(filename, 'r') as f:
                all_log_lines.extend(f.readlines())
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")

def display_title(title):
    """Displays a formatted title with matching equal signs."""
    print(title)
    print("=" * len(title))

def main_menu():
    """Displays the main menu and handles navigation."""
    while True:
        display_title("Apache Log Analyser - Main Menu")
        print("1) Successful Requests")
        print("2) Failed Requests")
        print("q) Quit")
        choice = input("What would you like to do? ").strip().lower()
        if choice == '1':
            successful_requests_menu()
        elif choice == '2':
            failed_requests_menu()
        elif choice == 'q':
            break
        else:
            print("Invalid option. Try again.")

def successful_requests_menu():
    """Displays submenu for successful request analysis."""
    while True:
        display_title("Apache Log Analyser - Successful Requests Menu")
        print("1) How many total requests (Code 200)")
        print("2) How many requests from Seneca (IPs starting with 142.204)")
        print("3) How many requests for OPS435_Lab")
        print("q) Return to Main Menu")
        choice = input("What would you like to do? ").strip().lower()
        if choice == '1':
            total_requests_200()
        elif choice == '2':
            requests_from_seneca()
        elif choice == '3':
            requests_for_ops435_lab()
        elif choice == 'q':
            break
        else:
            print("Invalid option. Try again.")

def failed_requests_menu():
    """Displays submenu for failed request analysis."""
    while True:
        display_title("Apache Log Analyser - Failed Requests Menu")
        print("1) How many total \"Not Found\" requests (Code 404)")
        print("2) How many 404 requests contained \"hidebots\" in the URL")
        print("3) Print all IP addresses that caused a 404 response")
        print("q) Return to Main Menu")
        choice = input("What would you like to do? ").strip().lower()
        if choice == '1':
            total_requests_404()
        elif choice == '2':
            requests_with_hidebots()
        elif choice == '3':
            ip_addresses_404()
        elif choice == 'q':
            break
        else:
            print("Invalid option. Try again.")

def total_requests_200():
    """Counts and prints total requests with HTTP status code 200."""
    global all_log_lines
    count = 0
    for line in all_log_lines:
        match = re.match(r'([\d\.]+) - - \[(.*?)\] "(.*?)" (\d+) ((\d+)|-).*', line)
        if match and match.group(4) == '200':
            count += 1
    print(f"Total successful requests (200): {count}")

def requests_from_seneca():
    """Counts and prints requests from IPs starting with 142.204."""
    global all_log_lines
    count = 0
    for line in all_log_lines:
        match = re.match(r'([\d\.]+) - - \[(.*?)\] "(.*?)" (\d+) ((\d+)|-).*', line)
        if match and match.group(1).startswith("142.204"):
            count += 1
    print(f"Requests from Seneca IPs (142.204.*): {count}")

def requests_for_ops435_lab():
    """Counts and prints requests containing 'OPS435_Lab' in the URL."""
    global all_log_lines
    count = 0
    for line in all_log_lines:
        match = re.match(r'([\d\.]+) - - \[(.*?)\] "(.*?)" (\d+) ((\d+)|-).*', line)
        if match and "OPS435_Lab" in match.group(3):
            count += 1
    print(f"Requests for OPS435_Lab: {count}")

def total_requests_404():
    """Counts and prints total requests with HTTP status code 404."""
    global all_log_lines
    count = 0
    for line in all_log_lines:
        match = re.match(r'([\d\.]+) - - \[(.*?)\] "(.*?)" (\d+) ((\d+)|-).*', line)
        if match and match.group(4) == '404':
            count += 1
    print(f"Total 'Not Found' requests (404): {count}")

def requests_with_hidebots():
    """Counts and prints 404 requests that contain 'hidebots' in the URL."""
    global all_log_lines
    count = 0
    for line in all_log_lines:
        match = re.match(r'([\d\.]+) - - \[(.*?)\] "(.*?)" (\d+) ((\d+)|-).*', line)
        if match and match.group(4) == '404' and "hidebots" in match.group(3):
            count += 1
    print(f"404 requests with 'hidebots': {count}")

def ip_addresses_404():
    """Prints all unique IP addresses that caused a 404 response."""
    global all_log_lines
    ip_dict = {}
    for line in all_log_lines:
        match = re.match(r'([\d\.]+) - - \[(.*?)\] "(.*?)" (\d+) ((\d+)|-).*', line)
        if match and match.group(4) == '404':
            ip_dict[match.group(1)] = True
    print("IP addresses that caused 404:")
    for ip in ip_dict.keys():
        print(ip)

# Main Script
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Error: No arguments provided.")
        sys.exit(1)

    if args[0] in ['--default', '-d']:
        if len(args) < 2:
            print("Error: No filenames provided with --default.")
            sys.exit(1)
        load_logs(args[1:])
        total_requests_200()
    else:
        load_logs(args)
        main_menu()
