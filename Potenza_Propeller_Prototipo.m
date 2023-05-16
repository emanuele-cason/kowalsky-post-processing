clear all
close all
%% Dati di inupt
ro=1.225;
S=1;
Cd0=0.0206;
AR=11;
e=0.731;
W=6*9.81;
D=0.254;       %Diametro elica [m]

%% CALCOLO RENDIMENTO ELICA IN FUNZIONE DEL RAPPORTO DI AVANZAMENTO
%Dati reperibili al link: https://www.apcprop.com/files/PER3_10x6.dat
J=[0.00 0.03 0.06 0.08 0.11 0.14 0.17 0.20 0.22 0.25 0.28 0.31 0.33 0.36 0.39 0.42 0.45 0.47 0.50 0.53 0.56 0.59 0.61 0.64 0.67 0.70 0.73 0.75 0.78 0.81];
eta=[0.0000 0.0642 0.1257 0.1843 0.2420 0.2933 0.3435 0.3908 0.4352 0.4767 0.5154 0.5511 0.5837 0.6134 0.6402 0.6640 0.6894 0.7029 0.7182 0.7312 0.7419 0.7498 0.7549 0.7566 0.7537 0.7408 0.7111 0.6501 0.5049 0.0008];
%Interpolazione dati
coeff_eta=polyfit(J,eta,15);
x_J=linspace(0,J(end),100);
y_eta=polyval(coeff_eta,x_J);
figure(1)
plot(x_J,y_eta,'r-',J,eta,'bo',[0 J(end)],[0 0],'k-',[0 0],[0 1],'k-')
xlabel('J')
ylabel('\eta_p')
title('Rendimento elica APC 10x6 in funzione del rapporto di funzionamento')
axis([0 J(end) 0 1])
grid on
grid minor

%% CALCOLO POTENZA MECCANICA EROGATA DAL MOTORE IN FUNZIONE DEL NUMERO DI GIRI MOTORE
%Dati ottenuti da eCalc dagli screen di data 18/03/2019
RPM=[1200 1800 2400 3000 3600 4200 4800 5400 6000 6600 7200 7800 8400 8539];
P_E=[2.2 4.2 7.4 12.1 18.8 27.9 39.8 54.9 73.8 96.8 124.4 157.0 195.3 206.2];
n_m=[0.219 0.382 0.515 0.614 0.683 0.732 0.766 0.790 0.807 0.819 0.827 0.833 0.837 0.833];        %Rendimento meccanico
%Interpolazione dati
P_S=P_E.*n_m;
coeff_P_S=polyfit(RPM,P_S,3);
x_RPM=linspace(0,RPM(end),100);
y_P_S=polyval(coeff_P_S,x_RPM);
figure(2)
plot(x_RPM,y_P_S,'r-',RPM,P_S,'bo',[0 RPM(end)],[0 0],'k-',[0 0],[0 max(P_S)+0.1*max(P_S)],'k-')
xlabel('RPM [1/(60s)]')
ylabel('P_S [W]')
title('Potenza meccanica erogata dal motore in funzione del numero di giri motore')
axis([0 RPM(end) 0 max(P_S)+0.1*max(P_S)])
grid on
grid minor
hold off

