nb_elements = 500
material_step = '1'
force_value = 1246.01
disp_value = 1.72
sample = '01_2007'
element_type = 'quadratic_tetrahedrons'
material_law = 'Keller_1994'

model = ExtAPI.DataModel.Project.Model

# Change working directory

path = r'C:\Users\U1033_BIOMECA\Desktop\Data_JPR\density_law_fitting'
path_act = r"C:\Users\U1033_BIOMECA\Desktop\Data_JPR\density_law_fitting"
from os import chdir
chdir(path_act)
logfile = open('logfile.txt', 'a')
logfile.write('Starting simulation\n')
chdir(path)

# Import Named selections
try:
    model.NamedSelections.InternalObject.ImportNamedSelectionFromCDBFile(
        path + "\\initial_mesh_size\\" + sample + "_vertebra_" + str(nb_elements) + ".cdb")
    Tree.Refresh()
    logfile.write('named selections imported\n')
except:
    logfile.write('error with named selection importation\n')

# Create conditions

fixed = model.Analyses[0].AddNodalDisplacement()
fixed.Location = model.NamedSelections.Children[0]
fixed.XComponent.Output.DiscreteValues = [Quantity("0 [mm]")]
fixed.YComponent.Output.DiscreteValues = [Quantity("0 [mm]")]
fixed.ZComponent.Output.DiscreteValues = [Quantity("0 [mm]")]

force = model.Analyses[0].AddNodalForce()
force.Location = model.NamedSelections.Children[1]
force.XComponent.Output.DiscreteValues = [Quantity("0 [N]")]
force.YComponent.Output.DiscreteValues = [Quantity("0 [N]")]
force.ZComponent.Output.DiscreteValues = [Quantity(str(force_value) + " [N]")]

displacement = model.Analyses[0].AddNodalDisplacement()
displacement.Location = model.NamedSelections.Children[1]
displacement.XComponent.Output.DiscreteValues = [Quantity("0 [mm]")]
displacement.YComponent.Output.DiscreteValues = [Quantity("0 [mm]")]
displacement.ZComponent.Output.DiscreteValues = [Quantity(str(disp_value) + " [mm]")]

# Prepare output

stress = model.Analyses[0].Solution.AddEquivalentStress()
strain = model.Analyses[0].Solution.AddEquivalentElasticStrain()
reaction = model.Analyses[0].Solution.AddForceReaction()
reaction.BoundaryConditionSelection = fixed
model.Analyses[0].Solution.AddTotalDeformation()
zdef = model.Analyses[0].Solution.AddDirectionalDeformation()
zdef.Location = model.NamedSelections.Children[1]
zdef.NormalOrientation =NormalOrientationType.ZAxis

# Solution imposed force

displacement.Suppressed = True
force.Suppressed = False
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)
solution = model.Analyses[0].Solution

string_results_force = ''
string_results_disp = ''
string_data = sample + '\t' + str(nb_elements) + 'k\t' + element_type + '\t' + str(material_law) + '\t' + str(len(model.Materials.Children)) + '\t' + material_step +'\t'

equivalent_stress = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.StressResults.EquivalentStress, solution.Children)
equivalent_strain = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.StrainResults.EquivalentElasticStrain, solution.Children)
total_deformation = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.DeformationResults.TotalDeformation, solution.Children)
directional_deformation = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.DeformationResults.DirectionalDeformation, solution.Children)

string_results_force += str(total_deformation[0].Maximum).split('[')[0]+'\t'
string_results_force += str(equivalent_strain[0].Maximum).split('[')[0]+'\t'
string_results_force += str(equivalent_stress[0].Maximum).split('[')[0]+'\t'
string_results_force += str(directional_deformation[0].Minimum).split('[')[0]+'\t'

# Solution imposed displacement

displacement.Suppressed = False
force.Suppressed = True
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)
solution = model.Analyses[0].Solution

equivalent_stress = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.StressResults.EquivalentStress, solution.Children)
equivalent_strain = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.StrainResults.EquivalentElasticStrain, solution.Children)
reaction = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.ProbeResults.ForceReaction, solution.Children)

string_results_disp += str(reaction[0].XAxis).split('[')[0]+'\t'
string_results_disp += str(reaction[0].YAxis).split('[')[0]+'\t'
string_results_disp += str(reaction[0].ZAxis).split('[')[0]+'\t'
string_results_disp += str(reaction[0].Total).split('[')[0]+'\t'
string_results_disp += str(equivalent_strain[0].Maximum).split('[')[0]+'\t'
string_results_disp += str(equivalent_stress[0].Maximum).split('[')[0]+'\t'


# Print Results

f = open('results.txt', 'a')
f.write(string_data + '\\' + string_results_disp + '\\' + string_results_force + '\n')
f.close()

