import time
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)

# ---------------- TASK FUNCTIONS ---------------- #
def read_tasks():
    tasks = []
    try:
        with open("tasks.csv", "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.lower().startswith("task"):
                    continue  # skip empty lines or header
                task, deadline = line.split(",")
                tasks.append({"task": task, "deadline": deadline})
    except FileNotFoundError:
        pass
    return tasks

def categorize_tasks(tasks):
    overdue, due_soon, later = [], [], []
    today = datetime.today().date()
    for t in tasks:
        try:
            deadline = datetime.strptime(t["deadline"], "%Y-%m-%d").date()
        except ValueError:
            print(Fore.RED + f"Skipping invalid date: {t['deadline']}")
            continue
        days_left = (deadline - today).days
        if days_left < 0:
            overdue.append(t)
        elif days_left <= 3:
            due_soon.append(t)
        else:
            later.append(t)
    return overdue, due_soon, later

def generate_summary(overdue, due_soon, later, export=False):
    print("\n" + Fore.CYAN + "TASK SUMMARY")

    print("\n" + Fore.RED + "Overdue Tasks:")
    if overdue:
        for t in overdue:
            print(Fore.RED + f"{t['task']} (Deadline: {t['deadline']})")
    else:
        print("None")

    print("\n" + Fore.YELLOW + "Tasks Due Soon (Within 3 Days):")
    if due_soon:
        for t in due_soon:
            print(Fore.YELLOW + f"{t['task']} (Deadline: {t['deadline']})")
    else:
        print("None")

    print("\n" + Fore.GREEN + "Later Tasks:")
    if later:
        for t in later:
            print(Fore.GREEN + f"{t['task']} (Deadline: {t['deadline']})")
    else:
        print("None")

    if export:
        with open("summary.txt", "w") as f:
            f.write("TASK SUMMARY\n\n")
            f.write("Overdue Tasks:\n")
            f.writelines([f"{t['task']} (Deadline: {t['deadline']})\n" for t in overdue] or ["None\n"])
            f.write("\nTasks Due Soon:\n")
            f.writelines([f"{t['task']} (Deadline: {t['deadline']})\n" for t in due_soon] or ["None\n"])
            f.write("\nLater Tasks:\n")
            f.writelines([f"{t['task']} (Deadline: {t['deadline']})\n" for t in later] or ["None\n"])

# ---------------- APP FUNCTIONS ---------------- #
def add_task():
    while True:
        task = input("Enter task name (leave blank to stop adding): ").strip()
        if not task:
            break
        while True:
            deadline = input("Enter deadline (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
                break
            except ValueError:
                print(Fore.RED + "Invalid date format. Please use YYYY-MM-DD.")
        with open("tasks.csv", "a") as file:
            file.write(f"{task},{deadline}\n")
        print(Fore.GREEN + "Task added successfully!")

def delete_task():
    tasks = read_tasks()
    if not tasks:
        print(Fore.RED + "No tasks to delete.")
        return
    for i, t in enumerate(tasks, 1):
        print(f"{i}. {t['task']} (Deadline: {t['deadline']})")
    while True:
        choice = input("Enter task number to delete: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(tasks):
            break
        print(Fore.RED + "Invalid choice. Try again.")
    tasks.pop(int(choice)-1)
    with open("tasks.csv", "w") as file:
        for t in tasks:
            file.write(f"{t['task']},{t['deadline']}\n")
    print(Fore.GREEN + "Task deleted successfully!")

def update_task():
    tasks = read_tasks()
    if not tasks:
        print(Fore.RED + "No tasks to update.")
        return
    for i, t in enumerate(tasks, 1):
        print(f"{i}. {t['task']} (Deadline: {t['deadline']})")
    while True:
        choice = input("Enter task number to update: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(tasks):
            task_index = int(choice)-1
            break
        print(Fore.RED + "Invalid choice. Try again.")

    new_name = input("Enter new task name (leave blank to keep current): ").strip()
    if new_name:
        tasks[task_index]["task"] = new_name
    while True:
        new_deadline = input("Enter new deadline (YYYY-MM-DD, leave blank to keep current): ").strip()
        if not new_deadline:
            break
        try:
            datetime.strptime(new_deadline, "%Y-%m-%d")
            tasks[task_index]["deadline"] = new_deadline
            break
        except ValueError:
            print(Fore.RED + "Invalid date format. Try again.")

    with open("tasks.csv", "w") as file:
        for t in tasks:
            file.write(f"{t['task']},{t['deadline']}\n")
    print(Fore.GREEN + "Task updated successfully!")

def show_reminders():
    tasks = read_tasks()
    _, due_soon, _ = categorize_tasks(tasks)
    if due_soon:
        print("\n" + Fore.MAGENTA + "🔔 REMINDERS: Tasks due soon!")
        for t in due_soon:
            print(Fore.YELLOW + f"{t['task']} | Deadline: {t['deadline']}")
    else:
        print("\n" + Fore.CYAN + "No upcoming tasks due soon. ✅")

# ---------------- MAIN LOOP ---------------- #
while True:
    try:
        show_reminders()
        print("\nSTUDENT TASK REMINDER")
        print("1. Add task")
        print("2. Generate summary")
        print("3. Delete task")
        print("4. Update task")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_task()
        elif choice == "2":
            tasks = read_tasks()
            overdue, due_soon, later = categorize_tasks(tasks)
            generate_summary(overdue, due_soon, later, export=True)
        elif choice == "3":
            delete_task()
        elif choice == "4":
            update_task()
        elif choice == "5":
            print(Fore.CYAN + "Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Try again.")
    except Exception as e:
        print(Fore.RED + f"Something went wrong: {e}")

    time.sleep(60)  # automatic reminder check every 60 seconds
