import unittest

from pydub import AudioSegment

from speech_unlock.utils.preprocess import \
    calculate_num_samples_for_seconds
from speech_unlock.utils.loadfile import generate_unique_tmp_filename
from speech_unlock.utils.generate_data import generate_bogus_wav_file


class MyTestCase(unittest.TestCase):
    def test_audio_from_file_has_correct_duration(self):
        fname = generate_unique_tmp_filename()
        fname = fname + ".wav"
        sr = 44100
        num_seconds = 5.5

        num_samples = calculate_num_samples_for_seconds(sr, num_seconds)

        generate_bogus_wav_file(sr, fname, num_samples)

        segment = AudioSegment.from_file(fname)
        self.assertTrue(len(segment) / 1000 == num_seconds)


if __name__ == "__main__":
    unittest.main()
