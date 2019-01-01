#Gaussian input file generator class
import re
from subprocess import call
class Gauss_Input():
    def __init__(self,filename,parameters):
        if filename != None:
            parameters = self.get_parameters(filename)
        for k, v in parameters.items():
            setattr(self,k,v)
    def get_parameters(self,filename):
        parameter_dict={
            'level_of_theory':None,
            'basis_set':None,
            'runtype':None,'run_params':None,
            'add_runtype':None,'add_params':None,
            'scf_params':None,
            'additional_input':[],
            'memory':None,
            'cores':None,
            'nodes':None,
            'check_file':None,
            'title':None,
            'charge':None,'multiplicity':None,
            'geometry':None
        }
        with open(filename,'r') as myfile:
            contents = myfile.readlines()
        done = False
        for i,line in enumerate(contents):
            if line == '\n':
                done = True
                continue
            line=line.lower()
            if '%' in line:
                translate=[
                    ('%',''),
                    ('chk','check_file'),
                    ('mem','memory'),
                    ('lindaworkers','nodes'),
                    ('nprocshared','cores'),
                    ('nprocs','cores')
                    ]
                for x,y in translate:
                    line = line.replace(x,y)
                k,v = line.split('=')
                parameter_dict[k]=v
            if '#' in [line, contents[i-1], contents[i-2]] and not done:
                line = line.replace('#','').split()
                runs,run_params=[],[]
                for l in line:
                    if l.split('(')[0].split('=')[0] in ['opt','freq','irc','scan']:
                        rps = re.search('(\(.+?\))', l)
                        if rps:
                            run_params.append(rps.group(1).split(','))
                            runs.append(l.split('(')[0])
                        elif '=' in l:
                            run_params.append([l.split('=')[1]])
                            runs.append(l.split('=')[0])
                        else:
                            runs.append(l)
                    elif 'scf' in l:
                        scfps = re.search('(\(.+?\))', l)
                        if scfps:
                            parameter_dict['scf_params']=scfps.group(1).split(',')
                        elif '=' in l:
                            parameter_dict['scf_params']=l.split('=')[1]
                    elif '/' in l:
                        parameter_dict['level_of_theory'],parameter_dict['basis_set'] = l.split('/')
                    else:
                        parameter_dict['additional_input'].append(l)
                runs.append(None)
                run_params.append(None)
                if runs[0]==None:
                    parameter_dict['runtype']='energy'
                else:
                    parameter_dict['runtype']=runs[0]
                    parameter_dict['run_params']=run_params[0]
                    parameter_dict['add_runtype']=runs[1]
                    parameter_dict['add_params']=run_params[1]
            if parameter_dict['title']==None and done:
                parameter_dict['title']=line.repalce('\n','')
                continue
            if parameter_dict['title'] != None and line[0] != ' ':
                parameter_dict['charge'], parameter_dict['multiplicity'] = line.split()
                done = False
                continue
            if parameter_dict['charge'] != None and not done:


        
                    