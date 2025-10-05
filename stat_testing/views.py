from django.http import HttpResponseRedirect
from django.shortcuts import render
import pandas as pd

from .forms import UploadFileForm
 
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                try:
                    df = pd.read_csv(file)
                    df_html = [df.to_html(index = False, border = 0)]
                    return render(request, 'upload.html', {'form': form, 'df_html': df_html})
                except:
                    raise Exception('Wrong file type')
            else:
                raise Exception('Wrong file type')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})