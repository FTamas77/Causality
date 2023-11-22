from owlready2 import *
import os

# configuration
owlready2.JAVA_EXE = "C:\\Program Files\\Java\\jre1.8.0_351\\bin\\java.exe"
onto_path.append(".")

# https://stackoverflow.com/questions/66965475/creating-an-instance-in-owlready2-creates-a-completely-new-class-instead-of-asig
# IRI must be formatted as a link - even if it's a fake one. For example, if IRI is "http://test.org/new.owl", my code works perfectly.
onto = get_ontology("http://test.org/new.owl")
# onto = get_ontology("ontology/co2mpas.owl")
# we always create a new ontology
# onto = get_ontology("ontology/co2mpas.owl").load()


with onto:

    class Measurement(Thing):
        pass

    class TestStage(Thing):
        pass

    class hasTestStage(Measurement >> TestStage, ObjectProperty):
        pass

    ##### Stage 1 #####
    class Calibration(TestStage):
        pass

    ##### Stage 2 #####
    class ModelSelection(TestStage):
        pass

    ##### Stage 3 #####
    class Prediction(TestStage):
        pass

    ####################
    ##### Physical #####
    ####################

    class PhysicalModel(Thing):
        pass

    class hasPhysicalModel(Measurement >> PhysicalModel, ObjectProperty):
        pass

    ###################
    ##### model 1 #####
    ###################

    class co2_model(PhysicalModel):
        pass

    # actual value 1
    class fuel_consumptions_liters_value(co2_model):
        pass

    class has_fuel_consumptions_liters_value(
        co2_model >> fuel_consumptions_liters_value, ObjectProperty
    ):
        pass

    # actual value 2
    class co2_emissions(co2_model):
        pass

    class has_fuel_consumptions_liters_value(
        co2_model >> co2_emissions, ObjectProperty
    ):
        pass

    ###################
    ##### model 2 #####
    ###################

    class engine_model(PhysicalModel):
        pass

    # actual value 1
    class active_cylinders(engine_model):
        pass

    class has_active_cylinders(engine_model >> active_cylinders, ObjectProperty):
        pass

    # actual value 2
    class engine_powers_out(engine_model):
        pass

    class has_engine_powers_out(engine_model >> engine_powers_out, ObjectProperty):
        pass

    # actual value 3
    class engine_temperature_derivatives(engine_model):
        pass

    class has_engine_temperature_derivatives(
        engine_model >> engine_temperature_derivatives, ObjectProperty
    ):
        pass

    ###################
    ##### model 3 #####
    ###################

    class electric_model(PhysicalModel):
        pass

    # actual value 1
    class motor_p1_maximum_powers(electric_model):
        pass

    class has_engine_temperature_derivatives(
        electric_model >> motor_p1_maximum_powers, ObjectProperty
    ):
        pass

    # actual value 2
    class motor_p0_speeds(electric_model):
        pass

    class has_motor_p0_speeds(electric_model >> motor_p0_speeds, ObjectProperty):
        pass

    ###################
    ##### model 4 #####
    ###################

    class control_model(PhysicalModel):
        pass

    # actual value 1
    class engine_temperatures(control_model):
        pass

    class has_engine_temperatures(control_model >> engine_temperatures, ObjectProperty):
        pass

    ###################
    ##### model 5 #####
    ###################

    class wheel_model(PhysicalModel):
        pass

    # actual value 1
    class wheel_speeds(wheel_model):
        pass

    class has_wheel_speeds(wheel_model >> wheel_speeds, ObjectProperty):
        pass

    # actual value 2
    class velocities(wheel_model):
        pass

    class has_velocities(wheel_model >> velocities, ObjectProperty):
        pass

    ############################
    ##### model parameters #####
    ############################

    # https://stackoverflow.com/questions/70061671/how-to-define-multiple-domains-in-owlready2
    # https://stackoverflow.com/questions/77529594/owlready2-create-functionalproperty-to-multiple-classes
    class has_value(FunctionalProperty):
        domain = [
            Or([wheel_speeds, control_model, electric_model, engine_model, co2_model])
        ]
        range = [float]

    class has_time(FunctionalProperty):
        domain = [
            Or([wheel_speeds, control_model, electric_model, engine_model, co2_model])
        ]
        range = [float]


# TODO: create separate ontology handler file
class ontology_handler:
    def save(self):
        return

    def ontology_builder(self, myList):
        return


if __name__ == "__main__":
    myList = []
    myList.append(
        [
            "fuel_consumptions_liters_value",
            "co2_emissions",
            "active_cylinders",
            "engine_powers_out",
            "motor_p1_maximum_powers",
            "engine_temperature_derivatives",
            "motor_p0_speeds",
            "engine_temperatures",
            "wheel_speeds",
            "velocities",
        ]
    )

    Measurement_1 = Measurement()
    co2_model_1 = co2_model()  # it is a "PhysicalModel"
    Measurement_1.hasPhysicalModel = [co2_model_1]

    fuel_consumptions_liters_value_1 = fuel_consumptions_liters_value()
    co2_model_1.has_fuel_consumptions_liters_value = [fuel_consumptions_liters_value_1]

    fuel_consumptions_liters_value_1.has_value = 5
    fuel_consumptions_liters_value_1.has_time = 5

    my_ontology_handler = ontology_handler()
    my_ontology_handler.ontology_builder(myList)

    # Now, we don't want to save it into a file
    onto.save(file="ontology/co2mpas.owl", format="rdfxml")
