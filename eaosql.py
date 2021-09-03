'''
This program can only be used at EAO/JCMT:

usage: eaosql.py [instrument] [-p project-ID] [-d utdate] [-n obsnum] [-o object] [-m molecule]
positional arguments:
  {uu,aweoweo,harp,scuba2}      enter Uu, Aweoweo, HARP or SCUBA2

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        project code
  -d UTDATE, --utdate UTDATE
                        UT date in format of YYYYMMDD
  -n OBSNUM, --obsnum OBSNUM
                        observation number
  -o OBJECT, --object, OBJECT
			observing target
  -m MOLECULE, --molecule MOLECULE

Generate a SQL file to search the JCMT database;
if neither project ID nor UTdate is provided, return all entries of today,
if available.
Then generate a txt file which lists all data file paths.

For complex and advance query, please use SQL directly,
or use the generated *.sql file as a starting point.

To-do: add the following keyword in SQL filter:
obs_sb, subbands (e.g., 250MHz), etc.

2021-03-24 Xue-Jian Jiang
2021-07-13 returned table is ordered by utdate obsnum
'''



import keyring, subprocess, os
from os import path
import pandas as pd
from datetime import datetime
import argparse
parser = argparse.ArgumentParser(usage='%(prog)s  eaosql.py [instrument] [-p project-ID] [-d utdate] [-n obsnum] [-o object] [-m molecule]',
                                 description='\
                                 This script generate a simple SQL file and search the JCMT database;\
                                 if neither project ID nor UTdate is provided, return all entries of today\
                                 if available.\
                                 It also generate a txt file which lists all data file paths.\
                                 For complex and advance query, please use SQL directly,\
                                 or use the generated *.sql file as a starting point.\
                                             ')
parser.add_argument("instrument", help="enter Uu, Aweoweo, HARP or SCUBA2", type = str.upper,
                    choices=['UU', 'HARP', 'SCUBA2','AWEOWEO'])
parser.add_argument("-p", "--project",  help="project code", type = str.upper)
parser.add_argument("-n", "--obsnum", help="observation number", type=int)
parser.add_argument("-o", "--object", help="observing target", type=str.upper)
parser.add_argument("-m", "--molecule", help="observing line", type=str.upper)
parser.add_argument("-d", "--utdate", help="UT date in format of YYYYMMDD",
                    )
args = parser.parse_args()
print('You entered: {}'.format(vars(args)))

instr = args.instrument # 'uu'
utdate = args.utdate
obsnum = args.obsnum
project = args.project
object = args.object
molecule = args.molecule

if 'project' == None:
        utdate = datetime.today().strftime('%Y%m%d')


def main():
        if 'instr' in globals():
                if instr == 'SCUBA2':
                        instrum = 'SCUBA2'
                        omp_scuba2(instrum)
                if instr == 'UU':
                        instrum = 'Uu'
                        omp_acsis(instrum)
                if instr == 'HARP':
                        instrum = 'HARP'
                        omp_acsis(instrum)
                if instr == 'AWEOWEO':
                        instrum = 'Aweoweo'
                        omp_acsis(instrum)

def omp_scuba2(instrum):
        ompcmd_base = '''\
mysql -h omp1 -u staff -b -p -e "select project, utdate, obsnum, object,
file_id, msbtitle, tau225st
from jcmt.COMMON
join jcmt.SCUBA2 on jcmt.COMMON.obsid=jcmt.SCUBA2.obsid
join jcmt.FILES on jcmt.SCUBA2.obsid_subsysnr=jcmt.FILES.obsid_subsysnr
where   jcmt.SCUBA2.filter=850
'''
        ompcmd = sql_filter(ompcmd_base)
        run_sql_file(ompcmd, instrum)

def omp_acsis(instrum):
        ompcmd_base = '''\
mysql -h omp1 -u staff -b -p -e "select project, utdate, obsnum, object,
file_id, msbtitle, obs_sb, jcmt.ACSIS.subsysnr, subbands, jcmt.ACSIS.restfreq,
molecule, transiti, tau225st
from jcmt.ACSIS
join jcmt.COMMON on jcmt.ACSIS.obsid=jcmt.COMMON.obsid
join jcmt.FILES on jcmt.ACSIS.obsid_subsysnr=jcmt.FILES.obsid_subsysnr
where jcmt.COMMON.telescop='JCMT'
''' \
        + "and instrume = '{}' ".format(instrum)
        ompcmd = sql_filter(ompcmd_base)
        run_sql_file(ompcmd, instrum)

def sql_filter(sql_text1):
        if project != None:
                sql_text1 += " and project='{}'".format(project)
        if utdate != None:
                sql_text1 += " and utdate='{}'".format(utdate)
        if obsnum != None:
                sql_text1 += " and obsnum={}".format(obsnum)
        if object != None:
                sql_text1 += " and object='{}'".format(object)
        if molecule != None:
                sql_text1 += " and molecule like '{}'".format(molecule)
        sql_text1 += ' order by utdate, obsnum, object;" > sql.tsv'
        return sql_text1

def run_sql_file(sql_text, instrum):
        sql_file = './'+instrum.lower()+'_sql.sql'
        print(sql_text, file = open(sql_file, 'w'))
        print('SQL script generated.')
        # omppwd = keyring.get_password('ompsql', username )
        print("Now you need to enter our internal staff password for the query:")
        subprocess.call(['. '+ sql_file], shell=True)

if __name__ == "__main__":
    main()

# -------------------------------------------------------------------------------------------
# run SQL to get the metadata, then run this script to generate a file list for later reduction.
# v0.2 20200904 use dataframe instead of np.array

sql_result = 'sql.tsv'
if os.path.isfile(sql_result) and os.path.getsize(sql_result) == 0:
        parser.error('!!! SQL return no result !!!')

f1=pd.read_csv(sql_result, sep='\t')
df = pd.DataFrame(columns=['path'])
j=-1
for i in range(0,len(f1)):
        date= str(f1['utdate'][i])
        num = format(f1['obsnum'][i], '05d')
        filter = f1['file_id'][i][:3]
        filename = f1['file_id'][i]
        if instr.lower() == 'scuba2':
                datapath=os.path.join('/jcmtdata/raw/scuba2/',filter,date,num,filename)
        if instr.lower() in ['uu', 'harp', 'aweoweo']:
                if f1['subsysnr'][i] == 1:    # only keep subsysnr=1 data
                        datapath = os.path.join('/jcmtdata/raw/acsis/spectra/', date, num, filename)
        if path.isfile(datapath):
                j=j+1
                df.loc[j] = datapath
files = pd.DataFrame(pd.unique(df.path))
files.to_csv('filelist.lis', index=False, header=False)
print('filelist.lis generated.')
