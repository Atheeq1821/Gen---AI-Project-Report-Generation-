from django.shortcuts import render
from django.http import HttpResponse

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import os
from .logger import logging


LANGCHAIN_API_KEY="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"
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_API_KEY']=LANGCHAIN_API_KEY

llm = Ollama(model="llama2")
output_parser=StrOutputParser()

def generate_abstract(domain,objectives):
    abstract_prompt=ChatPromptTemplate.from_messages(
        [
            ("system","You are an expert engineering consultant tasked with creating an abstract of a complete final year project report. Use the following information to generate a comprehensive project implementation and IEEE-formatted report abstract"),
            ("user",f"""Domain is {domain} and the objectives are {objectives} 
            Generate only abstract paragraph of 200 to 300 words for the complete engineering final year project and report. Must contain description of chosen algorithm or approach all the content should be in single paragraph and Dont add title I want only abstract paragraph""")

        ]
    )
    chain=abstract_prompt|llm|output_parser
    abstract = chain.invoke({"domain":domain,"objectives":objectives})
    logging.info("Abstract content returning")
    logging.info(f"{abstract}")
    return abstract

def create_title(abstract):
        logging.info("Creating title from abstract")
        title_prompt=ChatPromptTemplate.from_messages(
            [
                ("system","You are an expert engineering consultant tasked with creating a complete final year project and report. Use the following information to generate a best project title and IEEE-formatted report:"),
                ("user",f"""Abstract of the project: 
                 {abstract}
                Generate only title of the project for the complete engineering final year project and report. Must be in single line and creative""")
            ])
        chain=title_prompt|llm|output_parser
        logging.info("Title content returning")
        return chain.invoke({"abstract":abstract})

