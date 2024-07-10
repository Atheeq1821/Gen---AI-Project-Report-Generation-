from django.shortcuts import render
from django.http import HttpResponse
from .llm import Prompts
from .llm import generate_abstract
from .llm import create_title
from .report import Report
from .logger import logging

def get_data_from_form(request):
    if request.method == "POST":
        domain = request.POST.get("domain")
        objectives = request.POST.get("objectives")
        logging.info(f"Received data from user with domain is {domain} and objectives are {objectives}")
        #Debugging
        abstract="""
        Abstract:
            In this final year project, we aimed to develop an accurate tomato disease classification system using deep learning techniques. Our approach involved training a convolutional neural network (CNN) on a large dataset of labeled images of tomato fruits and vegetables, each with a different disease. By leveraging the power of deep learning, we achieved a remarkable 100% accuracy in classifying tomato diseases, significantly outperforming traditional machine learning methods. Our CNN model consisted of multiple convolutional layers, followed by pooling layers and a fully connected layer for classification. We evaluated the performance of our model using various evaluation metrics such as precision, recall, and F1-score, and observed that it consistently outperformed existing methods in terms of accuracy. The results of this project demonstrate the potential of deep learning techniques in solving complex problems in agriculture, such as tomato disease classification, with high accuracy and efficiency.
        """
        pr = Prompts(domain="Deep Learning",objectives="Tomato disease classification,100% accuracy",abstract=abstract)
        intro = pr.generate_methodology()
        logging.info(f"{intro}")






        #########################################################
        abstract = access_model_abstract(domain, objectives)
        logging.info("Abtract generation completed")

        project_title = create_title(abstract=abstract)
        logging.info(f" Generated Project title is {project_title}")
        downloadable=generate_report(domain=domain, objectives=objectives,abstract=abstract,title=project_title)
        logging.info("Report generation completed")
        response = HttpResponse(downloadable.getvalue(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=generated_project.docx'
        logging.info("Download started...")
        return response
    logging.info("The Start")  
    return render(request,"home.html")


def access_model_abstract(domain, objectives):
    logging.info("Abstract generation started")
    abstract_content = generate_abstract(domain=domain, objectives=objectives)
    return abstract_content
def generate_report(domain,objectives,abstract,title): 
    prompts = Prompts(domain=domain, objectives=objectives,abstract=abstract)
    logging.info("Report generation started")

    report = Report()
    report.add_title_page(title=title)
    logging.info("First page completed")
    report.add_content(heading="Abstract",content=abstract)
    logging.info("abstract content added")

    intro_content = prompts.generate_intro()
    logging.info("Introduction content completed")

    report.add_content(heading="Introduction",content=intro_content)
    logging.info("Introduction content added")

    literature_content = prompts.generate_literature()
    logging.info("Literature content completed")

    report.add_content(heading="Literature",content=literature_content)
    logging.info("Literature content added")

    methodology_content = prompts.generate_methodology()
    logging.info("Methodology content completed")

    report.add_content(heading="Methodology",content=methodology_content)
    logging.info("Methodology content added")

    implement_content = prompts.generate_implementation()
    logging.info("Implementation content completed")

    report.add_content(heading="Implementations",content=implement_content)
    logging.info("Implementations content added")

    result_content = prompts.generate_result()
    logging.info("Result content completed")

    report.add_content(heading="Results",content=result_content)
    logging.info("Results content added")

    discussion_content = prompts.generate_discussion()
    logging.info("Discussion content completed")

    report.add_content(heading="Discussion",content=discussion_content)
    logging.info("Discussion content added")

    conclusion_content = prompts.generate_conclusion()
    logging.info("Conclusion content completed")

    report.add_content(heading="Conclusion",content=conclusion_content)
    logging.info("Conclusion content added")

    references_content = prompts.generate_references()
    logging.info("References content completed")

    report.add_content(heading="References",content=references_content)
    logging.info("References content added")

    appendix_content = prompts.generate_appendices()
    logging.info("Appendix content completed")

    report.add_content(heading="Appendix",content=appendix_content)
    logging.info("Appendix content added")

    document = report.return_doc()
    logging.info("Document generation completed")

    bytes_file = report.convert_bytes()
    logging.info("Bytes file loaded")
    return bytes_file


    
    

