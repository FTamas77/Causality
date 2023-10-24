Conver non-binary data to binary:

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

Print the correlation line:

```
    def print_scatter_plot_with_correlation_line():
        scatter_plot_with_correlation_line(
            df['teljesítmény'], df["CO2 kibocsátás gkm V7"])
            ```