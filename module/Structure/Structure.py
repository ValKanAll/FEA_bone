
class Simulation:
    def __init__(self, ID_sim, ID_mekamesh, loads, script_path, results):
        # Test type
        if type(ID_sim) == str:
            self.ID_sim = ID_sim
        else:
            raise NameError('ID_sim is not a string')
        if type(ID_mekamesh) == str:
            self.ID_mekamesh = ID_mekamesh
        else:
            raise NameError('ID_mekamesh is not a string')
        try:
            for l in loads:
                if type(l) != Load:
                    raise NameError('load in load list is not a Load type')
            self.loads = loads
        except:
            raise NameError('load is not a list of Load type')
        if type(script_path) == str:
            self.script_path = script_path
        else:
            raise NameError('script_path is not a string')

        try:
            for r in results:
                if type(r) != Result:
                    raise NameError('result in result list is not a Result type')
            self.results = results
        except:
            raise NameError('result is not a list of Result type')

    def get_ID_simulation(self):
        return self.ID_sim

    def get_ID_mekamesh(self):
        return self.ID_mekamesh

    def get_loads(self):
        return self.loads

    def get_script_path(self):
        return self.script_path

    def get_result(self):
        return self.results

    def add_load(self, new_load):
        if type(new_load) == Load:
            if new_load.get_ID_simulation() == self.ID_sim:
                for load in self.loads:
                    if load.get_ID_load() == new_load.get_ID_load():
                        raise NameError('load already in the list')
                else:
                    self.results.append(new_load)
            else:
                raise NameError('simulation ID does not match')
        else:
            raise NameError('new load is not type Load')

    def suppress_load(self, ID_load):
        index = 0
        found = False
        while not found:
            for load in self.loads:
                if load.get_ID_load() == ID_load:
                    self.loads.pop(index)
                    found = True
                index += 1
            else:
                raise NameError('load ID not found in the list')
                found = True

    def add_result(self, new_result):
        if type(new_result) == Result:
            if new_result.get_ID_simulation() == self.ID_sim:
                for result in self.results:
                    if result.get_ID_result() == new_result.get_ID_result():
                        raise NameError('result already in the list')
                else:
                    self.results.append(new_result)
            else:
                raise NameError('simulation ID does not match')
        else:
            raise NameError('new result is not type Result')

    def suppress_result(self, ID_result):
        index = 0
        found = False
        while not found:
            for result in self.results:
                if result.get_ID_result() == ID_result:
                    self.results.pop(index)
                    found = True
                index += 1
            else:
                raise NameError('result ID not found in the list')
                found = True

    def modify_ID_sim(self, new_value):
        if type(new_value) == str:
            self.ID_sim = new_value
        else:
            raise NameError('new ID_sim is not a string')
        return self.ID_sim

    def modify_ID_mekamesh(self, new_value):
        if type(new_value) == str:
            self.ID_mekamesh = new_value
        else:
            raise NameError('new ID_mekamesh is not a string')
        return self.ID_mekamesh

    def modify_script_path(self, new_path):
        if type(new_path) == str:
            self.script_path = new_path
        else:
            raise NameError('new script path is not a string')
        return self.script_path


class Result:
    def __init__(self, ID_result):
        pass
    #type stress strain VM volume


class Load:
    def __init__(self, ID_load, load_type, vector):
        # Test type
        if type(ID_load) == str:
            self.ID_load = ID_load
        else:
            raise NameError('ID_load is not a string')
        if type(load_type) in ['force', 'moment']:
            self.load_type = load_type
        else:
            raise NameError('load type is not properly defined')
        if type(vector) == list and len(vector) == 3:
            self.vector = vector
        else:
            raise NameError('vector of the load is not a vector of 3')

    def get_ID_load(self):
        return self.ID_load

    def get_load_type(self):
        return self.load_type

    def get_vector(self):
        return self.vector

    def modify_ID_load(self, new_value):
        if type(new_value) == str:
            self.ID_load = new_value
        else:
            raise NameError('new ID_load is not a string')
        return self.ID_load

    def modify_load_type(self, new_load_type):
        if type(new_load_type) in ['force', 'moment']:
            self.load_type = new_load_type
        else:
            raise NameError('new load type is not properly defined')
        return self.load_type

    def modify_vector(self, new_vector):
        if type(new_vector) == list and len(new_vector) == 3:
            self.vector = new_vector
        else:
            raise NameError('new vector load is not a vector of 3')
        return self.vector


