def first_fit(block_sizes, process_sizes):
    allocation = [-1] * len(process_sizes)
    for i in range(len(process_sizes)):
        for j in range(len(block_sizes)):
            if block_sizes[j] >= process_sizes[i]:
                allocation[i] = j
                block_sizes[j] -= process_sizes[i]
                break
    return allocation

def best_fit(block_sizes, process_sizes):
    allocation = [-1] * len(process_sizes)
    for i in range(len(process_sizes)):
        best_idx = -1
        for j in range(len(block_sizes)):
            if block_sizes[j] >= process_sizes[i]:
                if best_idx == -1 or block_sizes[j] < block_sizes[best_idx]:
                    best_idx = j
        if best_idx != -1:
            allocation[i] = best_idx
            block_sizes[best_idx] -= process_sizes[i]
    return allocation

def display_allocation(process_sizes, allocation):
    print("\nProcess No.\tProcess Size\tBlock No.")
    for i in range(len(process_sizes)):
        if allocation[i] != -1:
            print(f"{i+1}\t\t{process_sizes[i]}\t\t{allocation[i]+1}")
        else:
            print(f"{i+1}\t\t{process_sizes[i]}\t\tNot Allocated")

def main():
    while True:
        print("\n--- Memory Management Simulator ---")
        print()
        print("1. First Fit")
        print("2. Best Fit")
        print("3. Back to Main Menu")
        print()
        choice = input("Enter your choice: ")
        print()

        if choice == '1' or choice == '2':
            n_blocks = int(input("Enter number of memory blocks: "))
            block_sizes = []
            for i in range(n_blocks):
                size = int(input(f"Enter size of block {i+1}: "))
                block_sizes.append(size)
            n_processes = int(input("Enter number of processes: "))
            process_sizes = []
            for i in range(n_processes):
                size = int(input(f"Enter size of process {i+1}: "))
                process_sizes.append(size)

            if choice == '1':
                allocation = first_fit(block_sizes[:], process_sizes)
                print("\nFirst Fit Allocation:")
            else:
                allocation = best_fit(block_sizes[:], process_sizes)
                print("\nBest Fit Allocation:")

            display_allocation(process_sizes, allocation)
            input("\nPress Enter to continue...")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
