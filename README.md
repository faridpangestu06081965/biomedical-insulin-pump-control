# Artificial Pancreas: Closed-Loop Blood Glucose PID Controller

![MATLAB](https://img.shields.io/badge/MATLAB-R2017a-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Simulink](https://img.shields.io/badge/Simulink-Automated-orange.svg)
![Domain](https://img.shields.io/badge/Domain-Biomedical%20%26%20Control-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A dual-stack biomedical control system modeling an automated artificial pancreas using MATLAB/Simulink programmatic API and an interactive Python Tkinter GUI. The system regulates blood glucose levels via closed-loop PID insulin infusion in response to postprandial meal disturbances.

---

## 📌 Project Overview & Engineering Highlights

This project models an automated insulin pump regulating blood glucose around a target setpoint of 90 mg/dL, managing safety-critical physiological constraints to prevent fatal hypoglycemia.

- 🩸 **Patient Metabolic Dynamics**: Modeled using a first-order lag transfer function $G(s) = \frac{1}{30s + 1}$, representing the physiological delay of insulin absorption in human tissue.
- 🎛️ **Safety-Critical PID Control**: Tuned conservatively ($P=1.5, I=0.05, D=2.0$) to guarantee an overdamped system response, prioritizing patient safety over rapid settling to avoid dangerous hypoglycemic dips.
- 🍲 **Postprandial Meal Disturbance**: Injects a sudden glucose spike at $t = 60\text{ min}$ to simulate carbohydrate intake and test closed-loop disturbance rejection.
- 🖥️ **Interactive Python GUI & Physical Saturation**: Features a custom Tkinter/Matplotlib application with real-time PID slider tuning and discrete physical constraints ($\text{insulin dose} \ge 0$).

---

## 📈 System Response Analysis

Based on the 200-minute simulation profile:
1. **Basal Phase (0 - 60 min)**: System steadily tracks and locks onto the baseline target setpoint of 90 mg/dL.
2. **Postprandial Recovery Phase (60 - 200 min)**: Upon meal ingestion at $t = 60\text{ min}$, glucose peaks at $\approx 115\text{ mg/dL}$. The PID controller infuses insulin to drive levels back to 90 mg/dL smoothly without severe undershoot.

---

## 🛠️ Tech Stack & Requirements

- **MATLAB/Simulink**: R2017a or newer (programmatic model build)
- **Python**: 3.x (`numpy`, `matplotlib`, `tkinter`)

---

## 🚀 Quick Start

### 1. Running MATLAB Programmatic Simulink Model
Open MATLAB, navigate to the folder, and run:
```matlab
artificial_pancreas
