from owlready2 import *
import os

owlready2.JAVA_EXE = "C:\\Program Files\\Java\\jre1.8.0_351\\bin\\java.exe"

onto = get_ontology("ontology/caseStudy.owl").load()
onto.load(reload=True)

print('\n\nList of the imported ontologies:\n', list(onto.imported_ontologies))
print('\n\nList of the individuals:\n', list(onto.individuals()))
print('\n\nList of the classes:\n', list(onto.classes()))
print('\n\nList of the properties:\n', list(onto.properties()))
print('\n\nList of the object_properties:\n', list(onto.object_properties()))
print('\n\nList of the data_properties:\n', list(onto.data_properties()))
print('\n\nList of the annotation_properties:\n',
      list(onto.annotation_properties()))
print('\n\nList of the disjoints:\n', list(onto.disjoints()))
print('\n\nList of the disjoint_classes:\n', list(onto.disjoint_classes()))
print('\n\nList of the disjoint_properties:\n',
      list(onto.disjoint_properties()))
print('\n\nList of the different_individuals:\n',
      list(onto.different_individuals()))
print('\n\nList of the rules:\n', list(onto.rules()))
print('\n\nList of the variables:\n', list(onto.variables()))

# subject - verb - object
print('\n\niri and name and is_a:\n')
print(onto.LifeCycleEnergySource_Renewable_ICEV_vehicle_1.iri)
print(onto.LifeCycleEnergySource_Renewable_ICEV_vehicle_1.name)
print(onto.LifeCycleEnergySource_Renewable_ICEV_vehicle_1.is_a)
