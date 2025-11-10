import pandas as pd
from pytest import approx

import constants_test_cases
from stat_testing.methods.method_factory import create_test

class TestOneSampleTTest():
    test_type = '1T-TEST'
    df = pd.read_csv('stat_testing/tests/sample_test_data/onesamplettest_data.csv', header = None)
    test_class = create_test(test_type, df)
    
    def test_left_tailed(self):
        results = self.test_class.run_test(self.df, constants_test_cases.ONE_SAMPLE_T_TEST_LEFT_TAILED)
        assert results['results_for_testing']['t_value'] == approx(constants_test_cases.ONE_SAMPLE_T_TEST_LEFT_TAILED['t_value'])
        assert results['results_for_testing']['p_value'] == constants_test_cases.ONE_SAMPLE_T_TEST_LEFT_TAILED['p_value']

    def test_right_tailed(self):
        results = self.test_class.run_test(self.df, constants_test_cases.ONE_SAMPLE_T_TEST_RIGHT_TAILED)
        assert results['results_for_testing']['t_value'] == approx(constants_test_cases.ONE_SAMPLE_T_TEST_RIGHT_TAILED['t_value'])
        assert results['results_for_testing']['p_value'] == constants_test_cases.ONE_SAMPLE_T_TEST_RIGHT_TAILED['p_value']

    def test_two_tailed(self):
        results = self.test_class.run_test(self.df, constants_test_cases.ONE_SAMPLE_T_TEST_TWO_TAILED)
        assert results['results_for_testing']['t_value'] == approx(constants_test_cases.ONE_SAMPLE_T_TEST_TWO_TAILED['t_value'])
        assert results['results_for_testing']['p_value'] == constants_test_cases.ONE_SAMPLE_T_TEST_TWO_TAILED['p_value']
