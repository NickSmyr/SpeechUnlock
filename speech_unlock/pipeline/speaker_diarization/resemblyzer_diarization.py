from typing import List, Dict

import numpy as np
from resemblyzer.audio import preprocess_wav
from resemblyzer.voice_encoder import VoiceEncoder

from speech_unlock.pipeline.abstract.annotation import IntervalAnnotation
from speech_unlock.pipeline.speaker_diarization.demo_utils import \
    interactive_diarization


def generate_speaker_intervals_from_scores(
        scores_per_frame : Dict[str, np.ndarray],
        sample_rate_hz : int,
        samples_per_frame: int = 16,
) -> List[IntervalAnnotation]:
    """
    Generate IntervalAnnotations based on who is speaking
    # TODO maybe need to create an unsure label
    """
    speaker_names = [k for k in scores_per_frame]
    # Shape n_frames x n_speakers
    concatenated_arrays = np.concatenate([
       scores_per_frame[speaker_name][..., np.newaxis] for speaker_name in
                                         speaker_names],
        axis=1)
    speaker_idxs = concatenated_arrays.argmax(axis=1) # n_frames,

    ## TODO optimize (is there a numpy function to extract the continuous
    #   intervals?)
    previous_speaker = None
    # Start and stop in frame idxs
    previous_range = None
    # Split speakers into contiguous segments
    intervals = []
    for frame_i, speaker_idx in enumerate(speaker_idxs):
        if previous_speaker is None:
            previous_speaker = speaker_idx
            previous_range = [frame_i]
            continue

        curr_speaker = speaker_idx
        # Another speaker starts speaking
        if curr_speaker != previous_speaker:
            # End of previous segment
            previous_range.append(frame_i)
            intervals.append(IntervalAnnotation(
                start_sec=previous_range[0] * samples_per_frame /
                          sample_rate_hz,
                end_sec=previous_range[1] * samples_per_frame /
                          sample_rate_hz,
                text=speaker_names[previous_speaker]
            ))
            previous_speaker = curr_speaker
            previous_range = [frame_i]

    # Add the last chunk
    previous_range.append(len(speaker_idxs))
    intervals.append(IntervalAnnotation(
        start_sec=previous_range[0] * samples_per_frame /
                  sample_rate_hz,
        end_sec=previous_range[1] * samples_per_frame /
                sample_rate_hz,
        text=speaker_names[previous_speaker]
    ))
    return intervals





def generate_scores_per_frame(
    filepath: str,
    speaker_segments: List[List[int]],
    speaker_names: List[str],
    sr: int,
    device: str = "cpu",
    samples_per_frame : int = 16
) -> Dict[str, np.ndarray]:
    """
    Generates scores per frame based on the resemblyzer

    :param device: 'cpu' or 'gpu'
    """
    wav = preprocess_wav(filepath)

    # Cut some segments from single speakers as reference audio
    speaker_wavs = [wav[int(s[0] * sr) : int(s[1] * sr)] for s in speaker_segments]

    ## Compare speaker embeds to the continuous embedding of the interview
    # Derive a continuous embedding of the interview. We put a rate of 16, meaning that an
    # embedding is generated every 0.0625 seconds. It is good to have a higher rate for speaker
    # diarization, but it is not so useful for when you only need a summary embedding of the
    # entire utterance. A rate of 2 would have been enough, but 16 is nice for the sake of the
    # demonstration.
    # We'll exceptionally force to run this on CPU, because it uses a lot of RAM and most GPUs
    # won't have enough. There's a speed drawback, but it remains reasonable.
    encoder = VoiceEncoder(device)
    _, cont_embeds, wav_splits = encoder.embed_utterance(
        wav, return_partials=True, rate=samples_per_frame
    )

    # Get the continuous similarity for every speaker. It amounts to a dot product between the
    # embedding of the speaker and the continuous embedding of the interview
    # 256 size per speaker
    speaker_embeds = [
        encoder.embed_utterance(speaker_wav) for speaker_wav in speaker_wavs
    ]

    # (Num frames,) shape array with scores per speaker
    similarity_dict = {
        name: cont_embeds @ speaker_embed
        for name, speaker_embed in zip(speaker_names, speaker_embeds)
    }
    ## Run the interactive demo
    #interactive_diarization(similarity_dict, wav, wav_splits)
    return similarity_dict

def demo_diarization(
    filepath: str,
    speaker_segments: List[List[int]],
    speaker_names: List[str],
    sr: int,
    device: str = "cpu",
    samples_per_frame : int = 16
) :
    """
    Generates scores per frame based on the resemblyzer

    :param device: 'cpu' or 'gpu'
    """
    ## TODO refactor duplicate code
    wav = preprocess_wav(filepath)

    # Cut some segments from single speakers as reference audio
    speaker_wavs = [wav[int(s[0] * sr) : int(s[1] * sr)] for s in speaker_segments]

    ## Compare speaker embeds to the continuous embedding of the interview
    # Derive a continuous embedding of the interview. We put a rate of 16, meaning that an
    # embedding is generated every 0.0625 seconds. It is good to have a higher rate for speaker
    # diarization, but it is not so useful for when you only need a summary embedding of the
    # entire utterance. A rate of 2 would have been enough, but 16 is nice for the sake of the
    # demonstration.
    # We'll exceptionally force to run this on CPU, because it uses a lot of RAM and most GPUs
    # won't have enough. There's a speed drawback, but it remains reasonable.
    encoder = VoiceEncoder(device)
    _, cont_embeds, wav_splits = encoder.embed_utterance(
        wav, return_partials=True, rate=samples_per_frame
    )

    # Get the continuous similarity for every speaker. It amounts to a dot product between the
    # embedding of the speaker and the continuous embedding of the interview
    # 256 size per speaker
    speaker_embeds = [
        encoder.embed_utterance(speaker_wav) for speaker_wav in speaker_wavs
    ]

    # (Num frames,) shape array with scores per speaker
    similarity_dict = {
        name: cont_embeds @ speaker_embed
        for name, speaker_embed in zip(speaker_names, speaker_embeds)
    }
    ## Run the interactive demo
    interactive_diarization(similarity_dict, wav, wav_splits, sr)
