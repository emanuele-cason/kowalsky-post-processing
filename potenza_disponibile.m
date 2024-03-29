%% NOTAZIONE UTILIZZATA
% coeff_: coefficienti del polyfit
% _apc: dati riferiti all'elica APC
% T_: thrust
% P_: potenza disponibile
% _wt: dati riferiti ai dati del wind tunnel
% _est: valore stimato dal modello eCalc + datasheet

D = 0.254;       %Diametro elica [m]
max_RPM = 8539;
n_max = max_RPM/60;
v = linspace(0, 45, 200);

% Dati ottenuti da test in galleria del vento in FULL THROTTLE. Diagrammi riportati nei
% documenti "Study of Electronic Speed Control Strategies for a Fixed
% Battery, Motor and Propeller Aircraft Propulsion Set - Viktor Zombori" (nel codice: _wt); e nel report tecnico del Team 07 (nel codice: _wt7) -
% SET B RIMOSSO: non � ben specificata la modalit� di raccolta dei dati.
% I dati sono stati ri-ottenuti dal diagramma con PlotDigitizer.com

% T_apc = [13.01 12.46 11.92 11.37 10.75 9.979 8.992 7.882 7.726 5.702 4.769];
% v_apc = [5 7 9 11 13 15 17 19 21 23 25];

% DA QUI IN POI I DATI SONO RIFERITI ALL'ELICA AERONAUT 10x6

T_wt = [13.63 13.12 12.46 11.84 11.08 10.20 9.358 8.517 7.567 6.689 5.775 4.789];
v_wt = [5 7 9 11 13 15 17 19 21 23 25 27];

% T_wt7 = [14.22 13.91 13.54 13.15 12.80 12.43 12.10 11.72 11.31 10.79 10.13 9.223 8.025];
% v_wt7 = [0 2.047 4.134 6.220 8.307 10.39 12.48 14.53 16.65 18.70 20.79 22.91 24.96];

%% CALCOLO RENDIMENTO DELL'ELICA IN FUNZIONE DELLA VELOCITA' INDISTURBATA
%Dati reperibili al link: https://www.apcprop.com/files/PER3_10x6.dat
J_tab = [0.00 0.03 0.06 0.08 0.11 0.14 0.17 0.20 0.22 0.25 0.28 0.31 0.33 0.36 0.39 0.42 0.45 0.47 0.50 0.53 0.56 0.59 0.61 0.64 0.67 0.70 0.73 0.75 0.78 0.81];
eta_prop = [0.0000 0.0642 0.1257 0.1843 0.2420 0.2933 0.3435 0.3908 0.4352 0.4767 0.5154 0.5511 0.5837 0.6134 0.6402 0.6640 0.6894 0.7029 0.7182 0.7312 0.7419 0.7498 0.7549 0.7566 0.7537 0.7408 0.7111 0.6501 0.5049 0.0008];
%Interpolazione dati
V_tab = J_tab .* n_max .* D;
coeff_eta_prop = polyfit(V_tab, eta_prop, 15);

%% CALCOLO POTENZA MECCANICA EROGATA DAL MOTORE IN FUNZIONE DEL NUMERO DI GIRI MOTORE
%Dati ottenuti da eCalc dagli screen di data 18/03/2019
RPM = [1200 1800 2400 3000 3600 4200 4800 5400 6000 6600 7200 7800 8400 8539];
P_elec = [2.2 4.2 7.4 12.1 18.8 27.9 39.8 54.9 73.8 96.8 124.4 157.0 195.3 206.2];
eta_mot = [0.219 0.382 0.515 0.614 0.683 0.732 0.766 0.790 0.807 0.819 0.827 0.833 0.837 0.833];        %Rendimento meccanico
%Interpolazione dati
P_shaft = P_elec .* eta_mot;
coeff_P_shaft = polyfit(RPM, P_shaft, 3);
max_P_shaft = polyval(coeff_P_shaft, max_RPM);

%% CALCOLO POTENZA PROPULSIVA EFFETTIVA PREVISTA IN FUNZIONE DELLA VELOCITA' INDISTURBATA
coeff_P_est = coeff_eta_prop .* max_P_shaft;

%% INTERPOLAZIONE POLINOMIALE THRUST MISURATO E POTENZA IN GALLERIA DEL VENTO
coeff_T_wt = polyfit(v_wt, T_wt, 3);
P_wt = T_wt.*v_wt;
coeff_P_wt = polyfit(v_wt, P_wt, 3);

%% CALCOLO ERRORE POTENZA MISURATA - PREVISTA
err_rel = abs(P_wt - polyval(coeff_P_est, v_wt))./(P_wt);

%% PLOT THRUST
figure;
hold on;
axis([0 30 0 15]);
title('Axi-2826/10 Gold line v2 + Elica Aeronaut 10x6');
xlabel('Airspeed [m/s]');
ylabel('Thrust [N]');
plot(v, polyval(coeff_T_wt, v));
plot (v_wt, T_wt, '*');

%% PLOT POTENZA DISPONIBILE (MISURATA VS PREVISTA) ED ERRORE
figure;
hold on;
axis([0 30 0 200]);
title('Axi-2826/10 Gold line v2 + Elica Aeronaut 10x6');
yyaxis left;
xlabel('Airspeed [m/s]');
ylabel('Thrust [N]');
plot(v, polyval(coeff_P_wt, v));
plot(v_wt, P_wt, '+');
plot(v, polyval(coeff_P_est, v));
legend('Wind tunnel (fit)', 'Wind tunnel (dati)' ,'Previsione eCalc');

yyaxis right;
ylabel('Relative error');
plot(v_wt, err_rel);

poly2sym(coeff_P_est) % In output la funzione simbolica - attenzione al range di plot!