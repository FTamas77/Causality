# Start

https://co2mpas.readthedocs.io/en/stable/quick.html

co2mpas run ./input/co2mpas_conventional.xlsx -O ./output -PL

# Notes:

The identified/calibrated parameters from WLTP data (i.e., data.prediction.models_<cycle>) can be grouped by functionality in eight macro-models:

**A/T:** gear shifting strategy for automatic transmission,
**electrics:** vehicle electric components ( i.e., alternator, service battery, drive battery, and DC/DC converter),
**clutch-torque-converter:** speed model for clutch or torque converter,
**co2_params:** extended willans lines parameters,
**after-treatment:** warm up strategy of after treatment,
**engine-coolant-temperature:** warm up and cooling models of the engine,
**engine-speed:** correlation from velocity to engine speed,
**control:** start/stop strategy or ECMS.

**Furthermore:**

The Electric Power System (EPS) of HEVs is composed by three main components:

* Electric machines (P0, P1, P2, P2_pla, P3f, P3r, P4f, and P4r),
* Batteries (Drive and Service, i.e. high and low voltage batteries), and
* DC/DC converter
