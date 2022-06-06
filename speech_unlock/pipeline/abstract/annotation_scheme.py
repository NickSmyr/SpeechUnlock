from abc import ABC
from typing import List

from speech_unlock.pipeline.abstract.annotation import (
    Annotation,
    IntervalAnnotation,
)


# TODO Maybe do validation of annotations


class AnnotationScheme(ABC):
    """
    Abstract class that represents a set of annotations within an Audio that
    follow the same semantic scheme (e.g. for breath detection there are
    only interval segments with the text 'sp', 'b' or 'sil')
    """

    def __init__(self, annotations: List[Annotation]):
        self._annotations = annotations

    @property
    def annotations(self):
        return self._annotations

    def transform_embed(self, start_sec: float, end_sec: float) -> "AnnotationScheme":
        """
        Transform the annotations and create an equivalent annotation scheme
        whose temoral annotations are transformed when the audio is embeded
        to another audio starting at start_sec and ending at end_sec
        """
        new_annotations = []
        for annotation in self._annotations:
            new_annotations.append(annotation.transform_embed(start_sec, end_sec))
        return AnnotationScheme(new_annotations)

    @classmethod
    def from_textgrid(cls, textgrid):
        intervals = textgrid.tierDict["annot"].entryList
        annotations = [
            IntervalAnnotation(x.start * 1000, x.end * 1000, x.label) for x in intervals
        ]
        return AnnotationScheme(annotations)


class IntervalAnnotationScheme(AnnotationScheme):
    def __init__(self, annotations : List[IntervalAnnotation]):
        super(IntervalAnnotationScheme, self).__init__(annotations)

    def to_lab_file(self, filename):
        with open(filename, "w") as f:
            for annotation in self.annotations:
                f.write("{} {} {}\n".format(
                    annotation.start, annotation.end, annotation.text
                ))

    @classmethod
    def from_lab_file(cls, filename):
        annotations = []
        with open(filename, "r") as f:
            for line in f.readlines():
                splitted = line.split()
                start = float(splitted[0])
                end = float(splitted[1])
                text = " ".join(splitted[2:])
                annotations.append(IntervalAnnotation(start, end, text))

        return IntervalAnnotationScheme(annotations)


class BreathDetectionScheme(AnnotationScheme):
    """
    Interval Annotations with only texts in 'sp', 'b' and 'sil'
    """
