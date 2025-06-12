#!/bin/bash

print_centered_line() {
  local text="$1"
  local term_width=$(tput cols)
  local text_length=${#text}
  local padding=$(( (term_width - text_length) / 2 ))
  printf "%*s%s\n" "$padding" "" "$text"
}

print_aligned_menu_option() {
  local num="$1"
  local text="$2"
  local term_width=$(tput cols)
  local line=" $num. $text"
  local line_length=${#line}
  local padding=$(( (term_width - line_length) / 2 ))
  printf "%*s%s\n" "$padding" "" "$line"
}

while true; do
  clear
  echo
  print_centered_line "=============================="
  print_centered_line " OS Project Simulation Menu "
  print_centered_line "=============================="
  echo

  print_aligned_menu_option 1 "CPU Scheduling Simulator"
  print_aligned_menu_option 2 "Memory Management Simulator"
  print_aligned_menu_option 3 "Deadlock Detection Simulator"
  print_aligned_menu_option 4 "Exit"

  echo
  print_centered_line "------------------------------"
  echo
  echo
  read -p "Enter your choice [1-4]: " choice
  echo

  case $choice in
    1)
      print_centered_line "Running CPU Scheduling Simulator..."
      echo
      python scheduler.py
      echo
      read -p "Press Enter to return to menu..."
      ;;
    2)
      print_centered_line "Running Memory Management Simulator..."
      echo
      python memory_allocation.py
      echo
      read -p "Press Enter to return to menu..."
      ;;
    3)
      print_centered_line "Running Deadlock Detection Simulator..."
      echo
      python deadlock_detection.py
      echo
      read -p "Press Enter to return to menu..."
      ;;
    4)
      echo
      print_centered_line "Exiting. Goodbye!"
      echo
      break
      ;;
    *)
      print_centered_line "Invalid choice. Try again."
      sleep 1
      ;;
  esac
done
