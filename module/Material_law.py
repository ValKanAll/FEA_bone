import pandas as pd
import os
import Calculator as calc

dirname = os.path.dirname(__file__)

material_data_path = os.path.join(dirname, "data/Bone_Material_Law.xlsx")


class MaterialLaw:
    def __init__(self, name, site, measure, law, range_measure, speed_rate):
        self.name = name
        self.site = site
        self.measure = measure
        self.law = law
        self.range_measure = range_measure
        self.speed_rate = speed_rate

    def get_name(self):
        return self.name

    def get_site(self):
        return self.site

    def get_measure(self):
        return self.measure

    def get_range_measure(self):
        return self.range_measure

    def get_speed_rate(self):
        return self.speed_rate

    def modify_name(self, new_name):
        self.name = new_name

    def modify_site(self, new_site):
        self.site = new_site

    def modify_measure(self, new_measure):
        self.measure = new_measure

    def modify_law(self, new_law):
        self.law = new_law

    def modify_range(self, new_range):
        self.range_measure = new_range

    def modify_speed_rate(self, new_speed_rate):
        self.speed_rate = new_speed_rate

    def get_formula(self, rate=None):
        if not rate:
            _rate = self.speed_rate[0]
        else:
            _rate = rate
        self_measure = self.measure

        def fun(density):
            formula = self.law.split('=')[-1]
            _vars = {self_measure: density, 'eps_dev': _rate}
            return calc.evaluate(formula, _vars)

        return fun


class MaterialData:
    def __init__(self, path):
        self.path = path
        self.data = pd.read_excel(self.path)
        self.values = self.data.values
        self.columns = self.data.columns
        self.index = self.data.index
        self.number_material_laws = self.index.stop - self.index.start
        self.material_laws = []
        for i in range(self.index.stop - self.index.start):
            name = self.values[i][0]
            site = self.values[i][1]
            measure = self.values[i][3]
            law = self.values[i][5]
            range_measure = [float(x) for x in self.values[i][4].split('-')]
            range_measure.sort()
            speed_rate = [float(_x) for _x in self.values[i][7].split('-')]
            self.material_laws.append(MaterialLaw(name, site, measure, law, range_measure, speed_rate))

    def add_material_law(self, new_material_law):
        if type(new_material_law) == MaterialLaw:
            if new_material_law not in self.material_laws:
                self.material_laws.append()
            else:
                return 'Material law already in the list'
        else:
            return 'Type is not MaterialLaw'

    def remove_material_law(self, law):
        if type(law) == MaterialLaw:
            index_law = 0
            for mat_law in self.material_laws:
                if mat_law == law:
                    self.material_laws.pop(index_law)
                index_law += 1
            else:
                return 'Material law not in the list'
        else:
            return 'Type is not MaterialLaw'






