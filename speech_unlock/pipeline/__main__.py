"""Python cmd tool to perform breath/silence detection, speaker diarization
on large files for conversion into small utterances for ASR systems. Also
provides functionality for creating tasks for crowdworkers and hosting the
tasks locally """
import shutil

import click
import os
from os.path import basename, join
from praatio import tgio
from pydub import AudioSegment

from speech_unlock.pipeline.abstract.annotation_scheme import \
    IntervalAnnotationScheme


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

BREATH_DETECTION_MODEL_PATH = "./models/modelMix4.h5"


@click.group()
def main():
    pass


@main.command()
@click.option(
    "--input-wav",
    type=click.Path(exists=True),
    required=True,
    help="The filename to split on breaths and silences",
)
@click.option("--output-dir", required=True, help="The output directory for files")
@click.option("--model-path", help="The trained model to use")
def split(input_wav, output_dir, model_path):
    """
    Split files according to breaths and silences. For each input file
    A directory is created in the form <filename>.d and the splitted
    utterance files are placed inside in the format file_<x>.wav.

    Utterances are segments of speech that are

    This command is mainly for processing large files with long sound
    recordings and it can process about 1GB of data per 16 minutes. However
    significant improvements can be achieved by multi core processors due to
    parallelization. On large files a progress bar is output showing the
    progress in MBytes

    Examples:\n
        python -m pipeline split --input-wav mywavfile --output-filename

    Some files may end up mistaken, containing breaths or silences since this
     algorithm
    is based on a statistical model
    """
    # Disable TF logging for now TODO
    # We don't want to import stuff that take a long time ( import
    # tensorflow should not have to run if we just want the help dialogues)
    from speech_unlock.pipeline.breath_detection.split_on_breaths_and_silences import (
        split_on_breaths_and_silences,
    )

    # TODO keep only necessary click logic
    if model_path is None:
        model_path = BREATH_DETECTION_MODEL_PATH

    split_output_dir = join(output_dir, "tmp")
    try:
        split_on_breaths_and_silences(input_wav, split_output_dir, model_path)
    except Exception as e:
        raise Exception(
            "Failed to split on breaths. This most likely means no breaths "
            "were detected from the input file"
        ) from e
    tg = tgio.openTextgrid(
        join(split_output_dir, "C" + basename(input_wav) + ".TextGrid")
    )
    intervals = tg.tierDict["annot"].entryList
    speakingIntervals = [x for x in intervals if x.label == "sp"]
    song = AudioSegment.from_wav(input_wav)
    for i, interval in enumerate(speakingIntervals):
        utterance = song[interval.start * 1000 : interval.end * 1000]
        utterance.export(join(output_dir, f"file_{i}.wav"), format="wav")
    print(f"Generated {len(intervals)} utterances in directory {output_dir}")
    # Clean up files generated from breath detection
    # shutil.rmtree(split_output_dir)


@main.command()
@click.option(
    "--input-wav",
    type=click.Path(exists=True),
    required=True,
    help="The filename to diarize",
)
@click.option(
    "--output-filename",
    required=False,
    help="The name of the filename to output the annotations"
)
@click.option(
    "--speaker-data-filename",
    type=click.Path(exists=True),
    required=True,
    help="A .lab file containing some initial data about the speakers. "
         "There should be at least one annotated interval in seconds for "
         "each speaker"
)
@click.option(
    "--demo",
    required=False,
    is_flag = True,
    help="Run an interactive demo plotting the results instead of saving to "
         "a file"
)
def diarize(input_wav, output_filename, speaker_data_filename, demo):
    """

    Examples:\n
        python -m pipeline diarize --input-wav mywavfile --output-filename
        --speaker_data_filename my_speaker_file.lab

    This diarization backend needs a .lab file specifying some initial
    datapoints about the speakers
    """
    # Imports go here to make click faster
    from speech_unlock.pipeline.speaker_diarization.\
        resemblyzer_diarization import \
        generate_scores_per_frame

    from speech_unlock.utils.file_formats import parse_lab_file

    from speech_unlock.pipeline.speaker_diarization.resemblyzer_diarization import \
        generate_speaker_intervals_from_scores
    from speech_unlock.utils.loadfile import get_audiofile_sr
    from speech_unlock.pipeline.speaker_diarization.resemblyzer_diarization import \
        demo_diarization

    intervals = parse_lab_file(speaker_data_filename)
    speaker_segments = [ [x.start, x.end] for x in intervals]
    speaker_names = [x.text for x in intervals]
    #sample_rate = get_audiofile_sr(input_wav)
    # Resemblyzer needs 16000 to function
    sample_rate = 16000


    # Save annotations or do the demo
    if demo:
        demo_diarization(
            filepath=input_wav,
            speaker_segments = speaker_segments,
            speaker_names= speaker_names,
            sr=sample_rate)
    else:
        scores = generate_scores_per_frame(filepath=input_wav,
                                           speaker_segments=speaker_segments,
                                           speaker_names=speaker_names,
                                           sr=sample_rate)
        intervals = generate_speaker_intervals_from_scores(
            scores,
            sample_rate_hz=sample_rate)

        scheme = IntervalAnnotationScheme(intervals)
        scheme.to_lab_file(output_filename)



if __name__ == "__main__":
    main()
