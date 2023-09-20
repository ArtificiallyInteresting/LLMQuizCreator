import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import React from 'react';
import { Modal } from '@mui/material';


class ThingPicker extends React.Component {
  render() {
    return    <Container maxWidth="sm">
                <TextField name="thing" value={this.props.label} label="Thing" onChange={this.props.handleThingChange}/>
              </Container>;
  }
}

class ItemsList extends React.Component {
  render() {
    return <Container maxWidth="sm">
      {this.props.items.map((item, i) => <div><TextField label={this.props.thing} value={item["name"]} onChange={(event) => this.props.handleItemChange(event, i)}></TextField></div>)}
      <Button onClick={() => this.props.setItems([...this.props.items, {name: "", description: ""}])}>Add Item</Button>
    </Container>;
  }
}

class DescriptionsList extends React.Component {
  render() {
    return <Container maxWidth="sm">
      {this.props.items.map((item, i) => <div><TextField label={item["name"]} value={item["description"]} onChange={(event) => this.props.handleDescriptionChange(event, i)}></TextField></div>)}
    </Container>;
  }
}
class QuestionsList extends React.Component {
  render() {
    return <Container maxWidth="sm">
      {this.props.questions.map((item, i) => <div><label>{item["question"]}</label><TextField value={item["answer"]} onChange={(event) => this.props.handleResponseChange(event, i)}></TextField></div>)}
    </Container>;
  }
}
class Result extends React.Component {
  render() {
    return <Container maxWidth="sm">
      <p>{this.props.finalResult}</p>
      <p>{this.props.explanation}</p>
    </Container>;
  }
}



function App() {
  const [submitting, setSubmitting] = useState(false);
  const [thing, setThing] = useState('Animal');
  const [items, setItems] = useState([{name: "Bear", description: "A large furry animal. Strong and powerful."}, 
          {name: "Cow", description: "A large animal. Gives milk."}, 
          {name: "Tiger", description: "A deadly animal. Has stripes."}, 
          {name: "Penguin", description: "A silly animal. Waddles. Lives in the cold."}])
  const [questions, setQuestions] = useState([])
  const [result, setResult] = useState([])
  const [explanation, setExplanation] = useState([])
  const [page, setPage] = useState(0);
  const handleThingChange = (event) => {
    const value = event.target.value;
    setThing(value);
  };
  const handleItemChange = (event, i) => {
    const value = event.target.value;
    const newItems = [...items];
    newItems[i]["name"] = value;
    setItems(newItems);
  };
  const handleDescriptionChange = (event, i) => {
    const value = event.target.value;
    const newItems = [...items];
    newItems[i]["description"] = value;
    setItems(newItems);
  };
  const handleResponseChange = (event, i) => {
    const value = event.target.value;
    const newItems = [...questions];
    newItems[i]["answer"] = value;
    setQuestions(newItems);
  };
  const handleFirstSubmit = async event => {
    event.preventDefault();
    setSubmitting(true);

    setTimeout(() => {
      setSubmitting(false);
    }, 3000)
    var generatedQuestions = await generateQuestions();
    var questionsObjects = []
    generatedQuestions.forEach(question => {
        questionsObjects.push({"question": question, "answer": ""})
    })
    setQuestions(questionsObjects);
    setPage(1)
  }
   const handleSecondSubmit = event => {
     event.preventDefault();
    setSubmitting(true);
 
    setTimeout(() => {
      setSubmitting(false);
    }, 3000)
    var result = getResult();
    setResult(result["finalResult"]);
    setExplanation(result["explanation"]);
    setPage(2)
  }


  const getResult = async () => {
    // return {"finalResult":"bear", "explanation":"because we're testing"}
    return await fetch("http://127.0.0.1:5000/analyzeAnswers", {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify({"thing": thing, "items": items, "questions": questions}),
    })
      .then((response) => {
        if (response.status !== 200) {
          throw new Error(response.statusText);
        }
        
        var responseJson = response.json()
        console.log(responseJson)
        return responseJson;
      })
      // .then(() => {
      //   console.log("Success")
      // })
      .catch((err) => {
        console.log(err)
      });
  }
  const generateQuestions = async () => {
    return [
      "1. Are you more comfortable in cold or warm climates?",
      "2. Do you consider yourself to be strong and powerful?",
      "3. Are you known for your silliness or sense of humor?",
      "4. Do you have a preference for living in water or on land?",
      "5. Are you often described as deadly or dangerous?"
    ]    
   return await fetch("http://127.0.0.1:5000/generateQuestions", {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      "Access-Control-Allow-Origin": "*",
    },
    body: JSON.stringify({"thing": thing, "items": items}),
  })
    .then((response) => {
      if (response.status !== 200) {
        throw new Error(response.statusText);
      }
      
      var responseJson = response.json()
      console.log(responseJson)
      return responseJson;
    })
    // .then(() => {
    //   console.log("Success")
    // })
    .catch((err) => {
      console.log(err)
    });
  }
  
  switch (page){
    case 0:
      return (
        <div className="App">
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <h1>Which {thing} are You?</h1>
            </Grid>

            <form onSubmit={handleFirstSubmit}>
            <Grid item xs={12}>
            <ThingPicker label={thing} handleThingChange={handleThingChange}/>
            </Grid>
            <Grid item xs={12}>
            <ItemsList items={items} setItems={setItems} thing={thing} handleItemChange={handleItemChange}/>
            </Grid>
            <DescriptionsList items={items} setItems={setItems} handleDescriptionChange={handleDescriptionChange}/>

            <Button type="submit">Submit</Button> 
            </form>

          </Grid>

        </div>
      );
    case 1:
      return (
      <Grid container spacing={2}>
        
        <form onSubmit={handleSecondSubmit}>
          <br></br>
          <QuestionsList questions={questions} setQuestions={setQuestions} handleResponseChange={handleResponseChange}/>
          <Button type="submit">Submit</Button> 
        </form>
      </Grid>
      );
    case 2:
      return (
      <Grid container spacing={2}>
        <Result finalResult={result} explanation={explanation}></Result>
      </Grid>
      );
      }
}

export default App;
