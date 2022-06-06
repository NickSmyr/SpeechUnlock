import unittest
import numpy as np

from speech_unlock.pipeline.abstract.annotation import IntervalAnnotation
from speech_unlock.pipeline.speaker_diarization.resemblyzer_diarization import \
    generate_speaker_intervals_from_scores


class MyTestCase(unittest.TestCase):
    def test_generate_speaker_intervals_correct_outputs(self):
        scores_per_frame = {
            'albin' : np.array([0.3, 0.3, 0.3, 0.3]),
            'david' : np.array([0.4, 0.4, 0.2, 0.4])
        }
        intervals = generate_speaker_intervals_from_scores(scores_per_frame,
                                               sample_rate_hz=2,
                                               samples_per_frame=3)
        correct_annotations = [
            IntervalAnnotation(0, 3, "david"),
            IntervalAnnotation(3, 4.5, "albin"),
            IntervalAnnotation(4.5, 6, "david")
        ]

        for int, int_true in zip(intervals, correct_annotations):
            self.assertEqual(int, int_true)


if __name__ == '__main__':
    unittest.main()
