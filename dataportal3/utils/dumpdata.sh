#!/bin/sh

python manage.py dumpdata --database=new --exclude=dataportal3.Aberystwyth_Locality_Dissolved --exclude=dataportal3.Bangor_Locality_Dissolved --exclude=dataportal3.Heads_of_the_Valleys --output=new_db4.json