"""Contains the Spectrum class representing a HPGe energy spectrum."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, cast

import pandas as pd
from pandas import DataFrame, Series, read_csv

if TYPE_CHECKING:
    from numpy import ndarray
    from path import Path
    from streamlit.runtime.uploaded_file_manager import UploadedFile

pd.options.plotting.backend = "plotly"
log = logging.getLogger(__name__)




class Spectrum:
    """An energy spectrum measured with an HPGe."""

    HEADER_LENGTH = 52  # lines

    def __init__(self, data: Series):
        """Initialize self."""
        self._data: Series = data
        self._slope: float | None = None
        self._origin: float = 0.0
        self._peaks: ndarray | None = None

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f"{self.__class__.__name__}({self._data})"

    def __str__(self) -> str:
        """Return str(self)."""
        return (
            f"{self.__class__.__name__}:\n"
            f"Energy scale: {self._slope} keV/bin x val + {self._origin}\n"
            f"{self._data}"
        )

    @property
    def data(self) -> Series:
        """Return the internal data."""
        return self._data

    @classmethod
    def from_file(cls, file: Path | UploadedFile) -> Spectrum:
        """Initialize the spectrum from a file."""
        log.info(f"Creating a Spectrum from: {file.name}")

        # First search for the live time in order to rescale the Y axis
        # An UploadedFile is a generator, once consumed it is impossible to re-read it
        # So we begin by reading the comment lines on the top, then we read the data
        live_time = 1.0
        try:
            stream = open(file, "rb") if isinstance(file, str) else file  # noqa: SIM115
            n = 0
            for binary_line in stream:
                n += 1
                line = binary_line.decode()
                if line.startswith("Live Time:"):
                    live_time = float(line.split(":")[1])
                    log.info(f"Live time: {live_time}")
                    break
            content: DataFrame = read_csv(
                stream, sep=r"\s+", skiprows=cls.HEADER_LENGTH - n, header=None
            )
        finally:
            # noinspection  PyUnboundLocalVariable
            stream.close()

        spectrum = content.drop(0, axis="columns").stack().reset_index(drop=True)
        spectrum = cast(Series, spectrum)
        spectrum.name = "spectrum"
        return cls(spectrum / live_time)

    def __sub__(self, other: Spectrum) -> Spectrum:
        """Subtract other from self, keeping self index."""
        spectrum = Spectrum(self.data - other.data.to_numpy())
        spectrum._slope = self._slope
        spectrum._origin = self._origin
        return spectrum


    def reset_energy_scale(self) -> None:
        """Reset the energy scale, showing the spectrum in bins."""
        self._data = self._data.reset_index(drop=True)
        self._slope = None
        self._origin = 0.0


