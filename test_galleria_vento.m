% Dati ottenuti da test in galleria del vento in FULL THROTTLE. Diagrammi riportati nei
% documenti "Study of Electronic Speed Control Strategies for a Fixed
% Battery, Motor and Propeller Aircraft Propulsion Set - Viktor Zombori"
% (nel codice: _A); e nel report tecnico del Team 07 (nel codice: _B) -
% RIMOSSO: non è ben specificata la modalità di raccolta dei dati.
% I dati sono stati ri-ottenuti dal diagramma con PlotDigitizer.com

% T_apc = [13.01 12.46 11.92 11.37 10.75 9.979 8.992 7.882 7.726 5.702 4.769];
% v_apc = [5 7 9 11 13 15 17 19 21 23 25];

% DA QUI IN POI I DATI SONO RIFERITI ALL'ELICA AERONAUT 10x6

T_A = [0 13.63 13.12 12.46 11.84 11.08 10.20 9.358 8.517 7.567 6.689 5.775 4.789];
v_A = [0 5 7 9 11 13 15 17 19 21 23 25 27];

T_B = [14.22 13.91 13.54 13.15 12.80 12.43 12.10 11.72 11.31 10.79 10.13 9.223 8.025];
v_B = [0 2.047 4.134 6.220 8.307 10.39 12.48 14.53 16.65 18.70 20.79 22.91 24.96];

v = linspace(0, 27, 200);

figure;
hold on;
c_T_A = polyfit(v_A, T_A, 3);
c_T_B = polyfit(v_B, T_B, 3);
plot(v, polyval(c_T_A, v));
plot(v, polyval(c_T_B, v));
plot (v_A, T_A, '*');
plot (v_B, T_B, '*');
legend('Thrust (A)', 'Thrust (B)');
xlabel('Airspeed [m/s]');
ylabel('Thrust [N]');
title('Axi-2826/10 Gold line v2 + propeller');

v = linspace(0, 45, 200);

figure;
hold on;
yyaxis left;
P_A = T_A.*v_A;
% P_B = T_B.*v_B;
c_P_A = polyfit(v_A, P_A, 3);
% c_P_B = polyfit(v_B, P_B, 3);
plot(v, polyval(c_P_A, v));
% plot(v, polyval(c_P_B, v));
plot(v_A, P_A, '+');
% plot(v_B, P_B, '+');

axis([0 45 0 200]);
legend('Wind tunnel');
xlabel('Airspeed [m/s]');
ylabel('Power available [W]');
title('Axi-2826/10 Gold line v2 + Aeronaut 10x6 propeller');

poly2sym(c_T)