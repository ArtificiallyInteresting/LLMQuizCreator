import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Container from '@mui/material/Container';
import React from 'react';


class ThingPicker extends React.Component {
  constructor(props) {
      super(props);
  }

  render() {
    return    <Container maxWidth="sm">
                <TextField name="thing" value={this.props.label} label="Thing" onChange={this.props.handleThingChange}/>
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
  const handleThingChange = (event) => {
    const value = event.target.value;
    setThing(value);
  };
  const handleFirstSubmit = event => {
    event.preventDefault();
   setSubmitting(true);

   setTimeout(() => {
     setSubmitting(false);
   }, 3000)
  }
   const handleSecondSubmit = event => {
     event.preventDefault();
    setSubmitting(true);
 
    setTimeout(() => {
      setSubmitting(false);
    }, 3000)
  }


  const generateQuestions = () => {
   fetch("http://127.0.0.1:5000/generateQuestions", {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      "Access-Control-Allow-Origin": "*",
    },
    body: JSON.stringify({"thing": thing, "items": items}),
  })
    .then((response) => {
      console.log(response)
      if (response.status !== 200) {
        throw new Error(response.statusText);
      }
      
      return response.json();
    })
    .then(() => {
      console.log("Success")
    })
    .catch((err) => {
      console.log(err)
    });
  }
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1>Which {thing} are You?</h1>
      </header>
      <div className="wrapper">
        {submitting &&
        <div>Submtting Form...</div>
      }
        <form onSubmit={handleFirstSubmit}>
        <ThingPicker label={thing} handleThingChange={handleThingChange}/>
        <Container maxWidth="sm">
          <fieldset>
            {items.map(item => <div> <TextField label={thing} value={item["name"]}></TextField></div>)} 
          </fieldset>
        </Container>
        
        <Container maxWidth="sm">
          <fieldset>
            {items.map(item => <div><TextField label={item["name"]} value={item["description"]}></TextField></div>)} 
          </fieldset>
        </Container>
        <Button type="submit">Submit</Button>

        <Container maxWidth="xl">
          <fieldset>
            {questions.map(question => <div><TextField label={question["question"]} value={question["answer"]}></TextField></div>)}
          </fieldset>
        </Container>
          
        </form>
        {/* <form onSubmit={handleSecondSubmit} hidden={questions.length == 0}>
          <fieldset>
            <label>
              <TextField name="thing" value="animal" label="Thing"/>
            </label>
            {items.map(item => <div><p>{item["name"]}</p> <TextField label={item["name"]} value={item["description"]}></TextField></div>)} 
          </fieldset>
          <Button type="submit">Submit</Button>
        </form> */}
      </div>
    </div>
    
    
  );
}

export default App;