%% POTENZA DISPONIBILE IN FUNZIONE DI V_INF PARAMETRIZZATA RISPETTO AD RPM
%Le variabili verranno rinominate con _param per distinguerle da quelle usate sopra
figure(3)
%RPM=5000
RPM_param=5000;
n=RPM_param/60;
P_S_param=polyval(coeff_P_S,RPM_param);
V_param=linspace(0,19,100);
J_param=V_param./(n*D);
eta_param=polyval(coeff_eta,J_param);
P_A_param=eta_param.*P_S_param;
plot(V_param,P_A_param,'b-');
%RPM=6500
RPM_param=6500;
n=RPM_param/60;
P_S_param=polyval(coeff_P_S,RPM_param);
V_param=linspace(0,23.5,100);
J_param=V_param./(n*D);
eta_param=polyval(coeff_eta,J_param);
P_A_param=eta_param.*P_S_param;
hold on
plot(V_param,P_A_param,'r-');
%RPM=7500
RPM_param=7500;
n=RPM_param/60;
P_S_param=polyval(coeff_P_S,RPM_param);
V_param=linspace(0,27.5,100);
J_param=V_param./(n*D);
eta_param=polyval(coeff_eta,J_param);
P_A_param=eta_param.*P_S_param;
plot(V_param,P_A_param,'m-');
%RPM=8000
RPM_param=8000;
n=RPM_param/60;
P_S_param=polyval(coeff_P_S,RPM_param);
V_param=linspace(0,30.5,100);
J_param=V_param./(n*D);
eta_param=polyval(coeff_eta,J_param);
P_A_param=eta_param.*P_S_param;
plot(V_param,P_A_param,'c-');
%RPM=8539
RPM_param=8539;
n=RPM_param/60;
P_S_param=polyval(coeff_P_S,RPM_param); %Potenza meccanica a numero di giri dato
V_param=linspace(0,31.0,100);
J_param=V_param./(n*D);
eta_param=polyval(coeff_eta,J_param); 
P_A_param=eta_param.*P_S_param;



plot(V_param,P_A_param,'g-');
title('Power available and Power required')
xlabel('V_\infty [m/s]')
ylabel('P_A [W]')
axis([0 35 0 300])

%% Potenza richiesta
k=1/(pi*AR*e);
A=0.5*ro*S*Cd0;
B=2*k*(W^2)/(ro*S);
f=@(V) A*(V.^3)+B*(V.^-1);
x_Pn=linspace(0,32,100);
y_Pn=feval(f,x_Pn);
plot(x_Pn,y_Pn,'k-')
legend('RPM=5000','RPM=6500','RPM=7500','RPM=8000','RPM=8539','P_R')
grid on
grid minor
hold off
V_7223=V_param;
P_A_7223=P_A_param;

%% PRESTAZIONI DI DECOLLO A RPM=7223
coeff_P_A=polyfit(V_7223,P_A_7223,15);
%y=polyval(coeff_P_A,V_param);
%hold on
%plot(V_param,y,'k-')
%hold off
a_0=coeff_P_A(1,1);
a_1=coeff_P_A(1,2);
a_2=coeff_P_A(1,3);
a_3=coeff_P_A(1,4);
a_4=coeff_P_A(1,5);
a_5=coeff_P_A(1,6);
a_6=coeff_P_A(1,7);
a_7=coeff_P_A(1,8);
a_8=coeff_P_A(1,9);
a_9=coeff_P_A(1,10);
a_10=coeff_P_A(1,11);
a_11=coeff_P_A(1,12);
a_12=coeff_P_A(1,13);
a_13=coeff_P_A(1,14);
a_14=coeff_P_A(1,15);
a_15=coeff_P_A(1,16);
fun=@(v) v.^2./(a_0*v.^15+a_1*v.^14+a_2*v.^13+a_3*v.^12+a_4*v.^11+a_5*v.^10+a_6*v.^9+a_7*v.^8+a_8*v.^7+a_9*v.^6+a_10*v.^5+a_11*v.^4+a_12*v.^3+a_13*v.^2+a_14*v+a_15);
M=6;
V_LOF_Array=[];
x_R_Array=[];
for V_LOF=1:0.5:14
sol=integral(fun,1,V_LOF);
x_R=M*sol;
V_LOF_Array=[V_LOF_Array V_LOF];
x_R_Array=[x_R_Array x_R];
end
coeff_x_R=spline(V_LOF_Array,x_R_Array);
V_LOF_spline=linspace(1,14,100);
x_R_spline=ppval(coeff_x_R,V_LOF_spline);
figure(4)
plot(11.9535,60,'b*',V_LOF_spline,x_R_spline,'r-')
title('Distanza di decollo in funzione della velocità di decollo')
xlabel('V_L_O_F [m/s]')
ylabel('x_R [m]')
axis([0 15 0 80])
legend('Target di progetto')
grid on
grid minor
%End script
save coeff.mat a_0 a_1 a_2 a_3 a_4 a_5 a_6 a_7 a_8 a_9 a_10 a_11 a_12 a_13 a_14 a_15

