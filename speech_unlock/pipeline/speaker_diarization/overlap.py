from pyannote.audio.pipelines import OverlappedSpeechDetection

HYPER_PARAMETERS = {
    # onset/offset activation thresholds
    "onset": 0.5,
    "offset": 0.5,
    # remove speech regions shorter than that many seconds.
    "min_duration_on": 0.0,
    # fill non-speech regions shorter than that many seconds.
    "min_duration_off": 0.0,
}

pipeline = OverlappedSpeechDetection(segmentation="pyannote/segmentation")


def overlap_detection(audio_path):
    pipeline.instantiate(HYPER_PARAMETERS)
    overlap = pipeline(audio_path)
    return overlap.for_json()
