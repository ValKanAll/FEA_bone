import os
import subprocess

cmd_workbench_template = r"C:\Users\U1033_BIOMECA\Desktop\Data_JPR\density_law_fitting\template\config_workbench_template.wbjn"
script_act_template = r"C:\Users\U1033_BIOMECA\Desktop\Data_JPR\density_law_fitting\template\vertebra_analysis_template.py"

cmd_workbench = r"C:\Users\U1033_BIOMECA\Desktop\Data_JPR\density_law_fitting\config_workbench.wbjn"
script_act = r"C:\Users\U1033_BIOMECA\Desktop\Data_JPR\density_law_fitting\vertebra_analysis.py"

#nb_elements = 700
#material_step = 20

sample_list = ['01_2007', '07_2007', '11_2007', '12_2007', '13_2007', '15_2007', '17_2007', '03', '31', '32', '35', '37', '40', '43', '44']
force_value_list = [1246.01, 3230.23, 1296.66, 651.34, 2336.36, 2564.94, 1335.21, 1924.38 , 3071.55, 4255.76, 1726.29, 2506.01, 5480.60, 2787.62, 1808.06]
disp_value_list = [1.72, 2.27, 2.42, 1.19, 1.48, 1.56, 2.50, 0.63, 0.94, 1.09, 1.17, 1.09, 1.56, 0.70, 0.48]
element_type = 'quadratic_tetrahedrons'
material_law = 'Keller_1994'

step_list = ['1'] 
element_list = [1400, 1500, 1600, 1700, 1800, 1900, 2000]

for i in [1, 9, 11]:
    sample = sample_list[i]
    force_value = force_value_list[i]
    disp_value = disp_value_list[i]
    for nb_elements in element_list:
        material_step = '1'
        try:
            # Creating the sample specific import mesh script
            with open(cmd_workbench_template, 'r') as f_in:
                with open(cmd_workbench, 'w+') as f_out:
                    #line = f_in.readline()
                    for line in f_in:
                        if "nb_elements = " in line:
                            line = "nb_elements = %s\n" % str(nb_elements)
                            print(line)
                        elif "material_step = " in line:
                            line = "material_step = '%s'\n" % material_step
                        elif "sample = " in line:
                            line = "sample = '%s'\n" % sample
                            print(line)
                        f_out.write(line)
                        #line = f_in.readline()
            f_in.close()
            f_out.close()

            # Creating the sample specific ACT script
            with open(script_act_template, 'r') as f_in:
                with open(script_act, 'w+') as f_out:
                    #line = f_in.readline()
                    for line in f_in:
                        if "nb_elements =" in line:
                            line = "nb_elements = %s\n" % str(nb_elements)
                        elif "material_step =" in line:
                            line = "material_step = '%s'\n" % material_step
                        elif "force_value =" in line:
                            line = "force_value = %s\n" % str(force_value)
                        elif "disp_value =" in line:
                            line = "disp_value = %s\n" % str(disp_value)
                        elif "element_type =" in line:
                            line = "element_type = '%s'\n" % element_type
                        elif "material_law =" in line:
                            line = "material_law ='%s'\n" % material_law
                        elif "sample =" in line:
                            line = "sample = '%s'\n" % sample
                            print(line)
                        f_out.write(line)
                        #line = f_in.readline()
            f_in.close()
            f_out.close()
            
            print('script act created')

            cmd = r'"C:\Program Files\ANSYS Inc\v193\Framework\bin\Win64\RunWB2.exe"  -B -R "%s"' % cmd_workbench
            print(cmd)
            subprocess.check_call(cmd, shell=True)
        except:
            print("ERROR : %s" % sample)