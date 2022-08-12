import pandas as pd

data = pd.read_csv("people.csv")

data.sort_values("Name", inplace=True)

data.drop_duplicates(subset="Name",
                     keep="first", inplace=True)

data.to_csv('people_.csv', index=False)
