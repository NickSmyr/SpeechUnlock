import unittest

from speech_unlock.pipeline.abstract.annotation import IntervalAnnotation
from speech_unlock.pipeline.abstract.annotation_scheme import \
    IntervalAnnotationScheme
from speech_unlock.utils.loadfile import generate_unique_tmp_filename


class MyTestCase(unittest.TestCase):
    def test_interval_annotation_scheme_persistence(self):
        fname = generate_unique_tmp_filename()
        annotations = [
            IntervalAnnotation(0.5, 3.5, 'a'),
            IntervalAnnotation(3.5, 4.5, 'b')
        ]
        scheme = IntervalAnnotationScheme(annotations)
        scheme.to_lab_file(fname + ".lab")
        new_scheme = IntervalAnnotationScheme.from_lab_file(fname + ".lab")
        for a1 , a2 in zip(scheme.annotations, new_scheme.annotations):
            self.assertEqual(a1, a2)


if __name__ == '__main__':
    unittest.main()
