
proc format;
value $age4x
Left-censored ="Left Censored"
0 ="0"
1 ="1"
2 ="2"
3 ="3"
4 ="4"
5 ="5"
6-10 ="6-10"
11-15 ="11-15"
16-20 ="16-20"
21-25 ="21-25"
26+ ="26+"
;
run;


proc format;
value d_flag
0 ="Not suppressed"
1 ="Values have been suppressed to prevent disclosure of sensitive data."
;
run;


/* data bds_e_ageisz_release;
label age4 = "Employment based measure of establishment age";
label estabs = "Number of establishments";
label emp = "Employment";
label denom = "Davis-Haltiwanger-Schuh (DHS) denominator";
label estabs_entry = "Establishment births";
label estabs_entry_rate = "Establishment birth rate";
label estabs_exit = "Establishment deaths";
label estabs_exit_rate = "Establishment death rate";
label d_flag = "Disclosure flag";
label firmdeath_emp = "Employment in firm deaths";
label msa = "Metropolitan Statistical Areas";
format
year2 year2x.
isize isize.
age4 age4x.
firms firms.
estabs estabs.
emp emp.
denom denom.
estabs_entry est0ntr.
estabs_entry_rate est0rat.
estabs_exit est0exi.
estabs_exit_rate est0rat.
job_creation job0tio.
job_creation_births job0rth.
job_creation_continuers job0uer.
job_creation_rate_births job0rth.
job_creation_rate job0rat.
job_destruction job0tio.
job_destruction_deaths job0ath.
job_destruction_continuers job0uer.
job_destruction_rate_deaths job0ath.
job_destruction_rate job0rat.
net_job_creation net0tio.
net_job_creation_rate net0rat.
reallocation_rate rea0rat.
d_flag d_flag.
firmdeath_firms fir0irm.
firmdeath_estabs fir0tab.
firmdeath_emp fir0_em.
size size.
msa msa.
state state.
sic1 sic1x.
;
run;
*/