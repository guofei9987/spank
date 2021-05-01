import pandas as pd

from examples.datasets import data_generator
import numpy as np
import spank
from spank import functions as F

# %%

sdf = data_generator(num_sample=5)

sdf.head()

# %%
sdf.select_expr('name as name1', '*', 'type as style_type',
                sdf.feature1 + 1,
                F.value(np.sin(sdf.feature2)).alias("feature4"),
                F.value(1))


# %%
sdf.filter_expr((sdf.sex == 'female') & (sdf.feature2 > 0.1))

# %%

sdf
