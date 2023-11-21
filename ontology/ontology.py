from owlready2 import *
import os

# configuration
owlready2.JAVA_EXE = "C:\\Program Files\\Java\\jre1.8.0_351\\bin\\java.exe"
onto_path.append(".")

onto = get_ontology("ontology/co2mpas.owl")
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

    class has_value(fuel_consumptions_liters_value >> float, FunctionalProperty):
        pass

    class has_time(fuel_consumptions_liters_value >> float, FunctionalProperty):
        pass

    # actual value 2
    class co2_emissions(co2_model):
        pass

    class has_value(co2_emissions >> float, FunctionalProperty):
        pass

    class has_time(co2_emissions >> float, FunctionalProperty):
        pass

    ###################
    ##### model 2 #####
    ###################
    class engine_model(PhysicalModel):
        pass

    # actual value 1
    class active_cylinders(engine_model):
        pass

    class has_value(active_cylinders >> float, FunctionalProperty):
        pass

    class has_time(active_cylinders >> float, FunctionalProperty):
        pass

    # actual value 2
    class engine_powers_out(engine_model):
        pass

    class has_value(engine_powers_out >> float, FunctionalProperty):
        pass

    class has_time(engine_powers_out >> float, FunctionalProperty):
        pass

    # actual value 3
    class engine_temperature_derivatives(engine_model):
        pass

    class has_value(engine_temperature_derivatives >> float, FunctionalProperty):
        pass

    class has_time(engine_temperature_derivatives >> float, FunctionalProperty):
        pass

    ###################
    ##### model 3 #####
    ###################
    class electric_model(PhysicalModel):
        pass

    # actual value 1
    class motor_p1_maximum_powers(electric_model):
        pass

    class has_value(motor_p1_maximum_powers >> float, FunctionalProperty):
        pass

    class has_time(motor_p1_maximum_powers >> float, FunctionalProperty):
        pass

    # actual value 2
    class motor_p0_speeds(electric_model):
        pass

    class has_value(motor_p0_speeds >> float, FunctionalProperty):
        pass

    class has_time(motor_p0_speeds >> float, FunctionalProperty):
        pass

    ###################
    ##### model 4 #####
    ###################
    class control_model(PhysicalModel):
        pass

    # actual value 1
    class engine_temperatures(control_model):
        pass

    class has_value(engine_temperatures >> float, FunctionalProperty):
        pass

    class has_time(engine_temperatures >> float, FunctionalProperty):
        pass

    ###################
    ##### model 5 #####
    ###################
    class wheel_model(PhysicalModel):
        pass

    # actual value 1
    class wheel_speeds(wheel_model):
        pass

    class has_value(wheel_speeds >> float, FunctionalProperty):
        pass

    class has_time(wheel_speeds >> float, FunctionalProperty):
        pass

    # actual value 1
    class velocities(wheel_model):
        pass

    class has_value(velocities >> float, FunctionalProperty):
        pass

    class has_time(velocities >> float, FunctionalProperty):
        pass


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
            "Fuel_consumptions_liters_value" "Co2_emissions",
            "Active_cylinders",
            "Engine_powers_out",
            "Motor_p1_maximum_powers",
            "Engine_temperature_derivatives",
            "Motor_p0_speeds",
            "Engine_temperatures",
            "Wheel_speeds",
            "Velocities",
        ]
    )

    my_ontology_handler = ontology_handler()
    my_ontology_handler.ontology_builder(myList)

    # Now, we don't want to save it into a file
    onto.save(file="ontology/co2mpas.owl", format="rdfxml")
