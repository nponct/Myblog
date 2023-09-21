from .forms import SearchForm

def add_default_data(request):
    search_form=SearchForm()
    return {'search_form':search_form}