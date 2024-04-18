
## Notes:

[Tutorial](https://mermaid.js.org/syntax/classDiagram.html)

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

## Scenario

        graph__ = """graph    [
                                            directed 1    
                                            node [id "hengerűrtartalom" label "hengerűrtartalom"]
                                            node [id "teljesítmény" label "teljesítmény"]
                                            node [id "Elhaladási zaj dBA" label "Elhaladási zaj dBA"]
                                            node [id "CO2 kibocsátás gkm V7" label "CO2 kibocsátás gkm V7"]
                                            node [id "Összevont átlagfogy" label "Összevont átlagfogy"]
                                            node [id "Korr abszorp együttható" label "Korr abszorp együttható"]
                                            node [id "kilométeróra állás" label "kilométeróra állás"]
                                            node [id "gy fogy ért orszúton" label "gy fogy ért orszúton"]
                                            edge [source "hengerűrtartalom" target "teljesítmény"]
                                            edge [source "gy fogy ért orszúton" target "teljesítmény"]
                                            edge [source "teljesítmény" target "Elhaladási zaj dBA"]
                                            edge [source "teljesítmény" target "Összevont átlagfogy"]
                                            edge [source "hengerűrtartalom" target "CO2 kibocsátás gkm V7"]
                                            edge [source "Összevont átlagfogy" target "CO2 kibocsátás gkm V7"]
                                            edge [source "kilométeróra állás" target "CO2 kibocsátás gkm V7"]
                                            edge [source "Korr abszorp együttható" target "CO2 kibocsátás gkm V7"]
                                            edge [source "Elhaladási zaj dBA" target "CO2 kibocsátás gkm V7"]
                            ]"""

