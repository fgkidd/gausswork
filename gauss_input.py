#Gaussian input file generator class
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
            'memory':None,
            'cores':None,
            'nodes':None,
            'check_file':None,
            'charge':None,'multiplicity':None,
            'geometry':None
        }
        with open(filename,'r') as myfile:
            contents = myfile.readlines()
        for i,line in enumerate(contents):
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
            if '#' in [line, contents[i-1], contents[i-2]]:
                line = line.replace('#','')



        
                    