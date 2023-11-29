from owlready2 import *
import os

# configuration
owlready2.JAVA_EXE = "C:\\Program Files\\Java\\jre1.8.0_351\\bin\\java.exe"
onto_path.append(".")

# https://stackoverflow.com/questions/66965475/creating-an-instance-in-owlready2-creates-a-completely-new-class-instead-of-asig
# IRI must be formatted as a link - even if it's a fake one. For example, if IRI is "http://test.org/new.owl", my code works perfectly.
onto = get_ontology("http://test.org/new.owl")
# onto = get_ontology("ontology/co2mpas.owl").load()

# default parameters, now the web uses it
selected_parameters = [
    {"name": "wheel_speeds", "active": True},
    {"name": "velocities", "active": True},
    {"name": "engine_temperatures", "active": True},
    {"name": "motor_p0_speeds", "active": True},
    {"name": "motor_p1_maximum_powers", "active": True},
    {"name": "engine_temperature_derivatives", "active": True},
    {"name": "engine_powers_out", "active": True},
    {"name": "active_cylinders", "active": True},
    {"name": "co2_emissions", "active": True},
    {"name": "fuel_consumptions_liters_value", "active": True},
]

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

    class PhysicalParameter(Thing):
        pass

    ###################
    ##### model 1 #####
    ###################

    class co2_model(PhysicalModel):
        pass

    # actual value 1
    class fuel_consumptions_liters_value(PhysicalParameter):
        pass

    # connect the model and the lowes parameter: co2_model >> fuel_consumptions_liters_value
    class has_fuel_consumptions_liters_value(
        co2_model >> fuel_consumptions_liters_value, ObjectProperty
    ):
        pass

    # actual value 2
    class co2_emissions(PhysicalParameter):
        pass

    # connect the model and the lowes parameter: co2_model >> co2_emissions
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
    class active_cylinders(PhysicalParameter):
        pass

    #  connect the model and the lowes parameter: engine_model >> active_cylinders
    class has_active_cylinders(engine_model >> active_cylinders, ObjectProperty):
        pass

    # actual value 2
    class engine_powers_out(PhysicalParameter):
        pass

    #  connect the model and the lowes parameter: engine_model >> engine_powers_out
    class has_engine_powers_out(engine_model >> engine_powers_out, ObjectProperty):
        pass

    # actual value 3
    class engine_temperature_derivatives(PhysicalParameter):
        pass

    # connect the model and the lowes parameter: engine_model >> engine_temperature_derivatives
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
    class motor_p1_maximum_powers(PhysicalParameter):
        pass

    class has_engine_temperature_derivatives(
        electric_model >> motor_p1_maximum_powers, ObjectProperty
    ):
        pass

    # actual value 2
    class motor_p0_speeds(PhysicalParameter):
        pass

    class has_motor_p0_speeds(electric_model >> motor_p0_speeds, ObjectProperty):
        pass

    ###################
    ##### model 4 #####
    ###################

    class control_model(PhysicalModel):
        pass

    # actual value 1
    class engine_temperatures(PhysicalParameter):
        pass

    class has_engine_temperatures(control_model >> engine_temperatures, ObjectProperty):
        pass

    ###################
    ##### model 5 #####
    ###################

    class wheel_model(PhysicalModel):
        pass

    # actual value 1
    class wheel_speeds(PhysicalParameter):
        pass

    class has_wheel_speeds(wheel_model >> wheel_speeds, ObjectProperty):
        pass

    # actual value 2
    class velocities(PhysicalParameter):
        pass

    class has_velocities(wheel_model >> velocities, ObjectProperty):
        pass

    ############################
    ##### model parameters #####
    ############################

    # https://stackoverflow.com/questions/70061671/how-to-define-multiple-domains-in-owlready2
    # https://stackoverflow.com/questions/77529594/owlready2-create-functionalproperty-to-multiple-classes
    # the superclass is PhysicalParameter
    class has_value(DataProperty):
        domain = [
            Or(
                [
                    wheel_speeds,
                    velocities,
                    engine_temperatures,
                    motor_p0_speeds,
                    motor_p1_maximum_powers,
                    engine_temperature_derivatives,
                    engine_powers_out,
                    active_cylinders,
                    co2_emissions,
                    fuel_consumptions_liters_value,
                ]
            )
        ]
        range = [float]

    class has_time(DataProperty):
        domain = [
            Or(
                [
                    wheel_speeds,
                    velocities,
                    engine_temperatures,
                    motor_p0_speeds,
                    motor_p1_maximum_powers,
                    engine_temperature_derivatives,
                    engine_powers_out,
                    active_cylinders,
                    co2_emissions,
                    fuel_consumptions_liters_value,
                ]
            )
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

    # measurements, add dataproperties as parameters
    fuel_consumptions_liters_value(has_value=[5], has_time=[6])
    fuel_consumptions_liters_value(has_value=[7], has_time=[8])
    fuel_consumptions_liters_value(has_value=[9], has_time=[10])
    fuel_consumptions_liters_value(has_value=[11], has_time=[12])

    print("print the instances of the class:\n")
    for i in fuel_consumptions_liters_value.instances():
        print(i)

    # Now, we don't want to save it into a file
    # onto.save(file="ontology/co2mpas.owl", format="rdfxml")

    ###############################
    # Sample queries using SPARQL #
    ###############################

    ret = list(
        default_world.sparql(
            """
                            SELECT ?prop_value
                            WHERE {   
                                ?inst a new:fuel_consumptions_liters_value .
                                ?inst new:has_value ?prop_value .
                            }
                
            """
        )
    )

    for triple in ret:
        print(triple)
