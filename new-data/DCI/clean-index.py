import csv,copy

fileDir = 'all-combined/index-offenses/'
year = '2016'
filename = fileDir+year+'-index-cp-b4.csv'

file = open(filename,'r')

county_obj = {'name':'','murder':{'total':0,'adult_male':0,'adult_female':0,'juvenile_male':0,'juvenile_female':0},
                        'forcible_rape':{'total':0,'adult_male':0,'adult_female':0,'juvenile_male':0,'juvenile_female':0},
                        'robbery':{'total':0,'adult_male':0,'adult_female':0,'juvenile_male':0,'juvenile_female':0},
                        'aggravated_assault':{'total':0,'adult_male':0,'adult_female':0,'juvenile_male':0,'juvenile_female':0},
                        'burglary':{'total':0,'adult_male':0,'adult_female':0,'juvenile_male':0,'juvenile_female':0},
                        'larceny_theft':{'total':0,'adult_male':0,'adult_female':0,'juvenile_male':0,'juvenile_female':0},
                        'mvt':{'total':0,'adult_male':0,'adult_female':0,'juvenile_male':0,'juvenile_female':0},
                        'total':{'total':0,'adult_male':0,'adult_female':0,'juvenile_male':0,'juvenile_female':0}
            }
tmp = copy.deepcopy(county_obj)
index = ''
all_counties = []
for line in file:
    if line != '':
        if line.startswith('##') and '(DOES NOT REPORT)' not in line:
            print('finished obj='+str(tmp))
            tmp2=tmp
            all_counties.append(copy.deepcopy(tmp))
            tmp = copy.deepcopy(county_obj)
            county = ' '.join(line.split(' ')[1:]).strip('\n')
            tmp['name']=county.upper()
            print('new county='+county)
        elif line.startswith('Murder'):
            index = 'murder'
            tmp[index]['total']=line.split(' ')[-1].strip('\n')
        elif line.startswith('Forcible'):
            index = 'forcible_rape'
            tmp[index]['total']=line.split(' ')[-1].strip('\n')
        elif line.startswith('Robbery'):
            index = 'robbery'
            tmp[index]['total']=line.split(' ')[-1].strip('\n')
        elif line.startswith('Aggravated'):
            index = 'aggravated_assault'
            tmp[index]['total']=line.split(' ')[-1].strip('\n')
        elif line.startswith('Burglary'):
            index = 'burglary'
            tmp[index]['total']=line.split(' ')[-1].strip('\n')
        elif line.startswith('Larceny'):
            index = 'larceny_theft'
            tmp[index]['total']=line.split(' ')[-1].strip('\n')
        elif line.startswith('Motor'):
            index = 'mvt'
            tmp[index]['total']=line.split(' ')[-1].strip('\n')
        elif line.startswith('Offense'):
            index = 'total'
            tmp[index]['total']=line.split(' ')[-1].strip('\n')
        elif line.startswith('M '):
            if len(line.split(' '))>1:
                #print(line+'--want='+str(line.split(' ')[1].strip('\n'))+'--size='+str(len(line.split(' '))))
                tmp[index]['adult_male']=line.split(' ')[1].strip('\n')
            if len(line.split(' '))>2:
                #print(line+'--want='+str(line.split(' ')[2].strip('\n'))+'--size='+str(len(line.split(' '))))
                tmp[index]['juvenile_male']=line.split(' ')[2].strip('\n')
        elif line.startswith('F '):
            if len(line.split(' '))>1:
                #print(line+'--want='+str(line.split(' ')[1].strip('\n'))+'--size='+str(len(line.split(' '))))
                tmp[index]['adult_female']=line.split(' ')[1].strip('\n')
            if len(line.split(' '))>2:
                #print(line+'--want='+str(line.split(' ')[2].strip('\n'))+'--size='+str(len(line.split(' '))))
                tmp[index]['juvenile_female']=line.split(' ')[2].strip('\n')
        #now parse numbers
        # tmp[index]['total'] = line.split(' ')[-1]
        # nx = file.readline()
        # if len(nx.split(' '))>0:
        #     tmp[index]['adult_male']=nx.split(' ')[1]
        # if len(nx.split(' '))>1:
        #     tmp[index]['adult_male']=nx.split(' ')[1]
file.close()
all_counties = all_counties[1:]
writefile = fileDir+year+'-index-cp-after.csv'
file = open(writefile,'w+')
file.write('county,'+'murder_total,murder_adult_male,murder_adult_female,murder_juvenile_male,murder_juvenile_female,'+
                    'forcible_rape_total,forcible_rape_adult_male,forcible_rape_adult_female,forcible_rape_juvenile_male,forcible_rape_juvenile_female,'+
                    'robbery_total,robbery_adult_male,robbery_adult_female,robbery_juvenile_male,robbery_juvenile_female,'+
                    'aggravated_assault_total,aggravated_assault_adult_male,aggravated_assault_adult_female,aggravated_assault_juvenile_male,aggravated_assault_juvenile_female,'+
                    'burglary_total,burglary_adult_male,burglary_adult_female,burglary_juvenile_male,burglary_juvenile_female,'+
                    'larceny_theft_total,larceny_theft_adult_male,larceny_theft_adult_female,larceny_theft_juvenile_male,larceny_theft_juvenile_female,'+
                    'mvt_total,mvt_adult_male,mvt_adult_female,mvt_juvenile_male,mvt_juvenile_female,'+
                    'total_total,total_adult_male,total_adult_female,total_juvenile_male,total_juvenile_female\n')
for county in all_counties:
    print('writing '+str(county))
    strg = f"{county['name']},{county['murder']['total']},{county['murder']['adult_male']},{county['murder']['adult_female']},{county['murder']['juvenile_male']},{county['murder']['juvenile_female']},"
    strg = strg+f"{county['forcible_rape']['total']},{county['forcible_rape']['adult_male']},{county['forcible_rape']['adult_female']},{county['forcible_rape']['juvenile_male']},{county['forcible_rape']['juvenile_female']},{county['robbery']['total']},{county['robbery']['adult_male']},{county['robbery']['adult_female']},{county['robbery']['juvenile_male']},{county['robbery']['juvenile_female']},{county['aggravated_assault']['total']},{county['aggravated_assault']['adult_male']},{county['aggravated_assault']['adult_female']},{county['aggravated_assault']['juvenile_male']},{county['aggravated_assault']['juvenile_female']},{county['burglary']['total']},{county['burglary']['adult_male']},{county['burglary']['adult_female']},{county['burglary']['juvenile_male']},{county['burglary']['juvenile_female']},{county['larceny_theft']['total']},{county['larceny_theft']['adult_male']},{county['larceny_theft']['adult_female']},{county['larceny_theft']['juvenile_male']},{county['larceny_theft']['juvenile_female']},{county['mvt']['total']},{county['mvt']['adult_male']},{county['mvt']['adult_female']},{county['mvt']['juvenile_male']},{county['mvt']['juvenile_female']},{county['total']['total']},{county['total']['adult_male']},{county['total']['adult_female']},{county['total']['juvenile_male']},{county['total']['juvenile_female']}"
    file.write(strg+'\n')

file.close()
