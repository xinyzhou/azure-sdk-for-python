# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from enum import Enum


class Gender(str, Enum):

    male = "Male"
    female = "Female"


class TextOperationStatusCodes(str, Enum):

    not_started = "NotStarted"
    running = "Running"
    failed = "Failed"
    succeeded = "Succeeded"


class TextRecognitionResultDimensionUnit(str, Enum):

    pixel = "pixel"
    inch = "inch"


class TextRecognitionResultConfidenceClass(str, Enum):

    high = "High"
    low = "Low"


class DescriptionExclude(str, Enum):

    celebrities = "Celebrities"
    landmarks = "Landmarks"


class OcrLanguages(str, Enum):

    unk = "unk"
    zh_hans = "zh-Hans"
    zh_hant = "zh-Hant"
    cs = "cs"
    da = "da"
    nl = "nl"
    en = "en"
    fi = "fi"
    fr = "fr"
    de = "de"
    el = "el"
    hu = "hu"
    it = "it"
    ja = "ja"
    ko = "ko"
    nb = "nb"
    pl = "pl"
    pt = "pt"
    ru = "ru"
    es = "es"
    sv = "sv"
    tr = "tr"
    ar = "ar"
    ro = "ro"
    sr_cyrl = "sr-Cyrl"
    sr_latn = "sr-Latn"
    sk = "sk"


class VisualFeatureTypes(str, Enum):

    image_type = "ImageType"
    faces = "Faces"
    adult = "Adult"
    categories = "Categories"
    color = "Color"
    tags = "Tags"
    description = "Description"
    objects = "Objects"
    brands = "Brands"


class TextRecognitionMode(str, Enum):

    handwritten = "Handwritten"
    printed = "Printed"


class Details(str, Enum):

    celebrities = "Celebrities"
    landmarks = "Landmarks"
