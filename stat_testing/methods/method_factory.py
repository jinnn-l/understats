from .method_classes import *

class StatisticalMethodFactory:
    #corresponds to choices.py
    test_types = {
        '1T-TEST': OneSampleTTest,
    }

@staticmethod
def create_test(test_type, df):
    test_class = StatisticalMethodFactory.test_types.get(test_type)
    if test_class is None:
        raise ValueError(f'Invalid test type: {test_type}')
    return test_class(df)