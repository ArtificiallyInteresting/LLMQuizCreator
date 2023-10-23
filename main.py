# A simple streamlit app which takes in four text inputs for names and then another four text inputs for a description of each name. Finally, it displays the names and descriptions in a dataframe.

import streamlit as st
import pandas as pd


from langchain.chat_models import ChatOpenAI

from langchain import PromptTemplate
from langchain import LLMChain
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
)
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.schema.messages import (
    SystemMessage,
    AIMessage,
    HumanMessage
)
from dotenv import load_dotenv
load_dotenv()

TESTING = False

def generateQuestions(thing, names, descriptions):
    if TESTING:
        return ["How would you describe your physical strength and power?",
        "Do you have a natural inclination towards providing nourishment or care for others?",
        "Are you known for your fierce and deadly nature, or do you prefer a more peaceful approach?",
        "Do you enjoy being playful and silly, often making others laugh?",
        "Are you comfortable in cold environments and do you have a unique way of moving, such as waddling?"]

    template='''You are a question generating bot. Users are going to be given a quiz to determine which {thing} they are. 
    Come up with exactly 5 free-form questions that we could ask the user to determine which {thing} they are. 
    Respond only with the questions separated by newlines, and none of the questions should be multiple choice. These are the choices:\n'''

    chain_variables = {"thing":thing}
    for i in range(len(names)):
        template += "\n {name" + str(i) + "}: {" + "description" + str(i) + "}"
        chain_variables["name" + str(i)] = names[i]
        chain_variables["description" + str(i)] = descriptions[i]
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    prompt=PromptTemplate(
        template=template,
        input_variables=list(chain_variables.keys())
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    output = chain.run(**chain_variables)
    
    output = output.splitlines()
    return output

def analyzeAnswers():
    if TESTING:
        st.session_state["output"] = "Based on your answers, it seems like you are a penguin! You enjoy being playful and silly, and you are comfortable in cold environments. Plus, your unique way of moving, like waddling, matches with a penguin's characteristics. Have fun waddling around and making others laugh!"
        st.session_state["step"] = 4
        step = 4
        return 
    chain_variables = {"thing":thing, "human_input": ""}
    for i in range(len(names)):
        chain_variables["name" + str(i)] = names[i]
        chain_variables["description" + str(i)] = descriptions[i]

    template = "You are a funny and interesting chatbot which is analyzing user answers to determine to determine which {thing} they are. \
                                These are the choices:\n{name0}: {description0}\n{name1}: {description1}\n{name2}: {description2}\n{name3}: {description3} \
                                                    And these are the questions and answers: \n"
    for i in range(len(questions)):
        template += "\nQuestion " + str(i+1) + ": " + questions[i] + "\nAnswer " + str(i+1) + ": " + answers[i]
    template += "Alright! The results are in! And the {thing} you are is..."

    systemMessage = PromptTemplate.from_template(template=template)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    chain = LLMChain(llm=llm, prompt=systemMessage) #, memory=memory
    output = chain.run(**chain_variables)
    # st.write(output)
    st.session_state["output"] = output
    st.session_state["step"] = 4
    step = 4


st.title("LLM Quiz Generator")

if "step" in st.session_state:
    step = st.session_state["step"]
else:
    step = 1

# Choose which thing this quiz will be about
if step == 1:
    with st.form(key='thing_form') as form:
        thing = st.text_input("Let's make a quiz to determine which ____ you are", value="animal")
        thing_submitted = st.form_submit_button(
            "Submit"
        )
        if thing_submitted:
            step = 2
            st.session_state["step"] = 2
            st.session_state["thing"] = thing

#Next, give names and descriptions for each thing
if step == 2:
    thing = st.session_state["thing"]
    with st.form(key='names_form') as form:
        names = ["bear", "cow", "tiger", "penguin"]
        descriptions = ['A large furry animal. Strong and powerful.', 'A large animal. Gives milk.', 'A deadly animal. Has stripes.', 'A silly animal. Waddles. Lives in the cold.']
        
        nameInputs = []
        descriptionInputs = []
        for i, name in enumerate(names):
            nameInputs.append(st.text_input(label=thing + " " + str(i+1), value=name))
            descriptionInputs.append(st.text_input(label='description ' + str(i+1), value=descriptions[i]))
        
        names_submitted = st.form_submit_button(
            "Submit"
        )
        if names_submitted:
            step = 3
            st.session_state["step"] = 3
            st.session_state["names"] = names
            st.session_state["descriptions"] = descriptions

# Next, give the user their questions
if step == 3:
    thing = st.session_state["thing"]
    names = st.session_state["names"]
    descriptions = st.session_state["descriptions"]
    # st.write(names)
    questions = generateQuestions(thing, names, descriptions)

    with st.form(key='questions_form') as form:
        answers = []
        for question in questions:
            # st.write(question)
            answers.append(st.text_input(label=question, key=question))

        
        submit_button2 = st.form_submit_button(label='Submit')

        if submit_button2:
            # del submit_button2

           analyzeAnswers()

if step == 4:
    st.write(st.session_state["output"])

if __name__ == "__main__":
    generateQuestions("test", ["test1", "test2"], ["test1", "test2"])