class Mekamesh:
    def __init__(self, ID_mekamesh, path, ID_mesh, ID_scan, site):
        # Test type
        if type(ID_mesh) == str:
            self.ID_mesh = ID_mesh
        else:
            raise NameError('ID_mesh is not a string')
        if type(path) == str:
            self.path = path
        else:
            raise NameError('mesh path is not a string')
        if type(ID_scan) == str:
            self.ID_scan = ID_scan
        else:
            raise NameError('ID_scan is not a string')
        if type(site) == str:
            self.site = site
        else:
            raise NameError('site is not a string')
        if type(ID_mekamesh) == str:
            self.ID_mekamesh = ID_mekamesh
        else:
            raise NameError('ID_mekamesh')

    # Define scans
        self.simulation_list = []

    def get_simulation_list(self):
        return self.simulation_list

    def add_simulation(self, new_simulation):
        if type(new_simulation) == Simulation:
            if new_simulation.get_ID_mekamesh() == self.ID_mekamesh:
                for simulation in self.simulation_list:
                    if simulation.get_ID_simulation() == new_simulation.get_ID_simulation():
                        raise NameError('simulation already in the list')
                else:
                    self.simulation_list.append(new_simulation)
            else:
                raise NameError('mekamesh ID does not match')
        else:
            raise NameError('new simulation is not type Simulation')

    def suppress_simulation(self, ID_simulation):
        index = 0
        found = False
        while not found:
            for simulation in self.simulation_list:
                if simulation.get_ID_simulation() == ID_simulation:
                    self.simulation_list.pop(index)
                    found = True
                index += 1
            else:
                raise NameError('simulation ID not found in the list')
                found = True

    def get_ID_mekamesh(self):
        return self.ID_mekamesh

    def get_ID_mesh(self):
        return self.ID_mesh

    def get_ID_scan(self):
        return self.ID_scan

    def get_path(self):
        return self.path

    def get_site(self):
        return self.site

    def modify_ID_mekamesh(self, new_ID):
        if type(new_ID) == str:
            self.ID_mekamesh = new_ID
        else:
            raise NameError('new ID mekamesh is not a string')
        return self.ID_mekamesh

    def modify_ID_mesh(self, new_ID):
        if type(new_ID) == str:
            self.ID_mesh = new_ID
        else:
            raise NameError('new ID mesh is not a string')
        return self.ID_mesh

    def modify_ID_scan(self, new_ID):
        if type(new_ID) == str:
            self.ID_scan = new_ID
        else:
            raise NameError('new ID scan is not a string')
        return self.ID_scan

    def modify_path(self, new_path):
        if type(new_path) == str:
            self.path = new_path
        else:
            raise NameError('new path is not a string')
        return self.path

    def modify_site(self, new_site):
        if type(new_site) == str:
            self.path = new_site
        else:
            raise NameError('new site is not a string')
        return self.site

    
