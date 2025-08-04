from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import wikipedia
import re
class Chatbot:
    def __init__(self):
        super().__init__()
        self.model = OllamaLLM(model="llama3.2")
        self.template = self.template = """
Answer naturally and accurately.

Context from conversation: {context}

Relevant info from a web search (if available): {search}, If the results are inefficient, reply based on your current knowledge

User's Question: {question}

Answer as if you researched it yourself:
"""
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chtbot = self.prompt | self.model
        self.context = ""
        self.search =""
    def reply_chtbot(self,question):
        return self.chtbot.stream({"question":question,"context":self.context,"search":self.search})
    def search_thing(self,search_question):
        edited_search = re.sub(r"(?i)\bsearch( about)?\b", "",search_question).strip()
        
        try: 
            self.result_search = wikipedia.summary(edited_search, sentences=20)#self.ddgs.text(search_question,max_results=5)
            if self.result_search != "":
                self.search = self.result_search
            else:
                self.search = "No search results found."
        except Exception:
            self.search = "Internet Error, Can't search"
