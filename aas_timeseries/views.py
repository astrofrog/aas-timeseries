import uuid
from aas_timeseries.data import Data
from aas_timeseries.marks import BaseMark, Symbol, Line, VerticalLine, VerticalRange, HorizontalLine, HorizontalRange, Range, Text


class BaseView:
    """
    Base class for view-like objects (both the base figure and the actual views)
    """

    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self._data = {}
        self._markers = {}
        self._xlim = None
        self._ylim = None

    @property
    def xlim(self):
        return self._xlim

    @xlim.setter
    def xlim(self, range):
        self._xlim = range

    @property
    def ylim(self):
        return self._ylim

    @ylim.setter
    def ylim(self, range):
        self._ylim = range

    def add_markers(self, *, time_series=None, column=None, **kwargs):
        """
        Add markers, optionally with errorbars, to the figure.

        Parameters
        ----------
        data : `~astropy_timeseries.TimeSeries`
            The time series object containing the data.
        column : str
            The field in the time series containing the data.
        error : str, optional
            The field in the time series containing the data uncertainties.
        shape : {'circle', 'square', 'cross', 'diamond', 'triangle-up', 'triangle-down', 'triangle-right', 'triangle-left'}, optional
            The symbol shape.
        size : float or int, optional
            The area in pixels of the bounding box of the symbols.  Note that this
            value sets the area of the symbol; the side lengths will increase with
            the square root of this value.
        color : str or tuple, optional
            The fill color of the symbols.
        opacity : float or int, optional
            The opacity of the fill color from 0 (transparent) to 1 (opaque).
        edge_color : str or tuple, optional
            The edge color of the symbol.
        edge_opacity : float or int, optional
            The opacity of the edge color from 0 (transparent) to 1 (opaque).
        edge_width : float or int, optional
            The thickness of the edge, in pixels.
        label : str, optional
            The label to use to designate the marks in the legend.

        Returns
        -------
        layer : `~aas_timeseries.marks.Symbol`
        """
        if id(time_series) not in self._data:
            self._data[id(time_series)] = Data(time_series)
        markers = Symbol(data=self._data[id(time_series)], **kwargs)
        # Note that we need to set the column after the data so that the
        # validation works.
        markers.column = column
        self._markers[markers] = {'visible': True}
        return markers

    def add_line(self, *, time_series=None, column=None, **kwargs):
        """
        Add a line to the figure.

        Parameters
        ----------
        data : `~astropy_timeseries.TimeSeries`
            The time series object containing the data.
        column : str
            The field in the time series containing the data.
        width : float or int, optional
            The width of the line, in pixels.
        color : str or tuple, optional
            The color of the line.
        opacity : float or int, optional
            The opacity of the line from 0 (transparent) to 1 (opaque).
        label : str, optional
            The label to use to designate the marks in the legend.

        Returns
        -------
        layer : `~aas_timeseries.marks.Line`
        """

        if id(time_series) not in self._data:
            self._data[id(time_series)] = Data(time_series)
        line = Line(data=self._data[id(time_series)], **kwargs)
        # Note that we need to set the column after the data so that the
        # validation works.
        line.column = column
        self._markers[line] = {'visible': True}
        return line

    def add_range(self, *, time_series=None, column_lower=None, column_upper=None, **kwargs):
        """
        Add a time dependent range to the figure.

        Parameters
        ----------
        data : `~astropy_timeseries.TimeSeries`
            The time series object containing the data.
        column_lower : str
            The field in the time series containing the lower value of the data
            range.
        column_upper : str
            The field in the time series containing the upper value of the data
            range.
        color : str or tuple, optional
            The fill color of the range.
        opacity : float or int, optional
            The opacity of the fill color from 0 (transparent) to 1 (opaque).
        edge_color : str or tuple, optional
            The edge color of the range.
        edge_opacity : float or int, optional
            The opacity of the edge color from 0 (transparent) to 1 (opaque).
        edge_width : float or int, optional
            The thickness of the edge, in pixels.
        label : str, optional
            The label to use to designate the marks in the legend.

        Returns
        -------
        layer : `~aas_timeseries.marks.Range`
        """
        if id(time_series) not in self._data:
            self._data[id(time_series)] = Data(time_series)
        range = Range(data=self._data[id(time_series)], **kwargs)
        # Note that we need to set the columns after the data so that the
        # validation works.
        range.column_lower = column_lower
        range.column_upper = column_upper
        self._markers[range] = {'visible': True}
        return range

    def add_vertical_line(self, time, **kwargs):
        """
        Add a vertical line to the figure.

        Parameters
        ----------
        time : `~astropy.time.Time`
            The date/time at which the vertical line is shown.
        width : float or int, optional
            The width of the line, in pixels.
        color : str or tuple, optional
            The color of the line.
        opacity : float or int, optional
            The opacity of the line from 0 (transparent) to 1 (opaque).
        label : str, optional
            The label to use to designate the marks in the legend.

        Returns
        -------
        layer : `~aas_timeseries.marks.VerticalLine`
        """
        line = VerticalLine(time=time, **kwargs)
        self._markers[line] = {'visible': True}
        return line

    def add_vertical_range(self, time_lower, time_upper, **kwargs):
        """
        Add a vertical range to the figure.

        Parameters
        ----------
        time_lower : `~astropy.time.Time`
            The date/time at which the range starts.
        time_upper : `~astropy.time.Time`
            The date/time at which the range ends.
        color : str or tuple, optional
            The fill color of the range.
        opacity : float or int, optional
            The opacity of the fill color from 0 (transparent) to 1 (opaque).
        edge_color : str or tuple, optional
            The edge color of the range.
        edge_opacity : float or int, optional
            The opacity of the edge color from 0 (transparent) to 1 (opaque).
        edge_width : float or int, optional
            The thickness of the edge, in pixels.
        label : str, optional
            The label to use to designate the marks in the legend.

        Returns
        -------
        layer : `~aas_timeseries.marks.VerticalRange`
        """
        range = VerticalRange(time_lower=time_lower, time_upper=time_upper, **kwargs)
        self._markers[range] = {'visible': True}
        return range

    def add_horizontal_line(self, value, **kwargs):
        """
        Add a horizontal line to the figure.

        Parameters
        ----------
        value : float or int
            The y value at which the horizontal line is shown.
        width : float or int, optional
            The width of the line, in pixels.
        color : str or tuple, optional
            The color of the line.
        opacity : float or int, optional
            The opacity of the line from 0 (transparent) to 1 (opaque).
        label : str, optional
            The label to use to designate the marks in the legend.

        Returns
        -------
        layer : `~aas_timeseries.marks.HorizontalLine`
        """
        line = HorizontalLine(value=value, **kwargs)
        self._markers[line] = {'visible': True}
        return line

    def add_horizontal_range(self, value_lower, value_upper, **kwargs):
        """
        Add a horizontal range to the figure.

        Parameters
        ----------
        value_lower : float or int
            The value at which the range starts.
        value_upper : float or int
            The value at which the range ends.
        color : str or tuple, optional
            The fill color of the range.
        opacity : float or int, optional
            The opacity of the fill color from 0 (transparent) to 1 (opaque).
        edge_color : str or tuple, optional
            The edge color of the range.
        edge_opacity : float or int, optional
            The opacity of the edge color from 0 (transparent) to 1 (opaque).
        edge_width : float or int, optional
            The thickness of the edge, in pixels.
        label : str, optional
            The label to use to designate the marks in the legend.

        Returns
        -------
        layer : `~aas_timeseries.marks.HorizontalRange`
        """
        range = HorizontalRange(value_lower=value_lower, value_upper=value_upper, **kwargs)
        self._markers[range] = {'visible': True}
        return range

    def add_text(self, **kwargs):
        """
        Add a text label to the figure.

        Parameters
        ----------
        time : `~astropy.time.Time`
            The date/time at which the text is shown.
        value : float or int
            The y value at which the text is shown.
        weight : {'normal', 'bold'}, optional
            The weight of the text.
        baseline : {'alphabetic', 'top', 'middle', 'bottom'}, optional
            The vertical text baseline.
        align : {'left', 'center', 'right'}, optional
            The horizontal text alignment.
        angle : float or int, optional
            The rotation angle of the text in degrees (default 0).
        text : str, optional
            The text label to show.
        color : str or tuple, optional
            The color of the text.
        opacity : float or int, optional
            The opacity of the text from 0 (transparent) to 1 (opaque).
        label : str, optional
            The label to use to designate the marks in the legend.

        Returns
        -------
        layer : `~aas_timeseries.marks.Text`
        """
        text = Text(**kwargs)
        self._markers[text] = {'visible': True}
        return text


class View(BaseView):

    def __init__(self, inherited_marks=None):
        super().__init__()
        self._inherited_marks = inherited_marks or []

    def show(self, layers):
        self._set_visible(layers, True)

    def hide(self, layers):
        self._set_visible(layers, False)

    def _set_visible(self, layers, visible):
        if isinstance(layers, BaseMark):
            layers = [layers]
        for layer in layers:
            if layer in self._markers:
                self._markers[layer]['visible'] = visible
            else:
                raise ValueError(f'Layer {layer} no in view')