import Material_law as ml
import os
import numpy as np
import math
import matplotlib.pyplot as plt

dirname = os.path.dirname(__file__)

material_data_path = os.path.join(dirname, "data/Bone_Material_Law.xlsx")


material_data = ml.MaterialData(material_data_path)

plt.figure()
for law in material_data.material_laws:
    cond_vertebra1 = (law.get_site().find('vertebra') > 0)
    cond_vertebra2 = (law.get_site().find('spine') > 0)
    if cond_vertebra1 or cond_vertebra2:
        formula = law.get_formula()
        range_measure = law.get_range_measure()
        t = np.linspace(range_measure[0], range_measure[1], 100)
        y = [formula(x) for x in t]
        ref = law.get_name()+'_'+law.get_site()
        plt.plot(t, y, label=ref)

        print(law.get_name()+'\t'+law.get_site() + '\tE(rho=0.129g/cm3):\t'+ str(formula(0.129)*1000) + 'MPa')
        print(law.get_law())

plt.tight_layout()
plt.legend(loc='upper right', borderaxespad=0.)
plt.xlabel('density (g/cm^3)')
plt.ylabel('E (GPa)')
plt.show()


