# Table of Contents

- [Table of Contents](#table-of-contents)
  - [Classes](#classes)
    - [Singleton classes](#singleton-classes)
    - [Main classes](#main-classes)
    - [Main business logic](#main-business-logic)
    - [Main causality logics](#main-causality-logics)
  - [Conver non-binary data to binary for causal discovery:](#conver-non-binary-data-to-binary-for-causal-discovery)
  - [Print the correlation line in case of causal inference:](#print-the-correlation-line-in-case-of-causal-inference)

## Classes

[Tutorial](https://mermaid.js.org/syntax/classDiagram.html)

### Singleton classes

These are frequently used, therefore singletons.
**TODO:** logger::print_log is static, because the class constructor needs some special parameter.

```mermaid
classDiagram
      class confiurator{
            +get_causal_discovery_keep_cols_labels()
            +get_causal_inference_keep_cols()
            +get_applied_input_files()
            +get_CONFIG_FILE()
            +get_ROOT_DIR()
            +get_INPUT_DATA_DIR()
      }
      class logger{
            +print_log()
      }
```

### Main classes

**gui**

* created in the main and holds the gui objects
* creates the logger, because logger needs the gui and the text box on it

```mermaid
classDiagram
      class gui{
            +build_gui()
            +start_gui()
      }
```

### Main business logic

**causal_algs**

* has no data
* the gui calls it
* responsible for reading the data by data_reader
* responsible to pass the input data to the causal algoritms

**data_reader**

* it is now a simple static method
* does not store any data
* removes the not used columns, keeps only the needed ones
* return a pandas framework

```mermaid
classDiagram
      causal_algs --> Causal_discovery
      causal_algs --> Causal_inference
      causal_algs --> data_reader
      class Causal_discovery
      class Causal_inference
      class causal_algs{
            +causal_inference()
            +causal_discovery()
      }
      class data_reader{
            +read_input_data(keep_cols, list_of_files)
      }
```

### Main causality logics

**Causal_discovery**

* has no data
* the gui calls it
* responsible for reading the data by data_reader
* responsible to pass the input data to the causal algoritms

**Causal_inference**

* it is now a simple static method
* does not store any data
* removes the not used columns, keeps only the needed ones
* return a pandas framework

```mermaid
classDiagram
      class Causal_discovery{
            +create_model()
            +identify_effect()
            +estimate_effect()
            +refute()
      }
      class Causal_inference{
            +calculate_pc()
            +calculate_fci()
            +calculate_ges()
      }
```

---

## Conver non-binary data to binary for causal discovery:

```
# Convert to binary format a non-binary data
# (Actually patternDel will be kept and not deleted)
patternDel = "Diesel|Otto"
filter = df['motor működési mód'].str.contains(patternDel) == False
df = df[~filter]

df['motor működési mód'].replace("Diesel", 0, inplace=True)
df['motor működési mód'].replace("Otto", 1, inplace=True)

print("\nSize of the input data: " +
      str(df.shape[0]) + "x" + str(df.shape[1]) + "\n\nAnd the input data:\n")
print(df)
```

## Print the correlation line in case of causal inference:

```
scatter_plot_with_correlation_line(df['teljesítmény'], df["CO2 kibocsátás gkm V7"])
```
