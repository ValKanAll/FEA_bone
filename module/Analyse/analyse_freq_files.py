import os
import numpy as np
path = r"C:\Users\U1033_BIOMECA\Desktop\Data_JPR\density_law_fitting\freq_file_size"

os.chdir(path)

sample_list = ['01_2007', '03', '07_2007', '11_2007', '12_2007', '13_2007', '15_2007', '17_2007', '31', '32', '35', '37', '40', '43', '44']
element_list = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]
material_step = '1'

analyse_file = open('analysis.txt', 'w')
analyse_file.write('sample' + '\t' + 'total_el' + '\t' + 'rho_moy' + '\t' + 'E_moy' + '\t' + 'rho_med' + '\t' + 'E_med' + '\n')

for sample in ['07_2007', '32', '37']:
    for nb_elements in element_list:
        file_name = sample + '_vertebra_' + str(nb_elements) + '-Freq.txt'
        file = open(file_name, 'r')
        total_el = 0
        rho_moy = 0
        E_moy = 0
        rho_list = []
        E_list = []
        for line in file:
            values = line.split('\t')
            if len(values) == 3:
                rho = float(values[0])
                E = float(values[1])
                num = int(values[2])
                for i in range(num):
                    rho_list.append(rho)
                    E_list.append(E)
                
                total_el += num
                rho_moy += rho*num
                E_moy += E*num
        E_moy /= total_el
        rho_moy /= total_el
        E_med = np.median(E_list)
        rho_med = np.median(rho_list)
        analyse_file.write(sample + '\t' + str(total_el) + '\t' + str(rho_moy) + '\t' + str(E_moy) + '\t' + str(rho_med) + '\t' + str(E_med) + '\n')
        file.close()
analyse_file.close()