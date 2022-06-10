import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';

import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button';
import {Divider, Grid, Paper, Stack, TextareaAutosize} from "@mui/material";
import "./Annotate.css"
import SwapVertIcon from '@mui/icons-material/SwapVert';
import {grey} from "@mui/material/colors";
import ReactAudioPlayer from 'react-audio-player';
import PlayCircleIcon from '@mui/icons-material/PlayCircle';
import PauseCircleIcon from '@mui/icons-material/PauseCircle';
import ReplayCircleFilledIcon from '@mui/icons-material/ReplayCircleFilled';

// A Pair of blocks that contain the transcriptions from both models, the swap button and the final text input
// Props transcr1, transcr2, kbSelected, onclick, selectedTranscription
function SubmitButton(props){
    return (
        <button style={{
            backgroundColor: "lightgreen",
            margin: "5px",
            borderRadius: "5px",
            width: "100px",
            height: "50px",
        }}
                onClick={props.onSubmit}
        >Submit</button>
    );
}

// Annotation screen component. Data arguments are blocks (transcription blocks)
// And when submitting it should make a post request to the backend with the result
// Props:
//          blocks: A list of blocks (tuples) containing transcriptions. Each tuple is
//                  (googleTranscription, kbTranscription)
//          onSubmit: A callback that is called when the user has finished annotating the utterance. The parameters
//                  passed to the callback is the final concatenated transcription string
//          blockEndTimes: A list containing the end times in seconds for each of the blocks
class Annotate extends React.Component {
    constructor(props) {
        super(props);

        this.getSelectedTranscription = this.getSelectedTranscription.bind(this)
        this.onSubmit = this.onSubmit.bind(this)

        this.textBoxRef = React.createRef()

        this.rap = undefined
    }
    // On submit used in the components children
    onSubmit(){
        this.props.onSubmit(this.getSelectedTranscription())
    }
    getSelectedTranscription() {
        // ContentEditable in userInput makes user input add a newline at the end
        // (sometimes)
        return this.textBoxRef.current.textContent
    }

    render(){
      return (<>
      <div style={{
          display: "flex",
          flexDirection: "column"
      }}>
          <ReactAudioPlayer
              src={this.props.audioFilePath}
              controls
              ref={(element) => { this.rap = element; }}
          />
              <TextareaAutosize ref={this.textBoxRef}>
                  {this.props.transcription}
              </TextareaAutosize>
              <SubmitButton onSubmit={this.onSubmit}/>
      </div>
        </>
    );
    }
}
export default Annotate;