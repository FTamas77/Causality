from owlready2 import *
import os

owlready2.JAVA_EXE = "C:\\Program Files\\Java\\jre1.8.0_351\\bin\\java.exe"
onto_path.append(".")
onto = get_ontology("ontology/onto.owl")
onto.load(reload=True)


# TODO: move into a separate file
class ontology_handler:

    #def openOntology(self):
    #self.onto = get_ontology("ontology/onto.owl")
    #self.onto.load(reload=True)

    #def createOntology(self):
    #self.onto = get_ontology("http://myonto.org/onto.owl")
    #self.onto.save(file="ontology/onto.owl", format="rdfxml")

    def addClasses(self, myList):
        print(Thing)

        my_new_class = types.new_class("NewClassName", (Thing, ))
        print(my_new_class)

        my_obj = my_new_class("myObjName", namespace=onto)  # make an instance
        print(my_obj)  # qwerty.myObjName

        return


# for dewvelopment
if __name__ == '__main__':
    myList = []
    myList.append([
        'Fuel_consumptions_liters_value'
        'Co2_emissions', 'Active_cylinders', 'Engine_powers_out',
        'Motor_p1_maximum_powers', 'Engine_temperature_derivatives',
        'Motor_p0_speeds', 'Engine_temperatures', 'Wheel_speeds', 'Velocities',
        'Times'
    ])

    myOntology = ontology_handler()
    myOntology.openOntology()
    myOntology.addClasses(myList)
