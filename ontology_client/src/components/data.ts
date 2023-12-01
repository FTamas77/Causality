export const hues = [200, 320, 80, 160, 0, 240, 120, 280, 40];

export const size = {
  default: 1,
  hover: 8
};

import { reactive } from "vue";
export const nodes = reactive({});
export const edges = reactive({});

/*
1: { name: "wheel_speeds", edgeWidth: 1, hue: 200 },
2: { name: "velocities", edgeWidth: 1, hue: 160 },
3: { name: "engine_temperatures", edgeWidth: 1, hue: 320 },
4: { name: "motor_p0_speeds", edgeWidth: 1, hue: 160 },
5: { name: "motor_p1_maximum_powers", edgeWidth: 1, hue: 80 },
6: { name: "engine_temperature_derivatives", edgeWidth: 1, hue: 160 },
7: { name: "engine_powers_out", edgeWidth: 1, hue: 160 },
8: { name: "active_cylinders", edgeWidth: 1, hue: 160 },
9: { name: "co2_emissions", edgeWidth: 1, hue: 160 },
10: { name: "fuel_consumptions_liters_value", edgeWidth: 1, hue: 160 }
*/

/*
{ source: "1", target: "2", edgeWidth: 1, hue: 200 },
{ source: "1", target: "3", edgeWidth: 1, hue: 200 },

{ source: "2", target: "8", edgeWidth: 1, hue: 80 },

{ source: "3", target: "4", edgeWidth: 1, hue: 320 },
{ source: "3", target: "5", edgeWidth: 1, hue: 320 },
{ source: "3", target: "7", edgeWidth: 1, hue: 320 },

{ source: "2", target: "6", edgeWidth: 1, hue: 160 },
{ source: "4", target: "7", edgeWidth: 1, hue: 160 },
{ source: "4", target: "2", edgeWidth: 1, hue: 160 },

{ source: "5", target: "6", edgeWidth: 1, hue: 80 },
{ source: "5", target: "7", edgeWidth: 1, hue: 80 },
{ source: "8", target: "7", edgeWidth: 1, hue: 80 }
*/