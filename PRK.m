clear all;

%get netReactivity from metal ULOF case
h = openfig('/global/home/users/ckeckler/docs/mini/ARC-mini/metal/ULOF/thermallyStratified/globalFigs/rhoPlotLong.fig','invisible');
dataObjs = get(get(h,'Children'),'Children'); %get line data for net reactivity line
time = get(dataObjs{2}(9),'XData');
netReactivity = get(dataObjs{2}(9),'YData');

%group decay constants, 1/s
lambda = [1.3377E-2 3.1026E-2 1.1763E-1 3.0917E-1 8.8605E-1 2.9416E+0];

%group yields
beta = [8.1001E-5 5.8791E-4 5.0738E-4 1.2053E-3 7.1130E-4 2.6155E-4];

%PRK data
betaEff = sum(beta);
l = 3.65E-7; %s
Lambda = l; %s

%time step
dt = 1E-6;
t = 10:dt:300;

%initialize power and precursor concentrations
phi = zeros(1,length(t));
C = {zeros(1,length(t)) zeros(1,length(t)) zeros(1,length(t)) zeros(1,length(t)) zeros(1,length(t)) zeros(1,length(t))};

%initial conditions
phi(1) = 1.0;
i = 1;
while i < length(lambda) + 1
    C{i}(1) = beta(i)/lambda(i)/Lambda;
    i = i + 1;
end

%solve for transient behavior
i = 1; %time step
while i < length(phi) - 1
    rho = interp1(time,netReactivity,t(i)); %get reactivity at specified time
    
    delayedNeutronTerm = 0;
    j = 1; %group
    while j < length(lambda) + 1 %sum reactivity from delayed neutrons
        delayedNeutronTerm = delayedNeutronTerm + lambda(j)*C{j}(i);
        j = j + 1;
    end
    
    phi(i+1) = dt*(phi(i)*(rho-betaEff)/Lambda + delayedNeutronTerm) + phi(i);
    
    j = 1; %group
    while j < length(lambda) + 1
        C{j}(i+1) = dt*(beta(j)*phi(i)/Lambda - lambda(j)*C{j}(i)) + C{j}(i);
        j = j + 1;
    end
    
    display(i)
    i = i + 1;
end

figure;
semilogy(t,phi);
savefig('PRKpower')