class Mesh:
    def __init__(self, ID_mesh, path, ID_stl, site, named_selection=False):
        # Test type
        if type(ID_mesh) == str:
            self.ID_mesh = ID_mesh
        else:
            raise NameError('ID_mesh is not a string')
        if type(path) == str:
            self.path = path
        else:
            raise NameError('mesh path is not a string')
        if type(ID_stl) == str:
            self.ID_stl = ID_stl
        else:
            raise NameError('ID_stl is not a string')
        if type(site) == str:
            self.site = site
        else:
            raise NameError('site is not a string')
        if type(named_selection) == bool:
            self.named_selection = named_selection
        else:
            raise NameError('named_selection is not a boolean')

    # Define scans
        self.mekamesh_list = []

    def get_mekamesh_list(self):
        return self.mekamesh_list

    def add_stl(self, new_mekamesh):
        if type(new_mekamesh) == Mekamesh:
            if new_mekamesh.get_ID_mesh() == self.ID_mesh:
                for mekamesh in self.mekamesh_list:
                    if mekamesh.get_ID_mekamesh() == new_mekamesh.get_ID_mekamesh():
                        raise NameError('mekamesh already in the list')
                else:
                    self.mekamesh_list.append(new_mekamesh)
            else:
                raise NameError('Mesh ID does not match')
        else:
            raise NameError('new mekamesh is not type Mekamesh')

    def suppress_mekamesh(self, ID_mekamesh):
        index = 0
        found = False
        while not found:
            for mekamesh in self.mekamesh_list:
                if mekamesh.get_ID_mekamesh() == ID_mekamesh:
                    self.mekamesh_list.pop(index)
                    found = True
                index += 1
            else:
                raise NameError('mekamesh ID not found in the list')
                found = True

    def get_ID_mesh(self):
        return self.ID_mesh

    def get_ID_stl(self):
        return self.ID_stl

    def get_path(self):
        return self.path

    def get_site(self):
        return self.site

    def get_named_selection(self):
        return self.named_selection

    def modify_ID_mesh(self, new_ID):
        if type(new_ID) == str:
            self.ID_mesh = new_ID
        else:
            raise NameError('new ID mesh is not a string')
        return self.ID_mesh

    def modify_ID_stl(self, new_ID):
        if type(new_ID) == str:
            self.ID_stl = new_ID
        else:
            raise NameError('new ID scan is not a string')
        return self.ID_stl

    def modify_path(self, new_path):
        if type(new_path) == str:
            self.path = new_path
        else:
            raise NameError('new path is not a string')
        return self.path

    def modify_site(self, new_site):
        if type(new_site) == str:
            self.path = new_site
        else:
            raise NameError('new site is not a string')
        return self.site

    def modify_named_selection(self, new_named_selection):
        if type(new_named_selection) == bool:
            self.named_selection = new_named_selection
        else:
            raise NameError('new named selection value is not a boolean')
        return self.named_selection


class stl_volume:
    def __init__(self, ID_stl, path, ID_scan, site):
        if type(ID_stl) == str:
            self.ID_stl = ID_stl
        else:
            raise NameError('ID_stl is not a string')
        if type(path) == str:
            self.path = path
        else:
            raise NameError('mesh path is not a string')
        if type(ID_scan) == str:
            self.ID_scan = ID_scan
        else:
            raise NameError('ID_scan is not a string')
        if type(site) == str:
            self.site = site
        else:
            raise NameError('site is not a string')

    # Define scans
        self.mesh_list = []

    def get_mesh_list(self):
        return self.mesh_list

    def add_mesh(self, new_mesh):
        if type(new_mesh) == Mesh:
            if new_mesh.get_ID_stl() == self.ID_stl:
                for mesh in self.mesh_list:
                    if mesh.get_ID_mesh() == new_mesh.get_ID_mesh():
                        raise NameError('mesh already in the list')
                else:
                    self.mesh_list.append(new_mesh)
            else:
                raise NameError('stl ID does not match')
        else:
            raise NameError('new mesh is not type Mesh')

    def suppress_mesh(self, ID_mesh):
        index = 0
        found = False
        while not found:
            for mesh in self.mesh_list:
                if mesh.get_ID_mesh() == ID_mesh:
                    self.mesh_list.pop(index)
                    found = True
                index += 1
            else:
                raise NameError('mesh ID not found in the list')
                found = True

    def get_ID_stl(self):
        return self.ID_stl

    def get_ID_scan(self):
        return self.ID_scan

    def get_path(self):
        return self.path

    def get_site(self):
        return self.site

    def modify_ID_stl(self, new_ID):
        if type(new_ID) == str:
            self.ID_stl = new_ID
        else:
            raise NameError('new ID stl is not a string')
        return self.ID_stl

    def modify_ID_scan(self, new_ID):
        if type(new_ID) == str:
            self.ID_scan = new_ID
        else:
            raise NameError('new ID scan is not a string')
        return self.ID_scan

    def modify_path(self, new_path):
        if type(new_path) == str:
            self.path = new_path
        else:
            raise NameError('new path is not a string')
        return self.path

    def modify_site(self, new_site):
        if type(new_site) == str:
            self.path = new_site
        else:
            raise NameError('new site is not a string')
        return self.site


