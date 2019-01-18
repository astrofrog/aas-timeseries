from astropy import units as u
from astropy_timeseries import TimeSeries

from aas_timeseries.visualization import InteractiveTimeSeriesFigure


def test_basic(tmpdir):

    ts = TimeSeries(time='2016-03-22T12:30:31', time_delta=3 * u.s, n_samples=5)
    ts['flux'] = [1, 2, 3, 4, 5]
    ts['error'] = [1, 2, 3, 4, 5]

    filename = tmpdir.join('figure.json').strpath

    figure = InteractiveTimeSeriesFigure()
    figure.add_markers(time_series=ts, column='flux', label='Markers')
    figure.add_line(time_series=ts, column='flux', label='Line')
    figure.add_markers(time_series=ts, column='flux', error='error', label='Markers with Errors')
    figure.add_vertical_line(ts.time[3], label='Vertical Line')
    figure.add_vertical_range(ts.time[0], ts.time[-1], label='Vertical Range')
    figure.save_interactive(filename)
