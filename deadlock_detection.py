def input_matrix(name, n, r):
    print(f"Enter {name} matrix (space separated):")
    matrix = []
    for i in range(n):
        row = list(map(int, input(f"Row {i + 1}: ").strip().split()))
        if len(row) != r:
            raise ValueError(f"Error: Row {i+1} of {name} matrix must contain exactly {r} values.")
        matrix.append(row)
    return matrix

def deadlock_detection():
    try:
        n = int(input("Enter number of processes: "))
        r = int(input("Enter number of resources: "))

        allocation = input_matrix("Allocation", n, r)
        max_demand = input_matrix("Max", n, r)

        print("Enter Available vector:")
        available = list(map(int, input().strip().split()))
        if len(available) != r:
            raise ValueError(f"Error: Available vector must contain exactly {r} values.")

        # Validation: Allocation should not exceed Max
        errors=[]
        for i in range(n):
            for j in range(r):
                if allocation[i][j] > max_demand[i][j]:
                    errors.append(f"Allocation for P{i}, Resource {j} is {allocation[i][j]}, but max is {max_demand[i][j]}.") 
                    if errors:
                        raise ValueError("Allocation exceeds Max in the following cases:\n" + "\n".join(errors)) 

        need = [[max_demand[i][j] - allocation[i][j] for j in range(r)] for i in range(n)]
        finish = [False] * n
        safe_sequence = []

        print("\nCalculating safe sequence...\n")
        while True:
            done_something = False
            for i in range(n):
                if not finish[i]:
                    if all(need[i][j] <= available[j] for j in range(r)):
                        for j in range(r):
                            available[j] += allocation[i][j]
                        finish[i] = True
                        safe_sequence.append(i)
                        done_something = True
            if not done_something:
                break

        if all(finish):
            print("No deadlock detected.")
            print("Safe sequence is:", ' -> '.join([f"P{p}" for p in safe_sequence]))
        else:
            print("Deadlock detected!")
            print("Processes involved:", ' '.join([f"P{i}" for i in range(n) if not finish[i]]))

    except ValueError as ve:
        print("\nInput Error:", ve)
    except Exception as e:
        print("\nUnexpected Error:", e)

    input("\nPress Enter to continue...")

def main():
    while True:
        print("\n--- Deadlock Detection Simulator ---")
        print("1. Run Deadlock Detection")
        print("2. Back to Main Menu")
        choice = input("\nEnter your choice: ")
        if choice == '1':
            deadlock_detection()
        elif choice == '2':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