class Scan:
    def __init__(self, ID_scan, path, resolution):
        # Test type
        if type(ID_scan) == str:
            self.ID_scan = ID_scan
        else:
            raise NameError('ID_scan is not a string')
        if type(path) == str:
            self.path = path
        else:
            raise NameError('path is not a string')
        if len(resolution) == 3 and type(resolution) == list:
            self.resolution = resolution
        else:
            raise NameError('resolution is not a list or is not a size 3')

        # Define scans
        self.stl_list = []

    def get_stl_list(self):
        return self.stl_list

    def add_stl(self, new_stl):
        if type(new_stl) == stl_volume:
            if new_stl.get_ID_scan() == self.ID_scan:
                for stl in self.stl_list:
                    if stl.get_ID_stl() == new_stl.get_ID_stl():
                        raise NameError('stl volume already in the list')
                else:
                    self.stl_list.append(new_stl)
            else:
                raise NameError('Scan ID does not match')
        else:
            raise NameError('new stl volume is not type stl volume')

    def suppress_stl(self, ID_stl):
        index = 0
        found = False
        while not found:
            for stl in self.stl_list:
                if stl.get_ID_stl() == ID_stl:
                    self.stl_list.pop(index)
                    found = True
                index += 1
            else:
                raise NameError('stl ID not found in the list')
                found = True

    def get_ID_scan(self):
        return self.ID_scan

    def get_path(self):
        return self.path

    def get_resolution(self):
        return self.resolution

    def modify_ID_scan(self, new_ID):
        if type(new_ID) == str:
            self.ID_scan = new_ID
        else:
            raise NameError('new ID scan is not a string')
        return self.ID_scan

    def modify_path(self, new_path):
        if type(new_path) == str:
            self.path = new_path
        else:
            raise NameError('new path is not a string')
        return self.path

    def modify_resolution(self, new_resolution):
        if type(new_resolution) == list and len(new_resolution) == 3:
            self.resolution = new_resolution
        else:
            raise NameError('new resolution is not a list of 3')
        return self.resolution

        
class Patient:
    def __init__(self, ID_patient, age, sex, complement=None):
        # Test type
        if type(ID_patient) == str:
            self.ID_patient = ID_patient
        else:
            raise NameError('ID_patient is not a string')
        if type(age) == int:
            self.age = age
        else:
            raise NameError('age is not a int')
        if sex in ['F', 'M', 'unknown']:
            self.sex = sex
        else:
            raise NameError('sex is not properly defined')
        if type(complement) == str:
            self.complement = complement
        else:
            raise NameError('Complement info on patient is not a string')

        # Define scans
        self.scan_list = []

    def get_scan_list(self):
        return self.scan_list

    def add_scan(self, new_scan):
        if type(new_scan) == Scan:
            if new_scan.get_ID_scan() == self.ID_patient:
                for scan in self.scan_list:
                    if scan.get_ID_scan() == new_scan.get_ID_scan():
                        raise NameError('scan already in the list')
                else:
                    self.scan_list.append(new_scan)
            else:
                raise NameError('Patient ID does not match')
        else:
            raise NameError('new scan is not type scan')

    def suppress_scan(self, ID_scan):
        index = 0
        found = False
        while not found:
            for scan in self.scan_list:
                if scan.get_ID_scan() == ID_scan:
                    self.scan_list.pop(index)
                    found = True
                index += 1
            else:
                raise NameError('scan ID not found in the list')
                found = True

    def get_ID_patient(self):
        return self.ID_patient

    def get_age(self):
        return self.age

    def get_sex(self):
        return self.sex

    def get_complement(self):
        return self.complement

    def modify_ID_patient(self, new_ID):
        if type(new_ID) == str:
            self.ID_patient = new_ID
        else:
            raise NameError('new ID scan is not a string')
        return self.ID_patient

    def modify_age(self, new_age):
        if type(new_age) == int:
            self.age = new_age
        else:
            raise NameError('new age is not a string')
        return self.age

    def modify_sex(self, new_sex):
        if type(new_sex) == str:
            self.sex = new_sex
        else:
            raise NameError('new sex scan is not properly defined')
        return self.sex

    def modify_complement(self, new_complement):
        if type(new_complement) == str:
            self.sex = new_complement
        else:
            raise NameError('new complement is not properly defined')
        return self.complement

