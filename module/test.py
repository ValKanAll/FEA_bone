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
    if law.measure == 'ρapp':
        formula = law.get_formula()
        range_measure = law.get_range_measure()
        t = np.linspace(range_measure[0], range_measure[1], 100)
        y = [formula(x) for x in t]
        plt.plot(t, y, label=law.get_name()+'_'+law.get_site())
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.show()


