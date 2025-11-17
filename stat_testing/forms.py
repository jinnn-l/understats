from django import forms
from .choices import *

class UploadFileForm(forms.Form):
    #show list of supported statistical analysis methods
    test = forms.ChoiceField(choices = STATISTICAL_TESTS_CHOICES)
    #allow file upload
    file = forms.FileField(label = 'File Upload')

#unpack attributes needed by each statistical test to generate form fields
class GetAttributesForm(forms.Form):
    def __init__(self, attributes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        discrete_attributes, continuous_attributes, form_order = attributes[0], attributes[1], attributes[2]
        for i in form_order:
            if i[0] == 0:
                attribute = discrete_attributes[i[1]]
                self.fields[attribute[0]] = create_discrete_form_field(attribute)
            else:
                attribute = continuous_attributes[i[1]]
                self.fields[attribute[0]] = create_continuous_form_field(attribute)

#unpack list of provided choices into form fields
@staticmethod
def create_discrete_form_field(attribute):
    choices = ()
    for choice in attribute[2]:
        choices += ((choice, choice),)
    return forms.ChoiceField(label = attribute[1], choices = choices)

@staticmethod
def create_continuous_form_field(attribute):
    #if the attribute is of integer type
    if attribute[2] == int:
        #if the minimum, maximum, step size, or initial value is not specified
        if len(attribute) == 3:
            return forms.IntegerField(label = attribute[1])
        else: 
            return forms.IntegerField(label = attribute[1], 
                                    min_value = attribute[3].get('min_value'),
                                    max_value = attribute[3].get('max_value'),
                                    step_size = attribute[3].get('step_size'),
                                    initial = attribute[3].get('initial'))
    #if the attribute is of float type
    elif attribute[2] == float:
        if len(attribute) == 3:
            #if the minimum, maximum, step size, or initial value is not specified
            return forms.FloatField(label = attribute[1])
        else: 
            return forms.FloatField(label = attribute[1], 
                                    min_value = attribute[3].get('min_value'),
                                    max_value = attribute[3].get('max_value'),
                                    step_size = attribute[3].get('step_size'),
                                    initial = attribute[3].get('initial'))
    else:
        raise TypeError('Unsupported attribute type')

        
