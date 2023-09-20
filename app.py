from flask import Flask, request, jsonify;
from flask_cors import cross_origin
import animalLlm
import json
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/generateQuestions',methods = ['POST'])
@cross_origin()
def generateQuestions():
    # print(request.body)
    data = json.loads(request.data.decode('utf-8'))
    questions = animalLlm.generateQuestions(data["thing"], data["items"])
    response = jsonify(questions)
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response



@app.route('/analyzeAnswers',methods = ['POST'])
@cross_origin()
def analyzeAnswers():
    # print(request.body)
    data = json.loads(request.data.decode('utf-8'))

    finalAnswer = animalLlm.analyzeAnswers(data["thing"], data["items"], data["questions"])
    response = jsonify({"answer": finalAnswer})
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response




