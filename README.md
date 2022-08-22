# Speech Unlock

An integrated audio annotation pipeline to help researchers and  developers 
annotate their speech data developed by [TMH](https://www.kth.se/is/tmh)


- Breath and silence detection
- Speaker diarization
- Overlap detection (TODO)
- Laughter detection (TODO)
- Automatic Speech recognition (ASR) (TODO)

Speech Unlock offers pre-trained models as well as training capabilities 
for them

Another feature that Speech Unlock provides is the ability to generate 
and host ASR crowdsourcing tasks for Prolific, Amazon Mechanical Turk


## File format

The file format that is central for Speech Unlock and is 
used throughout the pipelines is called a lab file and 
has a `.lab` extension. 

The lab file contains multiple files and each line contains one 
temporal annotation segment (for example a continuous 
time period within a file where a person laughed) and has the
following format: `<start_sec> 
<end_sec>  <text>` where `<start_sec>` is the start of the segment 
in seconds, `<end_sec>` is the end of the segment is seconds and 
`<text>` is the label of the annotation segment.

## Setting up the development environment

To set up the pip dependencies install pip requirements
on a clean environment:
```
pip install -r requirements.txt
```