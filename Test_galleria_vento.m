% Dati ottenuti da test in galleria del vento in FULL THROTTLE. Diagramma riportato nel
% documento "Study of Electronic Speed Control Strategies for a Fixed
% Battery, Motor and Propeller Aircraft Propulsion Set - Viktor Zombori".
% I dati sono stati ri-ottenuti dal diagramma con PlotDigitizer.com

T_apc = [13.01 12.46 11.92 11.37 10.75 9.979 8.992 7.882 7.726 5.702 4.769];
v_apc = [5 7 9 11 13 15 17 19 21 23 25];
T_aeronaut = [13.63 13.12 12.46 11.84 11.08 10.20 9.358 8.517 7.567 6.689 5.775 4.789];
v_aeronaut = [5 7 9 11 13 15 17 19 21 23 25 27];

% plot(v_apc, T_apc, '.');
% hold on;
plot (v_aeronaut, T_aeronaut, '*');
hold on;
P_aeronaut = T_aeronaut.*v_aeronaut;
plot(v_aeronaut, P_aeronaut, '+');

c_T = polyfit(v_aeronaut, T_aeronaut, 3);
c_P = polyfit(v_aeronaut, P_aeronaut, 3);

v = linspace(0, 45, 200);
plot(v, polyval(c_P, v));

axis([0 45 0 200]);
legend('Aeronaut 10x6: Thrust', 'Aeronaut: P_A', 'Aeronaut polyfit: P_A');
xlabel('Airspeed [m/s]');
ylabel('Thrust [N] - Power available [W]');
title('Axi-2826/10 Gold line v2 + propeller');

poly2sym(c_T)