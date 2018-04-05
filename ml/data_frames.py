import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print("Messing with pandas data frams.")

dates = pd.date_range('20130101', periods=6)
print("""
# (Interpretation of docs):
# * Two dimensional data array.
# * index = row labels
# * columns = column labels
# * data = contents of the 2d array, can be of mixed types.
""")
df = pd.DataFrame(
    data=np.random.randn(6, 4),  # grid of data with coords as (row, col)
    index=dates,
    columns=list('ABCD')
)
print(df)

print("""
What happens if we don't declare index and columns?
We get integer coordinates by default.
""")
df = pd.DataFrame(
    data=np.random.randn(6, 4),  # grid of data with coords as (row, col)
    # index=dates,
    # columns=list('ABCD')
)
print(df)

print("""
Taking a dictionary of data and applying pandas DataFrame interpretation of data.
""")
df = pd.DataFrame({
    # Float value that will be considered a constant in _all_ rows of data.
    'A': 1.,
    # Timestamp data that will be considered a constant in _all_ rows of data.
    'B': pd.Timestamp('20130102'),
    # A series of data that will set the range of data to 4.
    'C': pd.Series(1, index=list(range(4)), dtype='float32'),
    # Additional unique data among the 4 rows.
    'D': np.array([3] * 4, dtype='int32'),
    # Explicit data added to the 4 rows.
    'E': pd.Categorical(["test", "train", "test", "train"]),
    # Another constant added to the 4 rows of data.
    'F': 'foo',
    # What happens if we add a simple array of 5 items.
    # We will get a value error that, due to the assertion above of 4 rows of
    # data, all additional data will need to be 4 rows, or be a constant.
    # 'G': [1, 2, 3, 4, 5]
})
print(df)
