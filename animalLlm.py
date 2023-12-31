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


def generateQuestions(thing, items):

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    template='''You are a question generating bot. Users are going to be given a quiz to determine which {thing} they are. Come up with exactly 5 questions that we could ask the user to determine which {thing} they are. These are the choices:\n'''
    names = []
    descriptions = []
    inputVariables = {"thing":thing}
    for i in range(len(items)):
        template += " {name" + str(i) + "}: {" + "description" + str(i) + "} \n"
        name = [items[i]["name"]]
        description = [items[i]["description"]]
        inputVariables["name" + str(i)] = name
        inputVariables["description" + str(i)] = description
    prompt=PromptTemplate(
        input_variables=list(inputVariables.keys()),
        template=template,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    output = chain.run(**inputVariables)

    #Validation here?

    questions = output.split("\n")
    return questions

def analyzeAnswers(thing, items, questions):
    history = ChatMessageHistory()
    template = "You are a funny and interesting chatbot analyzing the answers to a quiz to determine which {thing} the user is. The user will end up being one of these things: \n "
    for i in range(len(items)):
        template += items[i]["name"] + ": " + items[i]["description"] + " \n "
    # systemMessage = SystemMessagePromptTemplate.from_template(template=template, thing=thing, names=names, descriptions=descriptions)
    template += "Do not ask any additional questions, just tell the user which {thing} they are, and give a funny and clever explanation as to why \n "
    # systemContent = template.format(thing=thing)
    # systemMessage = SystemMessage(content=systemContent)
    print(template)

    # history.add_message(systemMessage)
    
    for i in range(len(questions)):
        history.add_message(AIMessage(content="Question " + str(i) + ": " + questions[i]["question"]))
        history.add_message(HumanMessage(content=questions[i]["answer"]))
    # history.add_message(AIMessage(content="Alright! The results are in! And the {thing} you are is...".format(thing=thing)))
    memory = ConversationBufferMemory(return_messages=True)
    memory.load_memory_variables(inputs=history)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    prompt = PromptTemplate(
        input_variables=["thing"], template=template
    )
    chain = LLMChain(llm=llm, memory=memory, prompt=prompt)
    output = chain.run(thing=thing)
    print(output)
    return output



if __name__ == "__main__":
    thing = "animal"
    names = ["lion", "penguin"]
    descriptions = ["brave and fiersome", "cold and silly"]
    # questions = generateQuestions(thing, names, descriptions)
    # print(questions)

    questions = ['1. Are you more inclined towards being brave and fierce, or do you tend to be more cautious and silly in your actions?', '2. Do you prefer warmer climates or are you more comfortable in colder environments?', '3. Are you known for your bravery and leadership qualities, or do you often find yourself being silly and making others laugh?', '4. Are you more comfortable in social situations, enjoying the company of others, or do you prefer solitude and quiet moments?', '5. When faced with challenges, do you tend to face them head-on with courage, or do you prefer to take a more cautious and calculated approach?']
    answers = ["brave and fierce", "colder environments", "bravery and leadership qualities", "enjoying the company of others", "head-on with courage"]
    answers = analyzeAnswers(thing, names, descriptions, questions, answers)

    print(answers)