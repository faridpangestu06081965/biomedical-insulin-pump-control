% =========================================================================
% Programmatic Simulink: Artificial Pancreas (Insulin Pump Control)
% Kompatibel dengan MATLAB R2017a
% =========================================================================
clear; clc;

modelName = 'Artificial_Pancreas_Control';

if bdIsLoaded(modelName)
    close_system(modelName, 0);
end

new_system(modelName);
open_system(modelName);

% 1. Spawn Blok Simulink
add_block('simulink/Sources/Constant', [modelName, '/Target_Glucose']);
add_block('simulink/Sources/Step', [modelName, '/Meal_Disturbance']);
add_block('simulink/Math Operations/Sum', [modelName, '/Error_Calc']);
add_block('simulink/Math Operations/Sum', [modelName, '/Force_Sum']);
add_block('simulink/Continuous/PID Controller', [modelName, '/Insulin_Pump_PID']);
add_block('simulink/Continuous/Transfer Fcn', [modelName, '/Patient_Metabolism']);
add_block('simulink/Signal Routing/Mux', [modelName, '/Mux']);
add_block('simulink/Sinks/Scope', [modelName, '/Glucose_Monitor']);

% 2. Atur Posisi Blok
set_param([modelName, '/Target_Glucose'], 'Position', [40, 100, 70, 130]);
set_param([modelName, '/Error_Calc'], 'Position', [130, 105, 150, 125], 'Inputs', '-|+'); % Aktual - Target
set_param([modelName, '/Insulin_Pump_PID'], 'Position', [200, 97, 240, 133]);
set_param([modelName, '/Meal_Disturbance'], 'Position', [240, 180, 270, 210]);
set_param([modelName, '/Force_Sum'], 'Position', [300, 105, 320, 125], 'Inputs', '-|+'); % Makan - Insulin
set_param([modelName, '/Patient_Metabolism'], 'Position', [370, 97, 460, 133]);
set_param([modelName, '/Mux'], 'Position', [520, 96, 525, 134], 'Inputs', '2');
set_param([modelName, '/Glucose_Monitor'], 'Position', [570, 100, 600, 130]);

% 3. Konfigurasi Parameter Fisiologis
% Target kadar gula darah: 90 mg/dL
set_param([modelName, '/Target_Glucose'], 'Value', '90'); 

% Pasien makan pada menit ke-60, menyebabkan lonjakan glukosa 50 mg/dL
set_param([modelName, '/Meal_Disturbance'], 'Time', '60', 'Before', '90', 'After', '140'); 

% Dinamika metabolisme: Keterlambatan respons tubuh terhadap insulin (1 / (30s + 1))
set_param([modelName, '/Patient_Metabolism'], 'Numerator', '[1]', 'Denominator', '[30 1]');

% Tuning PID untuk pompa (Fokus pada respons lambat/overdamped untuk mencegah hipoglikemia)
set_param([modelName, '/Insulin_Pump_PID'], 'P', '1.5', 'I', '0.05', 'D', '2.0');

% 4. Wiring
add_line(modelName, 'Target_Glucose/1', 'Error_Calc/1', 'autorouting', 'on');
add_line(modelName, 'Patient_Metabolism/1', 'Error_Calc/2', 'autorouting', 'on'); % Feedback Aktual

add_line(modelName, 'Error_Calc/1', 'Insulin_Pump_PID/1', 'autorouting', 'on');
add_line(modelName, 'Insulin_Pump_PID/1', 'Force_Sum/1', 'autorouting', 'on');
add_line(modelName, 'Meal_Disturbance/1', 'Force_Sum/2', 'autorouting', 'on');
add_line(modelName, 'Force_Sum/1', 'Patient_Metabolism/1', 'autorouting', 'on');

add_line(modelName, 'Target_Glucose/1', 'Mux/1', 'autorouting', 'on');
add_line(modelName, 'Patient_Metabolism/1', 'Mux/2', 'autorouting', 'on');
add_line(modelName, 'Mux/1', 'Glucose_Monitor/1', 'autorouting', 'on');

% 5. Eksekusi (Simulasi 200 menit)
set_param(modelName, 'StopTime', '200'); 
sim(modelName);
open_system([modelName, '/Glucose_Monitor']);
