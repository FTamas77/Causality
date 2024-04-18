
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
