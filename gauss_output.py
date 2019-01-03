import re
class Gauss_Output():
    def __init__(self,filename):
        parameters = self._get_parameters(filename)
        for k,v in parameters.items():
            setattr(self,k,v)
    def _get_parameters(self,filename):
        parameter_dict={
            'frequencies':[],
            'force_constants':[],
            'reduced_masses':[],
            'rotational_constants':[],
            'E':None,'H':None,'G':None,'U':None,
            'geometries':[],
            'atoms':[], 'cartesian_coordinates':[]
        }
        with open(filename,'r') as myfile:
            contents = myfile.readlines()
        geom_here,begin_geom,atom_here = False, False, False
        for line in contents:
            translate=[
                ('Frequencies','frequencies'),
                ('Red. masses','reduced_masses'),
                ('Frc consts','force_constants'),
                ('Thermal correction to Energy','UPC'),
                ('zero-point Energies','E_ZPE'),
                ('thermal Energies','U'),
                ('Enthalpies','H'),
                ('Free Energies','G')
            ]
            for t, k in translate:
                if t in line:
                    try:
                        pieces = line.split('--')[1]
                        parameter_dict[k].extend(pieces.split())
                    except:
                        pieces = line.split('=')[1]
                        parameter_dict[k]=float(pieces)
            if (parameter_dict['rotational_constants'] == []) and ('(GHZ)' in line): 
                parameter_dict['rotational_constants'].extend(line.split(':')[1].split())
            if 'Standard orientation' in line:
                geom=[]
                geom_here = True
            if geom_here and '1' in line:
                begin_geom = True
            if begin_geom and (not '--' in line):
                geom.append(line.split()[3:6])
            if begin_geom and '--' in line:
                geom_here,begin_geom = False, False
                parameter_dict['cartesian_coordinates'].extend(geom)
            if 'Charge = ' in line:
                atom_here = True
            if atom_here and len(line.split())==4:
                parameter_dict['atoms'].append(line.split()[0])
            if atom_here and line == '\n':
                atom_here = False
        parameter_dict['E']=float(parameter_dict['U'])-float(parameter_dict['UPC'])
        return parameter_dict
g=Gauss_Output('G:/My Drive/Work/2017/Species-4-Kin/H2NOandHNO.out')