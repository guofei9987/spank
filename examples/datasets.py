# import pandas as pd
import numpy as np
import spank as pd


def name_generator(num_sample):
    names = list()
    for i in range(num_sample):
        length = np.random.randint(5, 15)
        res = ''.join([chr(i) for i in np.random.randint(97, 123, size=length)])
        names.append(res)
    return names


def data_generator(num_sample=100000):
    pdf = pd.DataFrame(columns=['name', 'sex', 'age', 'type', 'feature1', 'feature2'])

    pdf.name = name_generator(num_sample)
    pdf.sex = [('male', 'female')[np.random.randint(0, 2)] for i in range(num_sample)]
    pdf.age = np.random.randint(1, 100, size=num_sample)
    pdf.type = [('type-A', 'type-B', 'type-C', 'type-D')[np.random.randint(0, 4)] for i in range(num_sample)]
    pdf.feature1 = np.random.random(size=num_sample)
    pdf.feature2 = np.random.random(size=num_sample)
    return pdf
