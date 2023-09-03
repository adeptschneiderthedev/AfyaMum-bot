# Twilio Whatsapp utility package imports

# Standard library imports
import logging
import param, textwrap, os, datetime

# Third party imports
from twilio.rest import Client
from decouple import config
import openai

# Chatbot imports
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.vectorstores import FAISS
from InstructorEmbedding import INSTRUCTOR
from langchain.embeddings import HuggingFaceInstructEmbeddings

# Set up the OpenAI API client, Langchain smith
openai.api_key = config("OPENAI_API_KEY")
langchain_tracing_v2 = config('LANGCHAIN_TRACING_V2')
langchain_endpoint = config('LANGCHAIN_ENDPOINT')
langchain_api_key = config('LANGCHAIN_API_KEY')


current_date = datetime.datetime.now().date()
if current_date < datetime.date(2023, 9, 2):
    llm_name = "gpt-3.5-turbo-0301"
else:
    llm_name = "gpt-3.5-turbo"
print(llm_name)


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = config("TWILIO_ACCOUNT_SID")
auth_token = config("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = config('TWILIO_NUMBER')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sending message logic through Twilio Messaging API
def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}"
            )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")



DB_FAISS_PATH = '../vectorstore/db_faiss'

custom_prompt_template = """
Provide the user with clear and concise information, limited to 250 words, to ensure easy understanding. If you don't have the answer, please state that you don't know rather than attempting to provide inaccurate information.

**Question**: {question}

For expectant mothers, please provide the following:

**Symptom Assessment**: Offer an assessment of the symptoms described in the query.

**Risk Evaluation**: Evaluate potential risks and complications that expectant mothers may face based on the conditions presented in the query.

**Personalized Guidance**: Suggest recommended actions, preventive measures, and self-care tips tailored to the user's specific situation.

**Specialist Referral**: Specify whether specialized medical attention may be necessary and, if so, provide guidance on how to seek such care.

**Risk Level**: Assess the risk level associated with the symptoms or conditions mentioned (e.g., high, medium, or low risk).

**Possible Remedies (for Low Risk)**: If the risk level is determined to be low, suggest appropriate remedies or self-care steps.
"""

def set_custom_prompt():
    """
    Prompt template for ConversationalRetrievalQAChain
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt

# ConversationalRetrievalChain
def conversational_retrieval_chain(llm, prompt, db, k, chain_type):
    # create a chatbot chain. Memory is managed externally.
    # define retriever
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        chain_type=chain_type, 
        retriever=retriever, 
        return_source_documents=True,
        return_generated_question=True,
        combine_docs_chain_kwargs={'prompt': prompt}
    )
    return qa 

class AfyaMumbot(param.Parameterized):
    chat_history = param.List([])
    answer = param.String("")
    db_query = param.String("")
    db_response = param.List([])

    def __init__(self, **params):
        super(cbfs, self).__init__(**params)
        llm = ChatOpenAI(model_name=llm_name, temperature=0.5)
        prompt = set_custom_prompt()
        # embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})
        embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl", model_kwargs={"device": "cpu"})
        db = FAISS.load_local(DB_FAISS_PATH, embeddings)
        self.qa = conversational_retrieval_chain(llm, prompt, db, 4, "stuff")

    def convchain(self, query):
        lines = query.split('\n')
        wrapped_lines = [textwrap.fill(line, width=110) for line in lines]
        wrapped_text = '\n'.join(wrapped_lines)
        result = self.qa({"question": wrapped_text, "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        self.db_query = result["generated_question"]
        self.db_response = result["source_documents"]
        self.answer = result['answer']
        return self.answer
    
def generate_response(query):
    cb = AfyaMumbot()
    return cb.convchain(query)