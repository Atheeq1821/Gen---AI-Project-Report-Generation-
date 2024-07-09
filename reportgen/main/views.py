from django.shortcuts import render
from django.http import HttpResponse
from .llm import Prompts
from .llm import generate_abstract
from .report import Report

def get_data_from_form(request):
    if request.method == "POST":
        domain = request.POST.get("domain")
        objectives = request.POST.get("objectives")

        abstract = access_model_abstract(domain, objectives)
        downloadable=generate_report(domain=domain, objectives=objectives,abstract=abstract)
        response = HttpResponse(downloadable.getvalue(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=generated_project_{domain.replace(" ", "_")}.docx'
        
        return response
    
    return render(request,"home.html")


def access_model_abstract(domain, objectives):
    abstract_content = generate_abstract(domain=domain, objectives=objectives)
    return abstract_content
def generate_report(domain,objectives,abstract):
    prompts = Prompts(domain=domain, objective=objectives,abstract=abstract)
    report = Report()
    report.add_content(heading="Abstract",content=abstract)
    intro_content = prompts.generate_intro()
    report.add_content(heading="Introduction",content=intro_content)
    document = report.return_doc()
    bytes_file = report.convert_bytes()
    return bytes_file


    
    

