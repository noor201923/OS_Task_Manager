processes = []

def add_process():
    pid = input("Enter Process ID: ")
    if any(p['pid'] == pid for p in processes):
        print("Process ID already exists. Try again.\n")
        return
    burst_time = int(input("Enter Burst Time: "))
    arrival_time = int(input("Enter Arrival Time: "))
    processes.append({'pid': pid, 'burst_time': burst_time, 'arrival_time': arrival_time})
    print(f"Process {pid} added successfully.\n")

def view_processes():
    if not processes:
        print("No processes to display.\n")
        return
    print("\nProcesses:")
    print("PID\tBurst Time\tArrival Time")
    for p in processes:
        print(f"{p['pid']}\t{p['burst_time']}\t\t{p['arrival_time']}")
    print()

def edit_process():
    pid = input("Enter Process ID to edit: ")
    for p in processes:
        if p['pid'] == pid:
            print(f"Current Burst Time: {p['burst_time']}")
            new_burst = int(input("Enter new Burst Time: "))
            print(f"Current Arrival Time: {p['arrival_time']}")
            new_arrival = int(input("Enter new Arrival Time: "))
            p['burst_time'] = new_burst
            p['arrival_time'] = new_arrival
            print(f"Process {pid} updated successfully.\n")
            return
    print("Process not found.\n")

def delete_process():
    pid = input("Enter Process ID to delete: ")
    for p in processes:
        if p['pid'] == pid:
            processes.remove(p)
            print(f"Process {pid} deleted successfully.\n")
            return
    print("Process not found.\n")

def simulate_fcfs():
    if not processes:
        print("No processes to schedule.\n")
        return

    proc_sorted = sorted(processes, key=lambda x: x['arrival_time'])
    current_time = 0
    total_tat = 0
    total_wt = 0
    gantt_chart = []

    print("\nFCFS Scheduling:")
    print()
    print("PID\tArrival\tBurst\tStart\tFinish\tTAT\tWT")

    for p in proc_sorted:
        start = max(current_time, p['arrival_time'])
        finish = start + p['burst_time']
        tat = finish - p['arrival_time']
        wt = tat - p['burst_time']
        total_tat += tat
        total_wt += wt
        gantt_chart.append((p['pid'], start, finish))

        print(f"{p['pid']}\t{p['arrival_time']}\t{p['burst_time']}\t{start}\t{finish}\t{tat}\t{wt}")
        current_time = finish

    avg_tat = total_tat / len(proc_sorted)
    avg_wt = total_wt / len(proc_sorted)

    print("\nGantt Chart:")
    print()
    for pid, start, finish in gantt_chart:
        print(f"| {pid} ", end="")
    print("|")
    for pid, start, finish in gantt_chart:
        print(f"{start}\t", end="")
    print(f"{gantt_chart[-1][2]}")

    print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
    print(f"Average Waiting Time   : {avg_wt:.2f}\n")




def simulate_sjf():
    if not processes:
        print("No processes to schedule.\n")
        return

    proc_sorted = processes[:]  # No need to sort initially
    completed = []
    time_now = 0
    ready_queue = []
    total_tat = 0
    total_wt = 0
    gantt_chart = []

    print("\nSJF Scheduling:")
    print()
    print("PID\tArrival\tBurst\tStart\tFinish\tTAT\tWT")

    while len(completed) < len(proc_sorted):
        for p in proc_sorted:
            if p not in completed and p['arrival_time'] <= time_now and p not in ready_queue:
                ready_queue.append(p)

        if ready_queue:
            ready_queue.sort(key=lambda x: (x['burst_time'], x['arrival_time'], x['pid']))
            current = ready_queue.pop(0)
            start = max(time_now, current['arrival_time'])
            finish = start + current['burst_time']
            tat = finish - current['arrival_time']
            wt = tat - current['burst_time']
            total_tat += tat
            total_wt += wt
            gantt_chart.append((current['pid'], start, finish))

            print(f"{current['pid']}\t{current['arrival_time']}\t{current['burst_time']}\t{start}\t{finish}\t{tat}\t{wt}")
            time_now = finish
            completed.append(current)
        else:
            time_now += 1

    avg_tat = total_tat / len(proc_sorted)
    avg_wt = total_wt / len(proc_sorted)

    print("\nGantt Chart:")
    print()
    for pid, start, finish in gantt_chart:
        print(f"| {pid} ", end="")
    print("|")
    for pid, start, finish in gantt_chart:
        print(f"{start}\t", end="")
    print(f"{gantt_chart[-1][2]}")

    print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
    print(f"Average Waiting Time   : {avg_wt:.2f}\n")



