D = 0.254;       %Diametro elica [m]
max_RPM = 8539;
n_max = max_RPM/60;

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

%% CALCOLO POTENZA PROPULSIVA EFFETTIVA IN FUNZIONE DELLA VELOCITA' INDISTURBATA
coeff_P_prop = coeff_eta_prop .* max_P_shaft
v = linspace(0, 29.5, 100);
plot(v, polyval(coeff_P_prop, v));

poly2sym(coeff_P_prop) % In output la funzione simbolica - attenzione al range di plot!

f = @(x) ((6914260054825037.*x.^15)/1267650600228229401496703205376 - (465975034830941.*x.^14)/309485009821345068724781056 + (438546751597867.*x.^13)/2417851639229258349412352 - (3848533357633813.*x.^12)/302231454903657293676544 + (2757069114498035.*x.^11)/4722366482869645213696 - (5459705683898567.*x.^10)/295147905179352825856 + (3845400541620467.*x.^9)/9223372036854775808 - (7799509199559873.*x.^8)/1152921504606846976 + (355565129980795.*x.^7)/4503599627370496 - (5890296412221353.*x.^6)/9007199254740992 + (4209679236237963.*x.^5)/1125899906842624 - (7914493034490199.*x.^4)/562949953421312 + (9006155510541971.*x.^3)/281474976710656 - (1337187439795785.*x.^2)/35184372088832 + (7678943032343733.*x)/281474976710656 + 5388791348096689/576460752303423488);
x = linspace(0, 29.4, 100);
plot(x, f(x));