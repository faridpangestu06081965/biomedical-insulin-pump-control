import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PancreasSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Artificial Pancreas - PID Controller Simulator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # --- Gaya UI (Themed Tkinter) ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'))

        # --- Layout Utama ---
        self.left_panel = ttk.Frame(self.root, padding="20")
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.right_panel = ttk.Frame(self.root, padding="10")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Komponen Panel Kiri (Kontrol PID) ---
        ttk.Label(self.left_panel, text="PID Parameters", style='Header.TLabel').pack(pady=(0, 20))

        # Proportional (P)
        ttk.Label(self.left_panel, text="Proportional (Kp):").pack(anchor=tk.W)
        self.kp_var = tk.DoubleVar(value=0.5)
        self.kp_slider = ttk.Scale(self.left_panel, from_=0.0, to=5.0, variable=self.kp_var, orient=tk.HORIZONTAL, command=self.update_labels)
        self.kp_slider.pack(fill=tk.X, pady=(0, 5))
        self.kp_label = ttk.Label(self.left_panel, text="0.50")
        self.kp_label.pack(anchor=tk.E, pady=(0, 15))

        # Integral (I)
        ttk.Label(self.left_panel, text="Integral (Ki):").pack(anchor=tk.W)
        self.ki_var = tk.DoubleVar(value=0.02)
        self.ki_slider = ttk.Scale(self.left_panel, from_=0.0, to=0.5, variable=self.ki_var, orient=tk.HORIZONTAL, command=self.update_labels)
        self.ki_slider.pack(fill=tk.X, pady=(0, 5))
        self.ki_label = ttk.Label(self.left_panel, text="0.02")
        self.ki_label.pack(anchor=tk.E, pady=(0, 15))

        # Derivative (D)
        ttk.Label(self.left_panel, text="Derivative (Kd):").pack(anchor=tk.W)
        self.kd_var = tk.DoubleVar(value=0.5)
        self.kd_slider = ttk.Scale(self.left_panel, from_=0.0, to=5.0, variable=self.kd_var, orient=tk.HORIZONTAL, command=self.update_labels)
        self.kd_slider.pack(fill=tk.X, pady=(0, 5))
        self.kd_label = ttk.Label(self.left_panel, text="0.50")
        self.kd_label.pack(anchor=tk.E, pady=(0, 25))

        # Tombol Simulasi
        self.sim_btn = ttk.Button(self.left_panel, text="Run Simulation", command=self.run_simulation)
        self.sim_btn.pack(fill=tk.X, pady=10)

        # --- Komponen Panel Kanan (Grafik Matplotlib) ---
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax1 = self.figure.add_subplot(211)
        self.ax2 = self.figure.add_subplot(212)
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Jalankan simulasi pertama kali saat aplikasi dibuka
        self.run_simulation()

    def update_labels(self, event=None):
        self.kp_label.config(text=f"{self.kp_var.get():.2f}")
        self.ki_label.config(text=f"{self.ki_var.get():.3f}")
        self.kd_label.config(text=f"{self.kd_var.get():.2f}")

    def run_simulation(self):
        # Ambil nilai PID dari slider
        Kp = self.kp_var.get()
        Ki = self.ki_var.get()
        Kd = self.kd_var.get()

        # Setup Simulasi Waktu
        dt = 1.0
        time = np.arange(0, 200, dt)
        target_glucose = 90.0
        actual_glucose = np.ones(len(time)) * target_glucose
        insulin_delivery = np.zeros(len(time))

        integral_error = 0
        prev_error = 0

        # Loop Kontrol Diskrit
        for i in range(1, len(time)):
            meal_spike = 40.0 if time[i] == 60 else 0.0
            error = actual_glucose[i-1] - target_glucose
            
            integral_error += error * dt
            derivative_error = (error - prev_error) / dt
            
            insulin_dose = (Kp * error) + (Ki * integral_error) + (Kd * derivative_error)
            insulin_dose = max(0, insulin_dose) # Tidak bisa menyedot insulin
            insulin_delivery[i] = insulin_dose
            
            insulin_effect = 0.6 * insulin_dose
            natural_decay = (target_glucose - actual_glucose[i-1]) * 0.05
            actual_glucose[i] = actual_glucose[i-1] + meal_spike - insulin_effect + natural_decay
            prev_error = error

        # Perbarui Grafik
        self.ax1.clear()
        self.ax1.plot(time, actual_glucose, label='Actual Blood Glucose', color='#1f77b4', linewidth=2)
        self.ax1.axhline(target_glucose, color='#d62728', linestyle='--', label='Target (90 mg/dL)')
        self.ax1.set_title('Patient Blood Glucose Level', fontsize=12, fontweight='bold')
        self.ax1.set_ylabel('Glucose (mg/dL)')
        self.ax1.legend(loc='upper right')
        self.ax1.grid(True, linestyle=':', alpha=0.7)

        self.ax2.clear()
        self.ax2.plot(time, insulin_delivery, label='Insulin Pump Delivery', color='#9467bd', linewidth=2)
        self.ax2.set_title('Insulin Pump Action', fontsize=12, fontweight='bold')
        self.ax2.set_xlabel('Time (minutes)')
        self.ax2.set_ylabel('Dose (Units)')
        self.ax2.fill_between(time, insulin_delivery, alpha=0.2, color='#9467bd')
        self.ax2.legend(loc='upper right')
        self.ax2.grid(True, linestyle=':', alpha=0.7)

        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    root = tk.Tk()
    app = PancreasSimulatorApp(root)
    root.mainloop()
