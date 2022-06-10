import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import Annotate from "./Annotate";

// ReactDOM.render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>,
//   document.getElementById('root')
// );

function onSubmit(str){
    alert("Received response: " + str)
}

ReactDOM.render(
  <React.StrictMode>
    <Annotate
        transcription={[
                 "istället ska juridik och beteendevetenskap inga i utbildningen på polishhögskolan"
        ]}
        audioFilePath={"/file_7.wav"}
        onSubmit={onSubmit}
        blockEndTimes={[
            1.6,4.1,4.5,5.9
        ]}
    />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals(console.log);
