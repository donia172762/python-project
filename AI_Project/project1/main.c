

import tkinter as tk
from tkinter import messagebox
from delivery_data import Package, Vehicle
from simulated import simulated_annealing
from Gentic import genetic_algorithm
from utils import total_cost, euclidean_distance
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import matplotlib.pyplot as plt
import random

SEED_VALUE = 42



def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]

    vehicle_info = list(map(int, lines[0].split()))
    num_vehicles, vehicle_capacity = vehicle_info[0], vehicle_info[1]

    num_packages = int(lines[1])
    packages = []
    for i in range(num_packages):
        x, y, weight, priority = map(int, lines[2 + i].split())
        packages.append(Package(i, x, y, weight, priority))

    vehicles = [Vehicle(i, vehicle_capacity) for i in range(num_vehicles)]

    return packages, vehicles


def plot_routes(vehicles, canvas_frame):
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(0, 0, 'ko', label='Depot')

    for i, v in enumerate(vehicles):
        if not v.packages:
            continue
        x_vals, y_vals = [0], [0]
        for pkg in v.packages:
            x_vals.append(pkg.x)
            y_vals.append(pkg.y)
            ax.plot(pkg.x, pkg.y, 'ks')
        x_vals.append(0)
        y_vals.append(0)
        ax.plot(x_vals, y_vals, marker='o', color=colors[i % len(colors)], label=f'Vehicle {v.id}')

    ax.set_title('Delivery Routes')
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.legend()
    ax.grid(True)
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 110)

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



def run_algorithm_from_selection():
    selection = algo_var.get()
    try:
        cooling_rate = float(cooling_entry.get())
        mutation_rate = float(mutation_entry.get())
        generations = int(generations_entry.get())
        population_size = int(population_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid values for parameters.")
        return

    if selection == "ga_random":
        run_algorithm(True, False, mutation_rate=mutation_rate, generations=generations, population_size=population_size)
    elif selection == "sa_random":
        run_algorithm(False, False, cooling_rate=cooling_rate)


def run_algorithm(use_ga, fixed_result, mutation_rate=0.05, cooling_rate=0.95, generations=500, population_size=100):
    if fixed_result:
        random.seed(SEED_VALUE)
    else:
        random.seed(None)

    try:
        packages, vehicles = read_input_file('input.txt')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read input.txt: {e}")
        return

    start_time = time.time()
    if use_ga:
        result = genetic_algorithm(packages, vehicles, mutation_rate=mutation_rate, generations=generations, population_size=population_size)
        algo = "Genetic Algorithm"
    else:
        result = simulated_annealing(packages, vehicles, cooling_rate=cooling_rate)
        algo = "Simulated Annealing"
    elapsed = time.time() - start_time

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"\n📊 Results using {algo} (Random):\n")
    for v in result:
        output_text.insert(tk.END, f"\n🚚 Vehicle {v.id} (Total Weight: {v.total_weight()} / {v.capacity}):\n")
        for pkg in v.packages:
            output_text.insert(tk.END, f"  📦 Package {pkg.id} → Location ({pkg.x}, {pkg.y}) | Weight: {pkg.weight} | Priority: {pkg.priority}\n")
    output_text.insert(tk.END, f"\n📏 Total distance cost: {total_cost(result):.2f} km")
    output_text.insert(tk.END, f"\n⏱️ Execution Time: {elapsed:.2f} seconds\n")

    plot_routes(result, canvas_frame)


root = tk.Tk()
root.title("Delivery Optimization")
root.geometry("1200x700")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

label = tk.Label(left_frame, text="Choose Algorithm and Mode:", font=("Arial", 13, "italic", "bold"), fg="#2a7fba")
label.pack(pady=10)

algo_var = tk.StringVar()
algo_var.set("ga_random")

options = [
    ("Genetic Algorithm (Random)", "ga_random"),
    ("Simulated Annealing (Random)", "sa_random")
]

for text, value in options:
    tk.Radiobutton(left_frame, text=text, variable=algo_var, value=value, font=("Arial", 11, "bold"), command=lambda: toggle_params()).pack(anchor="w")

params_label = tk.Label(left_frame, text="Algorithm Parameters:", font=("Arial", 12, "underline"), fg="#444")
params_label.pack(pady=10)


sa_frame = tk.Frame(left_frame)
cooling_label = tk.Label(sa_frame, text="Cooling Rate (SA):")
cooling_label.pack(anchor="w")
cooling_entry = tk.Entry(sa_frame)
cooling_entry.insert(0, "0.95")
cooling_entry.pack(fill=tk.X)


ga_frame = tk.Frame(left_frame)
mutation_label = tk.Label(ga_frame, text="Mutation Rate (GA):")
mutation_label.pack(anchor="w")
mutation_entry = tk.Entry(ga_frame)
mutation_entry.insert(0, "0.05")
mutation_entry.pack(fill=tk.X)

generations_label = tk.Label(ga_frame, text="Generations (GA):")
generations_label.pack(anchor="w")
generations_entry = tk.Entry(ga_frame)
generations_entry.insert(0, "500")
generations_entry.pack(fill=tk.X)

population_label = tk.Label(ga_frame, text="Population Size (GA):")
population_label.pack(anchor="w")
population_entry = tk.Entry(ga_frame)
population_entry.insert(0, "100")
population_entry.pack(fill=tk.X)

def toggle_params():
    if algo_var.get() == "ga_random":
        sa_frame.pack_forget()
        ga_frame.pack(fill=tk.X)
    else:
        ga_frame.pack_forget()
        sa_frame.pack(fill=tk.X)

toggle_params()

run_button = tk.Button(left_frame, text="Run", width=20, command=run_algorithm_from_selection)
run_button.pack(pady=15)

middle_frame = tk.Frame(main_frame)
middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

output_text = tk.Text(middle_frame, wrap=tk.WORD, font=("Courier New", 10))
output_text.pack(fill=tk.BOTH, expand=True)

canvas_frame = tk.Frame(main_frame, width=500, height=500)
canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

root.mainloop()