def simulate_rr():
    if not processes:
        print("No processes to schedule.\n")
        return

    # Input quantum with validation
    while True:
        try:
            quantum = int(input("Enter Time Quantum: "))
            if quantum <= 0:
                print("Quantum must be a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    # Sort processes by arrival time
    proc_queue = sorted(processes, key=lambda x: x['arrival_time'])
    n = len(proc_queue)

    rem_bt = [p['burst_time'] for p in proc_queue]     # Remaining burst time
    arrival_times = [p['arrival_time'] for p in proc_queue]
    completed = [False] * n
    start_finish_log = [[] for _ in range(n)]          # Track start & finish times for each process

    t = min(p['arrival_time'] for p in proc_queue)
    # Current time
    queue = [] # Ready queue storing indices of processes
    visited = [False] * n   # Track if process has been enqueued for the first time

    print("\nRound Robin Scheduling:")
    print()
    print("PID\tArrival\tBurst\tStart\tFinish")

    # Enqueue all processes that have arrived at time 0
    i = 0
    while i < n and proc_queue[i]['arrival_time'] <= t:
        queue.append(i)
        visited[i] = True
        i += 1

    while queue:
        idx = queue.pop(0)
        start = t

        # Execute process for quantum or remaining time whichever is smaller
        if rem_bt[idx] > quantum:
            t += quantum
            rem_bt[idx] -= quantum
        else:
            t += rem_bt[idx]
            rem_bt[idx] = 0
            completed[idx] = True

        finish = t
        start_finish_log[idx].append((start, finish))

        print(f"{proc_queue[idx]['pid']}\t{proc_queue[idx]['arrival_time']}\t{proc_queue[idx]['burst_time']}\t{start}\t{finish}")

        # Enqueue new processes that have arrived by current time and not visited yet
        for j in range(n):
            if not visited[j] and proc_queue[j]['arrival_time'] <= t:
                queue.append(j)
                visited[j] = True

        # Re-enqueue current process if not completed
        if not completed[idx]:
            queue.append(idx)

        # If queue is empty, jump time to next arrival process not visited yet
        if not queue:
            for j in range(n):  # <-- fixed here, was range(i, n)
                if not visited[j]:
                    t = max(t, proc_queue[j]['arrival_time'])
                    queue.append(j)
                    visited[j] = True
                    break

    # Print Summary Table
    total_tat = 0
    total_wt = 0
    print("\nSummary:")
    print()
    print("PID\tArrival\tBurst\tFinish\tTAT\tWT")
    for i in range(n):
        if not start_finish_log[i]:  # Process never executed
            print(f"{proc_queue[i]['pid']}\t{proc_queue[i]['arrival_time']}\t{proc_queue[i]['burst_time']}\tN/A\tN/A\tN/A")
            continue

        arrival = proc_queue[i]['arrival_time']
        burst = proc_queue[i]['burst_time']
        finish = start_finish_log[i][-1][1]
        tat = finish - arrival
        executed_time = sum(f - s for s, f in start_finish_log[i])
        wt = tat - burst
        total_tat += tat
        total_wt += wt
        print(f"{proc_queue[i]['pid']}\t{arrival}\t{burst}\t{finish}\t{tat}\t{wt}")

    valid_count = sum(1 for log in start_finish_log if log)
    if valid_count > 0:
        avg_tat = total_tat / valid_count
        avg_wt = total_wt / valid_count
        print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
        print(f"Average Waiting Time   : {avg_wt:.2f}")
    else:
        print("\nNo processes were executed.")

    # Print Gantt Chart
    print("\nGantt Chart:")
    print()
    gantt = []
    for i in range(n):
        for start, finish in start_finish_log[i]:
            gantt.append((start, proc_queue[i]['pid'], finish))

    gantt.sort(key=lambda x: x[0])  # Sort by start time

    for start, pid, finish in gantt:
        print(f"| {pid} ", end="")
    print("|")

    for start, pid, finish in gantt:
        print(f"{start}\t", end="")
    print(f"{gantt[-1][2] if gantt else ''}\n")



def process_management_menu():
    while True:
        print("\n--- Process Management ---")
        print()
        print("1. Add Process")
        print("2. View Processes")
        print("3. Edit Process")
        print("4. Delete Process")
        print("5. Back to CPU Scheduling Menu")
        print()
        choice = input("Enter choice: ")
        print()
        if choice == '1':
            add_process()
        elif choice == '2':
            view_processes()
        elif choice == '3':
            edit_process()
        elif choice == '4':
            delete_process()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Try again.")

def scheduling_algorithms_menu():
    while True:
        print("\n--- Scheduling Algorithms ---")
        print()
        print("1. FCFS Scheduling")
        print("2. SJF Scheduling")
        print("3. Round Robin Scheduling")
        print("4. Back to CPU Scheduling Menu")
        print()
        choice = input("Enter choice: ")
        print()
        if choice == '1':
            simulate_fcfs()
        elif choice == '2':
            simulate_sjf()
        elif choice == '3':
            simulate_rr()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

def cpu_scheduling_menu():
    while True:
        print("\n--- CPU Scheduling Simulator ---")
        print()

        print("1. Process Management")
        print("2. Scheduling Algorithms")
        print("3. Back to Main Menu")
        print()
        choice = input("Enter choice: ")
        print()
        if choice == '1':
            process_management_menu()
        elif choice == '2':
            scheduling_algorithms_menu()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    cpu_scheduling_menu()
      