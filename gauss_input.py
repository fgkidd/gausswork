#Gaussian input file generator class
import re
from subprocess import call
from gauss_output import *
class Gauss_Input():
    def __init__(self,filename=None,parameters=None):
        if filename != None:
            parameters = self._get_parameters(filename)
        for k, v in parameters.items():
            setattr(self,k,v)
    def __str__(self):
        self._write()
        return self._input_file
    def run(self):
        with open('system_information.txt','r') as myfile: 
            exe = '"'+myfile.readline().split('=')[1]+'"'
        dir = os.getcwd()
        filename = self.title.split('.gjf')[0].split('.com')[0]
        inp = '"'+dir+filename+'.gjf"'
        out = '"'+dir+filename+'.out"'
        try:
            os.remove(inp)
            os.remove(out)
        except:
            with open(inp,'a') as myfile:
                myfile.write(self._input_file)
            call(exe,inp,out)
    '''     
    @property
    def geometry(self):
        self.geometry = geometry
    
    @geometry.setter
    def geometry(self,value):
        if type(value) == str:
    '''
    def _get_parameters(self,filename):
        parameter_dict={
            'level_of_theory':None,
            'basis_set':None,
            'runtype':None,'run_params':None,
            'add_runtype':None,'add_params':None,
            'scf_params':None,
            'additional_input':[], 'ending_input':[],
            'memory':None, 'cores':None, 'nodes':None,
            'check_file':None,
            'title':None,
            'charge':None,'multiplicity':None,
            'geometry':'',
            'atoms':[], 'cartesian_coordinates':[]
        }
        with open(filename,'r') as myfile:
            contents = myfile.readlines()
        done = False
        runs,run_params=[],[]
        for line in contents:
            if line == '\n':
                done = True
                continue
            if '%' in line:
                translate=[
                    ('%chk','check_file'),
                    ('%mem','memory'),
                    ('%lindaworkers','nodes'),
                    ('%nprocshared','cores'),
                    ('%nprocs','cores')
                    ]
                k,v = line.split('=')
                key=k.lower()
                for x,y in translate:
                    key=key.replace(x,y)
                parameter_dict[key]=v.replace('\n','')
            elif not done and parameter_dict['title']==None:
                line = line.replace('#','').split()
                for l in line:
                    if (l.split('(')[0].split('=')[0]) in ['opt','freq','irc','scan']:
                        rps = re.search('(\(.+?\))', l)
                        if rps:
                            run_params.append(rps.group(1).replace('(','').replace(')','').split(','))
                            runs.append(l.split('(')[0].split('=')[0])
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
                            parameter_dict['scf_params']=[l.split('=')[1]]
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
                parameter_dict['title']=line.replace('\n','')
                continue
            if parameter_dict['title'] != None and line[0] != ' ':
                parameter_dict['charge'], parameter_dict['multiplicity'] = line.split()
                done = False
                continue
            if parameter_dict['charge'] != None and not done:
                a,x,y,z = line.split()
                parameter_dict['geometry']+=line.upper()
                parameter_dict['atoms'].append(a)
                parameter_dict['cartesian_coordinates'].append([float(x),float(y),float(z)])
            if done:
                parameter_dict['ending_input'].append(line)
        return parameter_dict
    def _write(self):
        text = ''
        translate=[
            ('memory','%mem='),
            ('nodes','%lindaworkers=:'),
            ('check_file','%chk='),
            ('cores','%nprocshared=')
            ]
        for k,v in translate:
            val = getattr(self,k)
            if val: text+=v+val+'\n'
        run_options=[
            'runtype','run_params',
            'add_runtype','add_params',
            'level_of_theory','basis_set',
            'scf_params',
            'additional_input'
            ]
        text+='# '
        for r in run_options:
            val = getattr(self,r)
            if val:
                if r=='basis_set': val = '/'+val
                if r=='scf_params': val='scf '+str(val)+'\n'
                if r=='additional_input': 
                    for add_inp in val:
                        text+=add_inp+' '
                    continue
                text+=str(val) + ' '
        text+='\n\n'+self.title+'\n\n'+self.charge+' '+self.multiplicity+'\n'+self.geometry+'\n'
        for e in self.ending_input:
            text+=e
        text = text.replace("'","").replace(' [','=(').replace(']',')').replace(' /','/').replace('::',':')
        self._input_file = text


g=Gauss_Input('G:/My Drive/Work/2017/Species-4-Kin/H2NN.gjf')
g.level_of_theory='HF'
g.basis_Set='3-21'
print(g)
g.run()