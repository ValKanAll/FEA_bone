import Material_law as ml
import os
import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt

dirname = os.path.dirname(__file__)

material_data_path = os.path.join(dirname, "data/Bone_Material_Law.xlsx")


material_data = ml.MaterialData(material_data_path)
exp_density = [0.125487633, 0.143974889, 0.1635147, 0.163649298, 0.1221565, 0.128381269, 0.24684165, 0.151251497, 0.262643418, 0.234034558, 0.226609347, 0.189364322, 0.286558473, 0.255658613, 0.15774732]
exp_modulus = [0.02385, 0.06651, 0.06174, 0.02374, 0.02282, 0.07540, 0.06854, 0.01989, 0.11376, 0.09991, 0.05272, 0.07186, 0.18118, 0.11556, 0.08692]

def getColor(N, idx):
    cmap = mpl.cm.get_cmap('rainbow')
    norm = mpl.colors.Normalize(vmin=0.0, vmax=N - 1)
    return cmap(norm(idx))

N_laws = len(material_data.material_laws)
i = 0
plt.figure()

for law in material_data.material_laws:
    cond_vertebra1 = (law.get_site().find('vertebra') > 0)
    cond_vertebra2 = (law.get_site().find('spine') > 0)
    #if cond_vertebra1 or cond_vertebra2:
    formula = law.get_formula()
    range_measure = law.get_range_measure()
    t = np.linspace(range_measure[0], range_measure[1], 100)
    y = [formula(x) for x in t]
    ref = law.get_name()+'_'+law.get_site()
    plt.plot(t, y, label=ref, color=getColor(N_laws, i))

    print(law.get_name()+'\t'+law.get_site() + '\tE(rho=0.129g/cm3):\t'+ str(formula(0.129)*1000) + 'MPa')
    print(law.get_law())
    i += 1


plt.scatter(exp_density, exp_modulus, label='experimental_data', color='black', marker='+')
plt.tight_layout()
plt.legend(loc='upper right', borderaxespad=0.)
plt.xlabel('density (g/cm^3)')
plt.ylabel('E (GPa)')
plt.show()