class Prompts:
    def __init__(self,domain,objectives,abstract):
        self.domain=domain
        self.objectives=objectives
        self.abstract=abstract

    def generate_intro(self):
        intro_prompt=ChatPromptTemplate.from_messages(
            [
                ("system","You are an expert engineering consultant tasked with creating a complete final year project and report. Use the following information to generate only the introduction content for the project report"),
                ("user",f"""Below is the abstract of the project :
                {self.abstract}
                Based on this abstract, write the Introduction section of the report. Include the following subsections:
                3. Introduction
                    - Background
                    - Problem Statement
                    - Project Objectives
                    - Scope of the Project
                Focus only on these subsections. Do not include a title, abstract, or any other sections. Use appropriate technical terminology and ensure the content is coherent and implementable. 

Begin your response with content of the Introduction section and then proceed with the subsections.
                """)

            ]
        )  
        chain=intro_prompt|llm|output_parser
        logging.info("introduction content returning")
        return chain.invoke({"domain":self.domain,"objectives":self.objectives,"abstract":self.abstract})
    
    def generate_literature(self):
        literature_prompt=ChatPromptTemplate.from_messages(
            [
                ("system","You are an expert engineering consultant tasked with creating a complete final year project and report. Use the following information to generate only the literature content for the project report"),
               ("user",f"""
                Below is the abstract of the project :
                {self.abstract}
                Based on this abstract, write the Literature section of the report. Include the following subsections:
                4. Literature Review
                    - Overview of relevant technologies and methodologies
                    - Analysis of similar existing solutions
                    - Identification of research gaps
                Focus only on these subsections. Do not include a title, abstract, or any other sections. Use appropriate technical terminology and ensure the content is coherent and implementable. 

Begin your response with 'Content of the literature section' and then proceed with the subsections.
                    
                """)

            ]
        )  
        chain=literature_prompt|llm|output_parser
        logging.info("literature content returning")
        return chain.invoke({"domain":self.domain,"objectives":self.objectives,"abstract":self.abstract})
    
    def generate_methodology(self):
        methodology_prompt=ChatPromptTemplate.from_messages(
            [
                ("system","You are an expert in deep learning and computer vision. Below is the abstract for a final year engineering project on tomato disease classification. Using this information, write the Methodology section for the project report"),
                 ("user",f"""
                Below is the abstract of the project :
                {self.abstract}
                Generate only the following content for the complete engineering final year project report using above informations:
                Based on this abstract, write the Methodology section of the report. Include the following subsections:
                    - Detailed description of the chosen algorithm or approach (must)
                    - Justification for the chosen method
                    - System architecture
                    - Data collection and preprocessing (if applicable)
                
                Focus only on these subsections. Do not include a title, abstract, or any other sections. Use appropriate technical terminology and ensure the content is coherent and implementable. 

                Begin your response with content of the methodology section and then proceed with the subsections.
                """)

            ]
        )  
        chain=methodology_prompt|llm|output_parser
        logging.info("Methodology content returning")
        return chain.invoke({"domain":self.domain,"objectives":self.objectives,"abstract":self.abstract})
    
    def generate_implementation(self):
        implement_prompt=ChatPromptTemplate.from_messages(
            [
                ("system","You are an expert engineering consultant tasked with creating a complete final year project and report. Use the following information to generate only the implementation content for the project report"),
                ("user",f"""
                Below is the abstract of the project :
                {self.abstract}
                Based on this abstract, write the Implementation section of the report. Include the following subsections:
                6. Implementation
                    - Detailed explanation of the implementation process
                    - Key components of the system
                    - Pseudo-code or high-level code snippets for critical parts
                    - Challenges faced and how they were overcome
                Focus only on these subsections. Do not include a title, abstract, or any other sections. Use appropriate technical terminology and ensure the content is coherent and implementable. 

Begin your response with the content of the implementation section and then proceed with the subsections.              
                """)

            ]
        )  
        chain=implement_prompt|llm|output_parser
        logging.info("Implementation content returning")
        return chain.invoke({"domain":self.domain,"objectives":self.objectives,"abstract":self.abstract})
    
    def generate_result(self):
        result_prompt=ChatPromptTemplate.from_messages(
            [
                ("system","You are an expert engineering consultant tasked with creating a complete final year project and report. Use the following information to generate only the result content for the project report"),
                   ("user",f"""
                Below is the abstract of the project :
                {self.abstract}
                Based on this abstract, write the Result section of the report. Include the following subsections:
                  7. Results and Analysis
                    - Performance metrics
                    - Evaluation of the system against project objectives
                    - Comparative analysis with existing solutions (if applicable)
                
                    
                Focus only on these subsections. Do not include a title, abstract, or any other sections. Use appropriate technical terminology and ensure the content is coherent and implementable. 

Begin your response with the content of the result section and then proceed with the subsections.
                """)

            ]
        )  
        chain=result_prompt|llm|output_parser
        logging.info("Result content returning")
        return chain.invoke({"domain":self.domain,"objectives":self.objectives,"abstract":self.abstract})
    
    def generate_discussion(self):
        discussion_prompt=ChatPromptTemplate.from_messages(
            [
                ("system","You are an expert engineering consultant tasked with creating a complete final year project and report. Use the following information to generate only the discussion content for the project report"),
                      ("user",f"""
                Below is the abstract of the project :
                {self.abstract}
                Based on this abstract, write the Discussion section of the report. Include the following subsections:
                  8. Discussion
                    - Interpretation of results
                    - Limitations of the current implementation
                    - Potential improvements and future work
                Focus only on these subsections. Do not include a title, abstract, or any other sections. Use appropriate technical terminology and ensure the content is coherent and implementable. 

Begin your response with the content of the discussion section  and then proceed with the subsections.
                """)

            ]
        )  
        chain=discussion_prompt|llm|output_parser
        logging.info("discussion content returning")
        return chain.invoke({"domain":self.domain,"objectives":self.objectives,"abstract":self.abstract})
    
    def generate_conclusion(self):
        conclusion_prompt=ChatPromptTemplate.from_messages(
            [
                ("system","You are an expert engineering consultant tasked with creating a complete final year project and report. Use the following information to generate only the conclusion content for the project report"),
                      ("user",f"""
                Below is the abstract of the project :
                {self.abstract}
                Based on this abstract, write the conclusion section of the report. Include the following subsections:
                9. Conclusion
                    - Summary of achievements
                    - Reflection on the project objectives
                    - Impact and significance of the project
                Focus only on these subsections. Do not include a title, abstract, or any other sections. Use appropriate technical terminology and ensure the content is coherent and implementable. 

Begin your response with the content of the conclusion section and then proceed with the subsections.
                """)

            ]
        )  
        chain=conclusion_prompt|llm|output_parser
        logging.info("Conclusion content returning")
        return chain.invoke({"domain":self.domain,"objectives":self.objectives,"abstract":self.abstract})
    
    def generate_references(self):
        ref_prompt=ChatPromptTemplate.from_messages(
            [
                ("system","You are an expert engineering consultant tasked with creating a complete final year project and report. Use the following information to generate only the references content for the project report"),
               ("user",f"""
                Below is the abstract of the project :
                {self.abstract}
                Based on this abstract, write the references section of the report:
                10. References (in IEEE format)
                Focus only on this section. Do not include a title, abstract, or any other sections. Use appropriate technical terminology and ensure the content is coherent and implementable. 

Begin your response with the content of the references section and then proceed.
                """)

            ]
        )  
        chain=ref_prompt|llm|output_parser
        logging.info("reference content returning")
        return chain.invoke({"domain":self.domain,"objectives":self.objectives,"abstract":self.abstract})
    
    def generate_appendices(self):
        appendix_prompt=ChatPromptTemplate.from_messages(
            [
                ("system","You are an expert engineering consultant tasked with creating a complete final year project and report. Use the following information to generate only the appendices content for the project report"),
                   ("user",f"""
                Below is the abstract of the project :
                {self.abstract}
                Based on this abstract, write the Appendics section of the report. Include the following subsections:
                11. Appendices
                    - Detailed technical specifications
                    - Additional data or results
                Focus only on these subsections. Do not include a title, abstract, or any other sections. Use appropriate technical terminology and ensure the content is coherent and implementable. 

Begin your response with the content of the appendices section and then proceed with the subsections.
                """)

            ]
        )  
        chain=appendix_prompt|llm|output_parser
        logging.info("final content returning")
        return chain.invoke({"domain":self.domain,"objectives":self.objectives,"abstract":self.abstract})
    
    
