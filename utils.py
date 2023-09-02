from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain import PromptTemplate
from langchain.vectorstores import FAISS
from InstructorEmbedding import INSTRUCTOR
from langchain.embeddings import HuggingFaceInstructEmbeddings

DB_FAISS_PATH = '../vectorstore/db_faiss'

custom_prompt_template = """Use the following pieces of information to answer the user's question in a simple manner which will enable him or her to easily understand.
Limit the response to 250 words.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer, risk level e.g high, medium or low risk, and possible remedies if low risk involved
below and nothing else.
Helpful answer for expectant mothers:

Symptom Assessment: Provide an assessment of the symptoms described in the query.

Risk Evaluation: Evaluate the potential risks and complications expectant mothers may be predisposed to based on the conditions presented in the query.

Personalized Guidance: Offer recommended actions, preventive measures, and self-care tips tailored to the user's specific situation.

Specialist Referral: Indicate whether specialized medical attention may be needed and, if so, provide guidance on seeking such care.

Risk Level: Assess the risk level associated with the symptoms or conditions mentioned (e.g., high, medium, or low risk).

Possible Remedies (for Low Risk): If the risk level is low, suggest appropriate remedies or self-care steps.
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

import param, textwrap

class cbfs(param.Parameterized):
    chat_history = param.List([])
    answer = param.String("")
    db_query = param.String("")
    db_response = param.List([])

    def __init__(self, **params):
        super(cbfs, self).__init__(**params)
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
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
    cb = cbfs()
    return cb.convchain(query)