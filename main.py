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

thing = None
df = None

def displayForm():
    st.title("Name and Description")

    # A streamlit form which takes in four text inputs for names and then another four text inputs for a description of each name.
    with st.form(key='name_form') as form:
        thing = st.text_input(label='Thing', value='Animal')
        name1 = st.text_input(label='Name 1', value='Bear')
        name2 = st.text_input(label='Name 2', value='Cow')
        name3 = st.text_input(label='Name 3', value='Tiger')
        name4 = st.text_input(label='Name 4', value='Penguin')
        description1 = st.text_input(label='Description 1', value='A large furry animal. Strong and powerful.')
        description2 = st.text_input(label='Description 2', value='A large animal. Gives milk.')
        description3 = st.text_input(label='Description 3', value='A deadly animal. Has stripes.')
        description4 = st.text_input(label='Description 4', value='A silly animal. Waddles. Lives in the cold.')
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Create a dataframe with the names and descriptions
        df = pd.DataFrame({'Name': [name1, name2, name3, name4], 'Description': [description1, description2, description3, description4]})
        st.dataframe(df)
        # displayQuestionForm(thing, name1, name2, name3, name4, description1, description2, description3, description4)
        displayQuestionForm()

#Yes I know this is too many parameters and it's stupid
def displayQuestionForm():
    
    with st.form(key='question_form'):

        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        prompt=PromptTemplate(
            template='''You are a question generating bot. Users are going to be given a quiz to determine which {thing} they are. Come up with exactly 5 questions that we could ask the user to determine which {thing} they are. These are the choices:
            {name1}: {description1}
            {name2}: {description2}
            {name3}: {description3}
            {name4}: {description4}''',
            input_variables=["thing", "name1", "description1", "name2", "description2", "name3", "description3", "name4", "description4"],
        )
        
        chain = LLMChain(llm=llm, prompt=prompt)
        output = chain.run(thing=thing, name1=df['Name'][0], description1=df['Description'][0], name2=df['Name'][1], description2=df['Description'][1], name3=df['Name'][2], description3=df['Description'][2], name4=df['Name'][3], description4=df['Description'][3])
        st.write(output)

        #Validation here?

        questions = "\n".split(output)
        answers = []
        for question in questions:
            st.write(question)
            answers.append(st.text_input(label='Answer', key=question))

        
        submit_button2 = st.form_submit_button(label='Submit')

        if submit_button2:
            del submit_button2

            history = ChatMessageHistory()

            systemMessage = SystemMessagePromptTemplate.from_template(template="You are a funny and interesting chatbot giving users a quiz to determine which {thing} they are. \
                                        You are going to ask the user 5 questions to determine which {thing} they are.\
                                        These are the choices:\n{choice1}: {description1}\n{choice2}: {description2}\n{choice3}: {description3}\n{choice4}: {description4}")
            history.add_message(systemMessage.format(thing=thing, name1=name1, description1=description1, name2=name2, description2=description2, name3=name3, description3=description3, name4=name4, description4=description4))
            history.add_message(AIMessage(content="Question 1: " + questions[0]))
            history.add_message(HumanMessage(content=answers[0]))
            history.add_message(AIMessage(content="Question 2: " + questions[1]))
            history.add_message(HumanMessage(content=answers[1]))
            history.add_message(AIMessage(content="Question 3: " + questions[2]))
            history.add_message(HumanMessage(content=answers[2]))
            history.add_message(AIMessage(content="Question 4: " + questions[3]))
            history.add_message(HumanMessage(content=answers[3]))
            history.add_message(AIMessage(content="Alright! The results are in! And the {thing} you are is...".format(thing=thing)))
            st.write(history)
            memory = ConversationBufferMemory(return_messages=True)
            memory.load_memory_variables(inputs=history)
            chain = LLMChain(llm=llm, memory=memory)
            output = chain.run()
            st.write(output)


displayForm()
# displayQuestionForm()

