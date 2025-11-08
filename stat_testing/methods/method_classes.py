from abc import ABC, abstractmethod
from prettytable import PrettyTable
from scipy.stats import t
import numpy as np

#abstract parent class
class StatisticalMethod(ABC):
    @abstractmethod
    def request_attributes(self) -> tuple:
        '''
        returns attributes needed to run test as a tuple of tuples in the order
        ((discrete attributes that accept input from a set of choices),
         (continuous attributes that accept input from a range of values),
         (indices, order in which attributes are presented to users))

        where each attribute is a inner tuple arranged as follows:
        - discrete attributes
        (attribute variable name <str>, attribute description as seen by users <str>, allowed choices <tuple>)

        - continuous attributes
        (attribute variable name <str>, variable type <type> , optional kwargs for the form field <dict>)

        for a test with 2 discrete attributes and 3 continuous attributes, 
        the last tuple may look something like
        ((0, 0), (0, 1), (1, 0), (1, 1), (1, 2))
        '''
        pass

    @abstractmethod
    def run_test(self, *args, **kwargs) -> dict:
        #run tests and output necessary information
        pass 

    #report p-values greater than 0.001 to 3 decimal places
    def report_p_value(self, value):
        return '< 0.001' if value < 0.001 else round(value, 3)
    
    #str output to be used for html template
    def report_result_string(self, results):
        keys = list(results.keys())
        str_output = ''
        for key in keys:
            if results[key]:
                str_output += f'{key} = {results[key]} <br>'
            else:
                str_output += f'{key} <br>'
        return str_output


#child classes that inherit from parent class
class OneSampleTTest(StatisticalMethod):
    def __init__(self, df):
        self.df = df
        self.nrows = df.shape[0]
        self.ncols = df.shape[1]
        self.col_range = tuple(range(self.ncols))

    def request_attributes(self) -> tuple: 
        attributes = (
            (('test_subtype', 'Type of test', ('left-tailed', 'right-tailed', 'two-tailed')),
             ('var_of_interest', 'Column of interest (first column is column 0)', self.col_range)),
            (('skip_rows', 'Number of header rows to skip', int, {'min_value': 0, 'max_value': self.nrows - 1, 'initial': 1}),
             ('null_hyp', 'Null hypothesis on the mean', float),
             ('conf', 'Confidence interval (as a decimal)', float, {'min_value': 0, 'max_value': 1})),
            ((0, 0), (0, 1), (1, 0), (1, 1), (1, 2))
        )
        return attributes
    
    def run_test(self, df, required_attributes) -> dict:
        #reading user input stored in django sessions
        test_subtype = required_attributes['test_subtype']
        var_of_interest = int(required_attributes['var_of_interest'])
        skip_rows = int(required_attributes['skip_rows'])
        null_hyp = float(required_attributes['null_hyp'])
        conf = float(required_attributes['conf'])

        #performing the statistical test
        df = df.to_numpy()    
        data = df[:,var_of_interest]
        n = len(df)
        sample_mean, sample_sd = np.mean(data), np.std(data, ddof = 1)
        sem = sample_sd / np.sqrt(n)
        t_value = (sample_mean - null_hyp) / (sample_sd / np.sqrt(n))

        if test_subtype == 'left-tailed':
            t_crit = t.ppf(conf, n - 1) 
            p_value = 1 - t.sf(np.abs(t_value), n - 1)
            sign = '<'
        elif test_subtype == 'right-tailed':
            t_crit = t.ppf(conf, n - 1) 
            p_value = t.sf(np.abs(t_value), n - 1)
            sign = '>'
        else:
            t_crit = t.ppf((1 + conf) / 2, n - 1)
            p_value = t.sf(np.abs(t_value), n - 1) * 2
            sign = '≠'
        
        var_name = df[:,var_of_interest][0] if skip_rows else ''
        conf_interval = [sample_mean - t_crit * sem, sample_mean + t_crit * sem]

        results = {
            'H0: μ': null_hyp,
            f'H1: μ {sign} {null_hyp}': '',
            'degrees of freedom': n - 1,
            't_value': t_value,
            'p_value': super().report_p_value(p_value),
        }

        #table to present calculations 
        table = PrettyTable()
        table.field_names = ['var', 'n', 'sample mean', 'sample sd', f'{conf * 100}% conf. interval', '']
        table.add_row([var_name, n, sample_mean, sample_sd, conf_interval[0], conf_interval[1]])

        return {
            'results': results,
            'table': table.get_html_string(),
            'str_output': super().report_result_string(results),
        }