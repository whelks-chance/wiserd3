#!/bin/bash

tablenames=("x_sid_liw2007_lsoa_" "x_sid_liw2007_police_" "x_sid_liwhh2004_fire_" "x_sid_liw2007_pcode_" "x_wisid_ad_plasc_ethnic_2004_ua_" "x_sid_liwhh2004_aefa_" "x_sid_liwhh2004_lsoa_" "x_sid_liwhh2005_parl_" "x_sid_liwhh2005_lsoa_" "x_sid_liwhh2005_police_" "x_sid_liwhh2005_pcode_" "x_sid_liwhh2005_ua_" "x_sid_liwhh2006_aefa_" "x_sid_liwhh2006_pcode_" "x_sid_liwps2004_lsoa_" "x_sid_liwps2004_pcode_" "x_sid_liw2007_ua_" "x_sid_liw2007_parl_" "x_sid_liwhh2004_pcode_" "x_sid_liwhh2006_fire_" "x_sid_liwhh2006_lsoa_" "x_sid_liwps2004_parl_" "x_sid_liwps2004_police_" "x_sid_liw2007_aefa_" "x_sid_liwhh2004_parl_" "x_sid_liwhh2004_police_" "x_sid_liwhh2004_ua_" "x_sid_whs2007_03_ua_" "x_sid_liwhh2005_aefa_" "x_sid_whs0306aq1_ua_" "x_sid_liwhh2005_fire_" "x_sid_whs2009_03_ua_" "x_sid_liwhh2006_parl_" "x_sid_whs0306aq2_ua_" "x_sid_liwhh2006_police_" "x_sid_whs2008_1315_ua_" "x_sid_whs2007_1315_ua_" "x_sid_liwhh2006_ua_" "x_sid_whs0306aq3_ua_" "x_sid_liwps2004_aefa_" "x_sid_liwps2004_fire_" "x_sid_whs0306cq1_ua_" "x_sid_liwps2004_ua_" "x_sid_whs2007_412_ua_" "x_sid_wersmq2004_wales_" "x_sid_whs0306cq2_ua_" "x_sid_whshh03063_ua_" "x_sid_whs0306cq3_ua_" "x_sid_whs2008_412_ua_" "x_sid_whs2007aq_ua_" "x_sid_whs2009aq_ua_" "x_sid_whs2009_1315_ua_" "x_sid_whs2008_03_ua_" "x_sid_whs2008aq_ua_" "x_sid_whshh03062_ua_" "x_sid_whs2009_412_ua_" "x_sid_whshh03061_ua_" "x_sid_whshh2007_ua_" "x_sid_whshh2009_ua_" "x_wisid_ad_plasc_ss1115welsh_2004_ua_" "x_wisid_ad_plasc_ethnic_2003_ua_" "x_wisid_ad_plasc_identity_2005_ua_" "x_wisid_ad_plasc_ethnic_2005_ua_" "x_sid_liw2007_fire_" "x_wisid_ad_plasc_ethnic_2006_ua_" "x_wisid_ad_plasc_identity_2006_ua_" "x_wisid_ad_plasc_ethnic_2007_ua_" "x_wisid_ad_plasc_ss1115welsh_2009_ua_" "x_wisid_ad_plasc_ss1115welsh_2005_ua_" "x_wisid_ad_plasc_ethnic_2008_ua_" "x_wisid_ad_plasc_identity_2007_ua_" "x_wisid_ad_plasc_ethnic_2009_ua_" "x_wisid_ad_plasc_identity_2003_ua_" "x_wisid_ad_plasc_identity_2008_ua_" "x_wisid_ad_plasc_identity_2004_ua_" "x_wisid_ad_plasc_ss1115welsh_2006_ua_" "x_wisid_ad_plasc_identity_2009_ua_" "x_wisid_ad_plasc_ss1115welsh_2003_ua_" "x_wisid_ad_plasc_ss1115welsh_2007_ua_" "x_wisid_ad_plasc_ss1115welsh_2008_ua_" "x_sid_whshh2008_ua_")

for i in ${tablenames[@]}
do

#    echo "$i"
    mkdir -p '/tmp/shp/'"$i"
    chmod -R 777 '/tmp/shp/'"$i"
    cmd='pgsql2shp -f /tmp/shp/'"$i"'/'"$i"'.shp -h localhost -u dataportal -P d4t4p0rtalacce55 "Survey_Data" '"$i"
    echo $cmd
    sudo su postgres -c "$cmd"
done