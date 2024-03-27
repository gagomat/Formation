from pandas import Series

from spectrum import Spectrum


def test_spectrum_initialization():
    data = Series([1, 2, 3, 4, 5])
    spectrum = Spectrum(data)
    assert spectrum.data.equals(data)

# Test the subtraction operation between two Spectrum instances
def test_spectrum_subtraction():
    data1 = Series([1, 2, 3, 4, 5])
    data2 = Series([0.5, 1.5, 2.5, 3.5, 4.5])
    spectrum1 = Spectrum(data1)
    spectrum2 = Spectrum(data2)
    result = spectrum1 - spectrum2
    expected_result = Series([0.5, 0.5, 0.5, 0.5, 0.5])
    assert result.data.equals(expected_result)

# Test the reset_energy_scale method
def test_reset_energy_scale():
    data = Series([1, 2, 3, 4, 5])
    spectrum = Spectrum(data)
    spectrum.reset_energy_scale()
    assert spectrum._slope is None
    assert spectrum._origin == 0.0