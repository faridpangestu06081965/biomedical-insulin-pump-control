# Artificial Pancreas: Closed-Loop Blood Glucose Control & Simulation

![MATLAB](https://img.shields.io/badge/MATLAB-R2017a-blue.svg)
![Simulink](https://img.shields.io/badge/Simulink-Programmatic-orange.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![GUI](https://img.shields.io/badge/Tkinter-Interactive%20GUI-green.svg)
![Domain](https://img.shields.io/badge/Domain-Biomedical%20%26%20Control-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A dual-stack biomedical control system modeling an automated artificial pancreas (insulin pump control system). This repository features both a programmatic **MATLAB/Simulink** API simulation and an interactive **Python Tkinter GUI** application to model closed-loop blood glucose regulation and postprandial meal disturbance rejection.

---

## 📌 System Overview & Engineering Highlights

The artificial pancreas regulates blood glucose levels around a target baseline setpoint of **90 mg/dL**, managing safety-critical physiological constraints to prevent fatal hypoglycemia.

- 🩸 **Physiological Metabolism Model**: Modeled using a first-order lag transfer function $G(s) = \frac{1}{30s + 1}$, representing the time delay of subcutaneous insulin absorption into human tissue.
- 🎛️ **Safety-Critical PID Control**: Tuned conservatively ($P=1.5, I=0.05, D=2.0$) to guarantee an *overdamped* system response, prioritizing patient safety over aggressive settling times to avoid dangerous glucose undershoot.
- 🍲 **Postprandial Disturbance Rejection**: Simulates carbohydrate intake by injecting a sudden glucose surge of $+40\text{ mg/dL}$ at $t = 60\text{ minutes}$.
- 🖥️ **Interactive Python Tkinter GUI**: A standalone desktop simulator with real-time PID parameter sliders ($K_p, K_i, K_d$), embedded Matplotlib plots, and discrete controller physical constraints ($\text{insulin dose} \ge 0$).

---

## 🛠️ Dual-Stack Architecture

### 1. MATLAB / Simulink (`artificial_pancreas.m`)
- Programmatically constructs the full Simulink block diagram using the MATLAB R2017a API (`add_block`, `add_line`).
- Configures continuous-time transfer functions, step disturbance inputs, feedback error calculation, and dual-signal Scope monitoring (`Glucose_Monitor`).

### 2. Python Interactive GUI (`pancreas_gui.py`)
- Built with **Object-Oriented Programming (OOP)** using `tkinter` and `matplotlib.backends.backend_tkagg`.
- Implements a discrete-time PID control algorithm with physical saturation constraints (the insulin pump can inject insulin, but cannot remove it from the bloodstream).
- Features real-time parameter adjustment via interactive sliders to observe system stability and response curves dynamically.

---

## 📈 System Response & Simulation Analysis

| Phase | Time Window | System Behavior |
|---|---|---|
| **Basal Baseline** | $0 - 60\text{ min}$ | Glucose steadily tracks and locks onto the target setpoint ($90\text{ mg/dL}$). |
| **Meal Intake** | $t = 60\text{ min}$ | Glucose spikes to $\approx 115\text{ mg/dL}$ due to carbohydrate ingestion. |
| **Closed-Loop Recovery** | $60 - 200\text{ min}$ | PID controller infuses insulin, smoothly restoring glucose to $90\text{ mg/dL}$ without undershoot. |

---

## 📂 Repository Structure

```text
.
├── artificial_pancreas.m   # Programmatic Simulink model generation script
├── pancreas_gui.py         # Standalone Python Tkinter interactive GUI application
└── README.md               # Project documentation
