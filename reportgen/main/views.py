from django.shortcuts import render
from django.http import HttpResponse

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import os

def get_data_from_form(request):
    if request.method == "POST":
        domain = request.POST.get("domain")
        objectives = request.POST.get("objectives")
        
        return HttpResponse("Form submitted successfully!")
    
    return render(request,"home.html")

