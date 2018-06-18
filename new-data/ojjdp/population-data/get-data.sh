#!/bin/bash

BASE = 'https://www.ojjdp.gov/ojstatbb/ezapop/asp/profile_display.asp'

#wget -o '$BASE?selState=56&selCounty=1&selLowerYear=1&selUpperYear=1&selLowerAge=1&selUpperAge=1&row_var=v05&col_var=v03&display_type=counts&export_file=yes&printer_friendly=&v0127=v0127'

wget -O test1.csv "https://www.ojjdp.gov/ojstatbb/ezapop/asp/profile_display.asp?selState=56&selCounty=1&selLowerYear=1&selUpperYear=1&selLowerAge=1&selUpperAge=1&row_var=v05&col_var=v03&display_type=counts&export_file=yes&printer_friendly=&v0127=v0127"
