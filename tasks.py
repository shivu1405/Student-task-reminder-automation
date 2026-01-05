from datetime import datetime
from colorama import init, Fore

init(autoreset=True)  # ensures colors reset after each print

def read_tasks():
    tasks = []
    try:
        with open("tasks.csv", "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.lower().startswith("task"):
                    continue  # skip header or empty lines
                task, deadline = line.split(",")
                tasks.append({"task": task, "deadline": deadline})
    except FileNotFoundError:
        pass
    return tasks

def categorize_tasks(tasks):
    overdue = []
    due_soon = []
    later = []

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

    # Optional: export summary to text file
    if export:
        with open("summary.txt", "w") as f:
            f.write("TASK SUMMARY\n\n")
            f.write("Overdue Tasks:\n")
            f.writelines([f"{t['task']} (Deadline: {t['deadline']})\n" for t in overdue] or ["None\n"])
            f.write("\nTasks Due Soon:\n")
            f.writelines([f"{t['task']} (Deadline: {t['deadline']})\n" for t in due_soon] or ["None\n"])
            f.write("\nLater Tasks:\n")
            f.writelines([f"{t['task']} (Deadline: {t['deadline']})\n" for t in later] or ["None\n"])

