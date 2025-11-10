from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
import pandas as pd

from .forms import *
from .methods import method_factory
  
class UploadFileView(TemplateView):
    template_name = 'upload.html'

    def get(self, request):
        upload_form = UploadFileForm()
        return render(request, 'upload.html', {'form': upload_form})
    
    def post(self, request):
        upload_form = UploadFileForm(request.POST, request.FILES)

        if upload_form.is_valid():
            test = request.POST['test']
            file = request.FILES['file']
            try:
                df = pd.read_csv(file, header = None)
                #store uploaded input in django sessions
                request.session['dataframe'] = df.to_json(orient = 'records', lines = True)
                request.session['test_type'] = test
                #redirect to RequestAttributeView
                return HttpResponseRedirect('details/')
            except:
                raise TypeError('Wrong file type')

class RequestAttributeView(FormView):
    template_name = 'details.html'

    #use method_factory to generate appropriate form based on input
    @staticmethod
    def generate_form(test_type, df):
        test_class = method_factory.create_test(test_type, df)
        attribute_tuple = test_class.request_attributes()
        form = GetAttributesForm(attributes = attribute_tuple)
        return form

    def get(self, request, *args , **kwargs):
        #retrieve information stored in django sessions
        test_type = request.session['test_type']
        df_json = request.session['dataframe']
        df = pd.read_json(df_json, lines = True)
        df_html = df.to_html(index = False, border = 0)
        form = self.generate_form(test_type, df)
        return render(request, self.template_name, {'form': form, 'df_html': df_html, 'test_type': test_type})
    
    def post(self, request, *args, **kwargs):
        required_attributes = request.POST
        df = pd.read_html(required_attributes['df_html'])[0]
        test_type = required_attributes['test_type']
        test_class = method_factory.create_test(test_type, df)
        #call each statistical test's run_test method to produce results
        results = test_class.run_test(df, required_attributes)
        #store results in django sessions
        request.session['results'] = results
        #redirect to DisplayResultsView
        return HttpResponseRedirect('/stat_testing/results/')
    
class DisplayResultsView(TemplateView):
    template_name = 'results.html'

    def get(self, request):
        results = request.session['results']
        return render(request, self.template_name, 
                      {'table': results['table'], 
                       'str_output': results['str_output'],
                       'plot': results['plot']})