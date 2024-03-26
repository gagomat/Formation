"""Contain functions to load data from file in the application."""

import logging

from streamlit.runtime.uploaded_file_manager import UploadedFile

from spectrum import Spectrum

log = logging.getLogger(__name__)


def load_spectrum_file(
    path: UploadedFile
) -> None:
    """Load a spectrum from a file. Returns an error message if necessary."""
    spectrum = Spectrum.from_file(path)

    return spectrum