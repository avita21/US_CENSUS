% Avita Sharma 5/1/2017
% Regression on Data from the US Census

% First run build_data.py

%% Load and Preprocess Data
clear, clc, close all

% load Panel Data
Panel = readtable('dataset.csv');
Panel.GDP = log(Panel.GDP);
Panel.uni = log(Panel.uni);
Panel.minw = log(Panel.minw);
Panel.eind = log(Panel.eind);
Panel.ecom = log(Panel.ecom);
% perform a Multilevel Mixed-Effects Modeling usin
% Ordinary Least Squares
lm_ols = fitlm(Panel, ['job ~ time + state +(time:state) + unemp + edu'...
                        '+ uni + minw + GDP + eind + ecom'])
lme_ols = fitlme(Panel, ['job ~ time + state +(time:state) + unemp + edu'...
                        '+ uni + minw + GDP + eind + ecom'])
figure();
plotResiduals(lm_ols,'fitted')
figure();
plotResiduals(lme_ols,'fitted')

  