'''
Graph
======

The :class:`Graph` widget is a widget for displaying plots. It supports
drawing multiple plot with different colors on the Graph. It also supports
axes titles, ticks, labeled ticks, grids and a log or linear representation on
both the x and y axis, independently.

To display a plot. First create a graph which will function as a "canvas" for
the plots. Then create plot objects e.g. MeshLinePlot and add them to the
graph.

To create a graph with x-axis between 0-100, y-axis between -1 to 1, x and y
labels of and X and Y, respectively, x major and minor ticks every 25, 5 units,
respectively, y major ticks every 1 units, full x and y grids and with
a red line plot containing a sin wave on this range::

    from kivy.garden.graph import Graph, MeshLinePlot
    graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                  x_ticks_major=25, y_ticks_major=1,
                  y_grid_label=True, x_grid_label=True, padding=5,
                  x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
    plot = MeshLinePlot(color=[1, 0, 0, 1])
    plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
    graph.add_plot(plot)

The MeshLinePlot plot is a particular plot which draws a set of points using
a mesh object. The points are given as a list of tuples, with each tuple
being a (x, y) coordinate in the graph's units.

You can create different types of plots other than MeshLinePlot by inheriting
from the Plot class and implementing the required functions. The Graph object
provides a "canvas" to which a Plot's instructions are added. The plot object
is responsible for updating these instructions to show within the bounding
box of the graph the proper plot. The Graph notifies the Plot when it needs
to be redrawn due to changes. See the MeshLinePlot class for how it is done.

The current availables plots are:

    * `MeshStemPlot`
    * `MeshLinePlot`
    * `SmoothLinePlot` - require Kivy 1.8.1
    * `ContourPlot`
    * `BarPlot`
    * `DotPlot`

.. note::

    The graph uses a stencil view to clip the plots to the graph display area.
    As with the stencil graphics instructions, you cannot stack more than 8
    stencil-aware widgets.

'''

__all__ = ('Graph', 'Plot', 'MeshLinePlot', 'MeshStemPlot', 'LinePlot', 'SmoothLinePlot', 'ContourPlot', 'BarPlot', 'DotPlot')
__version__ = '0.4.1-dev'

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stencilview import StencilView
from kivy.properties import NumericProperty, BooleanProperty,\
    BoundedNumericProperty, StringProperty, ListProperty, ObjectProperty,\
    DictProperty, AliasProperty, OptionProperty
from kivy.clock import Clock
from kivy.graphics import Mesh, Color, Rectangle, Point, RoundedRectangle
from kivy.graphics import Fbo
from kivy.graphics.texture import Texture
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.logger import Logger
from kivy import metrics
from math import log10, floor, ceil
from decimal import Decimal
try:
    import numpy as np
except ImportError as e:
    np = None


def identity(x):
    return x


def exp10(x):
    return 10 ** x


Builder.load_string("""
<GraphRotatedLabel>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0, 0, 1
            origin: root.center
    canvas.after:
        PopMatrix
""")


class GraphRotatedLabel(Label):
    angle = NumericProperty(0)


class Axis(EventDispatcher):
    pass


class XAxis(Axis):
    pass


class YAxis(Axis):
    pass


class Graph(Widget):
    '''Graph class, see module documentation for more information.
    '''

    # triggers a full reload of graphics
    _trigger = ObjectProperty(None)
    # triggers only a repositioning of objects due to size/pos updates
    _trigger_size = ObjectProperty(None)
    # triggers only a update of colors, e.g. tick_color
    _trigger_color = ObjectProperty(None)
    # triggers only a redraw of legend.
    _trigger_legend = ObjectProperty(None)
    # holds widget with the main title label
    _title = ObjectProperty(None)
    # holds widget with the x-axis label
    _xlabel = ObjectProperty(None)
    # holds widget with the y-axis label
    _ylabel = ObjectProperty(None)
    # holds widget with the legend
    _legend = ObjectProperty(None)
    # holds all the x-axis tick mark labels
    _x_grid_label = ListProperty([])
    # holds all the y-axis tick mark labels
    _y_grid_label = ListProperty([])
    # the mesh drawing all the ticks/grids
    _mesh_ticks = ObjectProperty(None)
    # the mesh which draws the surrounding rectangle
    _mesh_rect = ObjectProperty(None)
    # a list of locations of major and minor ticks. The values are not
    # but is in the axis min - max range
    _ticks_majorx = ListProperty([])
    _ticks_minorx = ListProperty([])
    _ticks_majory = ListProperty([])
    _ticks_minory = ListProperty([])

    tick_color = ListProperty([.25, .25, .25, 1])
    '''Color of the grid/ticks, default to 1/4. grey.
    '''

    background_color = ListProperty([0, 0, 0, 0])
    '''Color of the background, defaults to transparent
    '''

    border_color = ListProperty([1, 1, 1, 1])
    '''Color of the border, defaults to white
    '''

    label_options = DictProperty()
    '''Label options that will be passed to `:class:`kivy.uix.Label`.
    '''

    _with_stencilbuffer = BooleanProperty(True)
    '''Whether :class:`Graph`'s FBO should use FrameBuffer (True) or not (False).

    .. warning:: This property is internal and so should be used with care. It can break
    some other graphic instructions used by the :class:`Graph`, for example you can have
    problems when drawing :class:`SmoothLinePlot` plots, so use it only when you know
    what exactly you are doing.

    :data:`_with_stencilbuffer` is a :class:`~kivy.properties.BooleanProperty`, defaults
    to True.
    '''

    def __init__(self, **kwargs):
        super(Graph, self).__init__(**kwargs)

        with self.canvas:
            self._fbo = Fbo(size=self.size, with_stencilbuffer=self._with_stencilbuffer)

        with self._fbo:
            self._background_color = Color(*self.background_color)
            self._background_rect = Rectangle(size=self.size)
            self._mesh_ticks_color = Color(*self.tick_color)
            self._mesh_ticks = Mesh(mode='lines')
            self._mesh_rect_color = Color(*self.border_color)
            self._mesh_rect = Mesh(mode='line_strip')

        with self.canvas:
            Color(1, 1, 1)
            self._fbo_rect = Rectangle(size=self.size, texture=self._fbo.texture)

        mesh = self._mesh_rect
        mesh.vertices = [0] * (5 * 4)
        mesh.indices = range(5)

        self._plot_area = StencilView()
        self.add_widget(self._plot_area)

        t = self._trigger = Clock.create_trigger(self._redraw_all)
        ts = self._trigger_size = Clock.create_trigger(self._redraw_size)
        tc = self._trigger_color = Clock.create_trigger(self._update_colors)
        tl = self._trigger_legend = Clock.create_trigger(self._redraw_legend)

        self.bind(plots=tl)
        self.bind(center=ts, padding=ts, precision=ts, plots=ts, x_grid=ts,
                  y_grid=ts, draw_border=ts)
        self.bind(xmin=t, xmax=t, xlog=t, x_ticks_major=t, x_ticks_minor=t,
                  xlabel=t, x_grid_label=t, ymin=t, ymax=t, ylog=t,
                  y_ticks_major=t, y_ticks_minor=t, ylabel=t, y_grid_label=t,
                  font_size=t, label_options=t, x_ticks_angle=t, title=t,
                  legend=t, legend_pos=t)
        self.bind(tick_color=tc, background_color=tc, border_color=tc)
        self._trigger()

    def add_widget(self, widget):
        if widget is self._plot_area:
            canvas = self.canvas
            self.canvas = self._fbo
        super(Graph, self).add_widget(widget)
        if widget is self._plot_area:
            self.canvas = canvas

    def remove_widget(self, widget):
        if widget is self._plot_area:
            canvas = self.canvas
            self.canvas = self._fbo
        super(Graph, self).remove_widget(widget)
        if widget is self._plot_area:
            self.canvas = canvas

    def _get_ticks(self, major, minor, log, s_min, s_max):
        if major and s_max > s_min:
            if log:
                s_min = log10(s_min)
                s_max = log10(s_max)
                # count the decades in min - max. This is in actual decades,
                # not logs.
                n_decades = floor(s_max - s_min)
                # for the fractional part of the last decade, we need to
                # convert the log value, x, to 10**x but need to handle
                # differently if the last incomplete decade has a decade
                # boundary in it
                if floor(s_min + n_decades) != floor(s_max):
                    n_decades += 1 - (10 ** (s_min + n_decades + 1) - 10 **
                                      s_max) / 10 ** floor(s_max + 1)
                else:
                    n_decades += ((10 ** s_max - 10 ** (s_min + n_decades)) /
                                  10 ** floor(s_max + 1))
                # this might be larger than what is needed, but we delete
                # excess later
                n_ticks_major = n_decades / float(major)
                n_ticks = int(floor(n_ticks_major * (minor if minor >=
                                                     1. else 1.0))) + 2
                # in decade multiples, e.g. 0.1 of the decade, the distance
                # between ticks
                decade_dist = major / float(minor if minor else 1.0)

                points_minor = [0] * n_ticks
                points_major = [0] * n_ticks
                k = 0  # position in points major
                k2 = 0  # position in points minor
                # because each decade is missing 0.1 of the decade, if a tick
                # falls in < min_pos skip it
                min_pos = 0.1 - 0.00001 * decade_dist
                s_min_low = floor(s_min)
                # first real tick location. value is in fractions of decades
                # from the start we have to use decimals here, otherwise
                # floating point inaccuracies results in bad values
                start_dec = ceil((10 ** Decimal(s_min - s_min_low - 1)) /
                                 Decimal(decade_dist)) * decade_dist
                count_min = (0 if not minor else
                             floor(start_dec / decade_dist) % minor)
                start_dec += s_min_low
                count = 0  # number of ticks we currently have passed start
                while True:
                    # this is the current position in decade that we are.
                    # e.g. -0.9 means that we're at 0.1 of the 10**ceil(-0.9)
                    # decade
                    pos_dec = start_dec + decade_dist * count
                    pos_dec_low = floor(pos_dec)
                    diff = pos_dec - pos_dec_low
                    zero = abs(diff) < 0.001 * decade_dist
                    if zero:
                        # the same value as pos_dec but in log scale
                        pos_log = pos_dec_low
                    else:
                        pos_log = log10((pos_dec - pos_dec_low
                                         ) * 10 ** ceil(pos_dec))
                    if pos_log > s_max:
                        break
                    count += 1
                    if zero or diff >= min_pos:
                        if minor and not count_min % minor:
                            points_major[k] = pos_log
                            k += 1
                        else:
                            points_minor[k2] = pos_log
                            k2 += 1
                    count_min += 1
            else:
                # distance between each tick
                tick_dist = major / float(minor if minor else 1.0)
                min = s_min
                if s_max > 0 and s_min < 0:
                    min = floor(s_min / major) * major
                n_ticks = int(floor((s_max - min) / tick_dist) + 1)
                points_major = [0] * int(floor((s_max - min) / float(major))
                                         + 1)
                points_minor = [0] * (n_ticks - len(points_major) + 1)
                k = 0  # position in points major
                k2 = 0  # position in points minor
                for m in range(0, n_ticks):
                    pt = m * tick_dist + min
                    if pt < s_min:
                        continue
                    if minor and m % minor:
                        points_minor[k2] = pt
                        k2 += 1
                    else:
                        points_major[k] = pt
                        k += 1
            del points_major[k:]
            del points_minor[k2:]
        else:
            points_major = []
            points_minor = []
        return points_major, points_minor

    def _update_labels(self):
        xlabel = self._xlabel
        ylabel = self._ylabel
        title = self._title
        x = self.x
        y = self.y
        width = self.width
        height = self.height
        padding = self.padding
        x_next = padding + x
        y_next = padding + y
        xextent = width + x
        yextent = height + y - padding
        ymin = self.ymin
        ymax = self.ymax
        xmin = self.xmin
        precision = self.precision
        x_overlap = False
        y_overlap = False
        # set up title label
        if title:
            title.text = self.title
            title.texture_update()
            title.size = title.texture_size
            title.top = int(yextent) 
            title.x = int(x + width / 2. - title.width / 2.)
        # set up x and y axis labels
        if xlabel:
            xlabel.text = self.xlabel
            xlabel.texture_update()
            xlabel.size = xlabel.texture_size
            xlabel.pos = int(x + width / 2. - xlabel.width / 2.), int(padding + y)
            y_next += padding + xlabel.height
        if ylabel:
            ylabel.text = self.ylabel
            ylabel.texture_update()
            ylabel.size = ylabel.texture_size
            ylabel.x = padding + x - (ylabel.width / 2. - ylabel.height / 2.)
            x_next += padding + ylabel.height
        xpoints = self._ticks_majorx
        xlabels = self._x_grid_label
        xlabel_grid = self.x_grid_label
        ylabel_grid = self.y_grid_label
        ypoints = self._ticks_majory
        ylabels = self._y_grid_label
        # now x and y tick mark labels
        if len(ylabels) and ylabel_grid:
            # horizontal size of the largest tick label, to have enough room
            funcexp = exp10 if self.ylog else identity
            funclog = log10 if self.ylog else identity
            ylabels[0].text = precision % funcexp(ypoints[0])
            ylabels[0].texture_update()
            y1 = ylabels[0].texture_size
            y_start = y_next + (padding + y1[1] if len(xlabels) and xlabel_grid
                                else 0) + \
                               (padding + y1[1] if not y_next else 0)
            if title:
                yextent +=  - title.size[1] - padding
            else:
                yextent += - y1[1] / 2.
            ymin = funclog(ymin)
            ratio = (yextent - y_start) / float(funclog(ymax) - ymin)
            y_start -= y1[1] / 2.
            y1 = y1[0]
            for k in range(len(ylabels)):
                ylabels[k].text = precision % funcexp(ypoints[k])
                ylabels[k].texture_update()
                ylabels[k].size = ylabels[k].texture_size
                y1 = max(y1, ylabels[k].texture_size[0])
                ylabels[k].pos = (
                    int(x_next),
                    int(y_start + (ypoints[k] - ymin) * ratio))
            if len(ylabels) > 1 and ylabels[0].top > ylabels[1].y:
                y_overlap = True
            else:
                x_next += y1 + padding
        if len(xlabels) and xlabel_grid:
            funcexp = exp10 if self.xlog else identity
            funclog = log10 if self.xlog else identity
            # find the distance from the end that'll fit the last tick label
            xlabels[0].text = precision % funcexp(xpoints[-1])
            xlabels[0].texture_update()
            xextent = x + width - xlabels[0].texture_size[0] / 2. - padding
            # find the distance from the start that'll fit the first tick label
            if not x_next:
                xlabels[0].text = precision % funcexp(xpoints[0])
                xlabels[0].texture_update()
                x_next = padding + xlabels[0].texture_size[0] / 2.
            xmin = funclog(xmin)
            ratio = (xextent - x_next) / float(funclog(self.xmax) - xmin)
            right = -1
            for k in range(len(xlabels)):
                xlabels[k].text = precision % funcexp(xpoints[k])
                # update the size so we can center the labels on ticks
                xlabels[k].texture_update()
                xlabels[k].size = xlabels[k].texture_size
                half_ts = xlabels[k].texture_size[0] / 2.
                xlabels[k].pos = (
                    int(x_next + (xpoints[k] - xmin) * ratio - half_ts),
                    int(y_next))
                if xlabels[k].x < right:
                    x_overlap = True
                    break
                right = xlabels[k].right
            if not x_overlap:
                y_next += padding + xlabels[0].texture_size[1]
        # now re-center the title and the x and y axis labels
        if title:
            title.x = int(x_next + (xextent - x_next) / 2. - title.width / 2.)
        if xlabel:
            xlabel.x = int(x_next + (xextent - x_next) / 2. - xlabel.width / 2.)
        if ylabel:
            ylabel.y = int(y_next + (yextent - y_next) / 2. - ylabel.height / 2.)
            ylabel.angle = 90
        if x_overlap:
            for k in range(len(xlabels)):
                xlabels[k].text = ''
        if y_overlap:
            for k in range(len(ylabels)):
                ylabels[k].text = ''
        return x_next - x, y_next - y, xextent - x, yextent - y

    def _update_ticks(self, size):
        # re-compute the positions of the bounding rectangle
        mesh = self._mesh_rect
        vert = mesh.vertices
        if self.draw_border:
            s0, s1, s2, s3 = size
            vert[0] = s0
            vert[1] = s1
            vert[4] = s2
            vert[5] = s1
            vert[8] = s2
            vert[9] = s3
            vert[12] = s0
            vert[13] = s3
            vert[16] = s0
            vert[17] = s1
        else:
            vert[0:18] = [0 for k in range(18)]
        mesh.vertices = vert
        # re-compute the positions of the x/y axis ticks
        mesh = self._mesh_ticks
        vert = mesh.vertices
        start = 0
        xpoints = self._ticks_majorx
        ypoints = self._ticks_majory
        xpoints2 = self._ticks_minorx
        ypoints2 = self._ticks_minory
        ylog = self.ylog
        xlog = self.xlog
        xmin = self.xmin
        xmax = self.xmax
        if xlog:
            xmin = log10(xmin)
            xmax = log10(xmax)
        ymin = self.ymin
        ymax = self.ymax
        if ylog:
            ymin = log10(ymin)
            ymax = log10(ymax)
        if len(xpoints):
            top = size[3] if self.x_grid else metrics.dp(12) + size[1]
            ratio = (size[2] - size[0]) / float(xmax - xmin)
            for k in range(start, len(xpoints) + start):
                vert[k * 8] = size[0] + (xpoints[k - start] - xmin) * ratio
                vert[k * 8 + 1] = size[1]
                vert[k * 8 + 4] = vert[k * 8]
                vert[k * 8 + 5] = top
            start += len(xpoints)
        if len(xpoints2):
            top = metrics.dp(8) + size[1]
            ratio = (size[2] - size[0]) / float(xmax - xmin)
            for k in range(start, len(xpoints2) + start):
                vert[k * 8] = size[0] + (xpoints2[k - start] - xmin) * ratio
                vert[k * 8 + 1] = size[1]
                vert[k * 8 + 4] = vert[k * 8]
                vert[k * 8 + 5] = top
            start += len(xpoints2)
        if len(ypoints):
            top = size[2] if self.y_grid else metrics.dp(12) + size[0]
            ratio = (size[3] - size[1]) / float(ymax - ymin)
            for k in range(start, len(ypoints) + start):
                vert[k * 8 + 1] = size[1] + (ypoints[k - start] - ymin) * ratio
                vert[k * 8 + 5] = vert[k * 8 + 1]
                vert[k * 8] = size[0]
                vert[k * 8 + 4] = top
            start += len(ypoints)
        if len(ypoints2):
            top = metrics.dp(8) + size[0]
            ratio = (size[3] - size[1]) / float(ymax - ymin)
            for k in range(start, len(ypoints2) + start):
                vert[k * 8 + 1] = size[1] + (ypoints2[k - start] - ymin) * ratio
                vert[k * 8 + 5] = vert[k * 8 + 1]
                vert[k * 8] = size[0]
                vert[k * 8 + 4] = top
        mesh.vertices = vert

    x_axis = ListProperty([None])
    y_axis = ListProperty([None])

    def get_x_axis(self, axis=0):
        if axis == 0:
            return self.xlog, self.xmin, self.xmax
        info = self.x_axis[axis]
        return (info["log"], info["min"], info["max"])

    def get_y_axis(self, axis=0):
        if axis == 0:
            return self.ylog, self.ymin, self.ymax
        info = self.y_axis[axis]
        return (info["log"], info["min"], info["max"])

    def add_x_axis(self, xmin, xmax, xlog=False):
        data = {
            "log": xlog,
            "min": xmin,
            "max": xmax
        }
        self.x_axis.append(data)
        return data

    def add_y_axis(self, ymin, ymax, ylog=False):
        data = {
            "log": ylog,
            "min": ymin,
            "max": ymax
        }
        self.y_axis.append(data)
        return data

    def _update_plots(self, size):
        for plot in self.plots:
            xlog, xmin, xmax = self.get_x_axis(plot.x_axis)
            ylog, ymin, ymax = self.get_y_axis(plot.y_axis)
            plot._update(xlog, xmin, xmax, ylog, ymin, ymax, size)

    def _update_colors(self, *args):
        self._mesh_ticks_color.rgba = tuple(self.tick_color)
        self._background_color.rgba = tuple(self.background_color)
        self._mesh_rect_color.rgba = tuple(self.border_color)

    def _redraw_all(self, *args):
        # add/remove all the required labels
        xpoints_major, xpoints_minor = self._redraw_x(*args)
        ypoints_major, ypoints_minor = self._redraw_y(*args)
        self._redraw_title(*args)
        self._redraw_legend(*args)

        mesh = self._mesh_ticks
        n_points = (len(xpoints_major) + len(xpoints_minor) +
                    len(ypoints_major) + len(ypoints_minor))
        mesh.vertices = [0] * (n_points * 8)
        mesh.indices = [k for k in range(n_points * 2)]
        self._redraw_size()
    
    def _redraw_title(self, *arg):
        font_size = self.font_size
        if self.title:
            title = self._title
            if not title:
                title = Label(**self.label_options)
                self.add_widget(title)
                self._title = title

            title.font_size = font_size
            for k, v in self.label_options.items():
                setattr(title, k, v)
        else:
            title = self._title
            if title:
                self.remove_widget(title)
                self._title = None
    
    def _redraw_x(self, *args):
        font_size = self.font_size
        if self.xlabel:
            xlabel = self._xlabel
            if not xlabel:
                xlabel = Label()
                self.add_widget(xlabel)
                self._xlabel = xlabel

            xlabel.font_size = font_size
            for k, v in self.label_options.items():
                setattr(xlabel, k, v)

        else:
            xlabel = self._xlabel
            if xlabel:
                self.remove_widget(xlabel)
                self._xlabel = None
        grids = self._x_grid_label
        xpoints_major, xpoints_minor = self._get_ticks(self.x_ticks_major,
                                                       self.x_ticks_minor,
                                                       self.xlog, self.xmin,
                                                       self.xmax)
        self._ticks_majorx = xpoints_major
        self._ticks_minorx = xpoints_minor

        if not self.x_grid_label:
            n_labels = 0
        else:
            n_labels = len(xpoints_major)

        for k in range(n_labels, len(grids)):
            self.remove_widget(grids[k])
        del grids[n_labels:]

        grid_len = len(grids)
        grids.extend([None] * (n_labels - len(grids)))
        for k in range(grid_len, n_labels):
            grids[k] = GraphRotatedLabel(
                font_size=font_size, angle=self.x_ticks_angle,
                **self.label_options)
            self.add_widget(grids[k])
        for i in range(grid_len):
            for k, v in self.label_options.items():
                setattr(grids[i], k, v)
        return xpoints_major, xpoints_minor

    def _redraw_y(self, *args):
        font_size = self.font_size
        if self.ylabel:
            ylabel = self._ylabel
            if not ylabel:
                ylabel = GraphRotatedLabel()
                self.add_widget(ylabel)
                self._ylabel = ylabel

            ylabel.font_size = font_size
            for k, v in self.label_options.items():
                setattr(ylabel, k, v)
        else:
            ylabel = self._ylabel
            if ylabel:
                self.remove_widget(ylabel)
                self._ylabel = None
        grids = self._y_grid_label
        ypoints_major, ypoints_minor = self._get_ticks(self.y_ticks_major,
                                                       self.y_ticks_minor,
                                                       self.ylog, self.ymin,
                                                       self.ymax)
        self._ticks_majory = ypoints_major
        self._ticks_minory = ypoints_minor

        if not self.y_grid_label:
            n_labels = 0
        else:
            n_labels = len(ypoints_major)

        for k in range(n_labels, len(grids)):
            self.remove_widget(grids[k])
        del grids[n_labels:]

        grid_len = len(grids)
        grids.extend([None] * (n_labels - len(grids)))
        for k in range(grid_len, n_labels):
            grids[k] = Label(font_size=font_size, **self.label_options)
            self.add_widget(grids[k])
        for i in range(grid_len):
            for k, v in self.label_options.items():
                setattr(grids[i], k, v)
        return ypoints_major, ypoints_minor

    def _redraw_size(self, *args):
        # size a 4-tuple describing the bounding box in which we can draw
        # graphs, it's (x0, y0, x1, y1), which correspond with the bottom left
        # and top right corner locations, respectively
        self._clear_buffer()
        size = self._update_labels()
        self.view_pos = self._plot_area.pos = (size[0], size[1])
        self.view_size = self._plot_area.size = (
            size[2] - size[0], size[3] - size[1])

        if self.size[0] and self.size[1]:
            self._fbo.size = self.size
        else:
            self._fbo.size = 1, 1  # gl errors otherwise
        self._fbo_rect.texture = self._fbo.texture
        self._fbo_rect.size = self.size
        self._fbo_rect.pos = self.pos
        self._background_rect.size = self.size
        self._update_ticks(size)
        self._update_plots(size)
        if self.legend:
            self._update_legend(size)
    
    def _redraw_legend(self, *arg):
        font_size = self.font_size
        if self.legend:
            legend = self._legend
            if not legend:
                legend = LegendBox()
                self.add_widget(legend)
                self._legend = legend
            if legend not in self.children:
                self.add_widget(legend)
            
            legend.font_size = font_size
            legend.label_options = self.label_options
            legend.background_color = self.background_color
            
            legend.update_plots(self.plots)
                    
        else:
            legend = self._legend
            if legend:
                self.remove_widget(legend)
    
    def _update_legend(self, size):
        if self.legend:
            legend = self._legend
            if self.legend_pos == "top right":
                legend.right = self.x + size[2] - 5
                legend.top = self.y + size[3] - 5
            elif self.legend_pos == "bottom right":
                legend.right = self.x + size[2] - 5
                legend.y = self.y + size[1] + 5
            elif self.legend_pos == "bottom left":
                legend.x = self.x + size[0] + 5
                legend.y = self.y + size[1] + 5
            elif self.legend_pos == "top left":
                legend.x = self.x + size[0] + 5
                legend.top = self.y + size[3] - 5
            legend._redraw_all()

    def _clear_buffer(self, *largs):
        fbo = self._fbo
        fbo.bind()
        fbo.clear_buffer()
        fbo.release()

    def add_plot(self, plot):
        '''Add a new plot to this graph.

        :Parameters:
            `plot`:
                Plot to add to this graph.

        >>> graph = Graph()
        >>> plot = MeshLinePlot(mode='line_strip', color=[1, 0, 0, 1])
        >>> plot.points = [(x / 10., sin(x / 50.)) for x in range(-0, 101)]
        >>> graph.add_plot(plot)
        '''
        if plot in self.plots:
            return
        add = self._plot_area.canvas.add
        for instr in plot.get_drawings():
            add(instr)
        plot.bind(on_clear_plot=self._clear_buffer)
        self.plots.append(plot)

    def remove_plot(self, plot):
        '''Remove a plot from this graph.

        :Parameters:
            `plot`:
                Plot to remove from this graph.

        >>> graph = Graph()
        >>> plot = MeshLinePlot(mode='line_strip', color=[1, 0, 0, 1])
        >>> plot.points = [(x / 10., sin(x / 50.)) for x in range(-0, 101)]
        >>> graph.add_plot(plot)
        >>> graph.remove_plot(plot)
        '''
        if plot not in self.plots:
            return
        remove = self._plot_area.canvas.remove
        for instr in plot.get_drawings():
            remove(instr)
        plot.unbind(on_clear_plot=self._clear_buffer)
        self.plots.remove(plot)
        self._clear_buffer()

    def collide_plot(self, x, y):
        '''Determine if the given coordinates fall inside the plot area. Use
        `x, y = self.to_widget(x, y, relative=True)` to first convert into
        widget coordinates if it's in window coordinates because it's assumed
        to be given in local widget coordinates, relative to the graph's pos.

        :Parameters:
            `x, y`:
                The coordinates to test.
        '''
        adj_x, adj_y = x - self._plot_area.pos[0], y - self._plot_area.pos[1]
        return 0 <= adj_x <= self._plot_area.size[0] \
            and 0 <= adj_y <= self._plot_area.size[1]

    def to_data(self, x, y):
        '''Convert widget coords to data coords. Use
        `x, y = self.to_widget(x, y, relative=True)` to first convert into
        widget coordinates if it's in window coordinates because it's assumed
        to be given in local widget coordinates, relative to the graph's pos.

        :Parameters:
            `x, y`:
                The coordinates to convert.

        If the graph has multiple axes, use :class:`Plot.unproject` instead.
        '''
        adj_x = float(x - self._plot_area.pos[0])
        adj_y = float(y - self._plot_area.pos[1])
        norm_x = adj_x / self._plot_area.size[0]
        norm_y = adj_y / self._plot_area.size[1]
        if self.xlog:
            xmin, xmax = log10(self.xmin), log10(self.xmax)
            conv_x = 10.**(norm_x * (xmax - xmin) + xmin)
        else:
            conv_x = norm_x * (self.xmax - self.xmin) + self.xmin
        if self.ylog:
            ymin, ymax = log10(self.ymin), log10(self.ymax)
            conv_y = 10.**(norm_y * (ymax - ymin) + ymin)
        else:
            conv_y = norm_y * (self.ymax - self.ymin) + self.ymin
        return [conv_x, conv_y]
    
    def get_plot_area_size(self):
        return tuple(self._plot_area.size)
        

    xmin = NumericProperty(0.)
    '''The x-axis minimum value.

    If :data:`xlog` is True, xmin must be larger than zero.

    :data:`xmin` is a :class:`~kivy.properties.NumericProperty`, defaults to 0.
    '''

    xmax = NumericProperty(100.)
    '''The x-axis maximum value, larger than xmin.

    :data:`xmax` is a :class:`~kivy.properties.NumericProperty`, defaults to 0.
    '''

    xlog = BooleanProperty(False)
    '''Determines whether the x-axis should be displayed logarithmically (True)
    or linearly (False).

    :data:`xlog` is a :class:`~kivy.properties.BooleanProperty`, defaults
    to False.
    '''

    x_ticks_major = BoundedNumericProperty(0, min=0)
    '''Distance between major tick marks on the x-axis.

    Determines the distance between the major tick marks. Major tick marks
    start from min and re-occur at every ticks_major until :data:`xmax`.
    If :data:`xmax` doesn't overlap with a integer multiple of ticks_major,
    no tick will occur at :data:`xmax`. Zero indicates no tick marks.

    If :data:`xlog` is true, then this indicates the distance between ticks
    in multiples of current decade. E.g. if :data:`xmin` is 0.1 and
    ticks_major is 0.1, it means there will be a tick at every 10th of the
    decade, i.e. 0.1 ... 0.9, 1, 2... If it is 0.3, the ticks will occur at
    0.1, 0.3, 0.6, 0.9, 2, 5, 8, 10. You'll notice that it went from 8 to 10
    instead of to 20, that's so that we can say 0.5 and have ticks at every
    half decade, e.g. 0.1, 0.5, 1, 5, 10, 50... Similarly, if ticks_major is
    1.5, there will be ticks at 0.1, 5, 100, 5,000... Also notice, that there's
    always a major tick at the start. Finally, if e.g. :data:`xmin` is 0.6
    and this 0.5 there will be ticks at 0.6, 1, 5...

    :data:`x_ticks_major` is a
    :class:`~kivy.properties.BoundedNumericProperty`, defaults to 0.
    '''

    x_ticks_minor = BoundedNumericProperty(0, min=0)
    '''The number of sub-intervals that divide x_ticks_major.

    Determines the number of sub-intervals into which ticks_major is divided,
    if non-zero. The actual number of minor ticks between the major ticks is
    ticks_minor - 1. Only used if ticks_major is non-zero. If there's no major
    tick at xmax then the number of minor ticks after the last major
    tick will be however many ticks fit until xmax.

    If self.xlog is true, then this indicates the number of intervals the
    distance between major ticks is divided. The result is the number of
    multiples of decades between ticks. I.e. if ticks_minor is 10, then if
    ticks_major is 1, there will be ticks at 0.1, 0.2...0.9, 1, 2, 3... If
    ticks_major is 0.3, ticks will occur at 0.1, 0.12, 0.15, 0.18... Finally,
    as is common, if ticks major is 1, and ticks minor is 5, there will be
    ticks at 0.1, 0.2, 0.4... 0.8, 1, 2...

    :data:`x_ticks_minor` is a
    :class:`~kivy.properties.BoundedNumericProperty`, defaults to 0.
    '''

    x_grid = BooleanProperty(False)
    '''Determines whether the x-axis has tick marks or a full grid.

    If :data:`x_ticks_major` is non-zero, then if x_grid is False tick marks
    will be displayed at every major tick. If x_grid is True, instead of ticks,
    a vertical line will be displayed at every major tick.

    :data:`x_grid` is a :class:`~kivy.properties.BooleanProperty`, defaults
    to False.
    '''

    x_grid_label = BooleanProperty(False)
    '''Whether labels should be displayed beneath each major tick. If true,
    each major tick will have a label containing the axis value.

    :data:`x_grid_label` is a :class:`~kivy.properties.BooleanProperty`,
    defaults to False.
    '''

    xlabel = StringProperty('')
    '''The label for the x-axis. If not empty it is displayed in the center of
    the axis.

    :data:`xlabel` is a :class:`~kivy.properties.StringProperty`,
    defaults to ''.
    '''

    ymin = NumericProperty(0.)
    '''The y-axis minimum value.

    If :data:`ylog` is True, ymin must be larger than zero.

    :data:`ymin` is a :class:`~kivy.properties.NumericProperty`, defaults to 0.
    '''

    ymax = NumericProperty(100.)
    '''The y-axis maximum value, larger than ymin.

    :data:`ymax` is a :class:`~kivy.properties.NumericProperty`, defaults to 0.
    '''

    ylog = BooleanProperty(False)
    '''Determines whether the y-axis should be displayed logarithmically (True)
    or linearly (False).

    :data:`ylog` is a :class:`~kivy.properties.BooleanProperty`, defaults
    to False.
    '''

    y_ticks_major = BoundedNumericProperty(0, min=0)
    '''Distance between major tick marks. See :data:`x_ticks_major`.

    :data:`y_ticks_major` is a
    :class:`~kivy.properties.BoundedNumericProperty`, defaults to 0.
    '''

    y_ticks_minor = BoundedNumericProperty(0, min=0)
    '''The number of sub-intervals that divide ticks_major.
    See :data:`x_ticks_minor`.

    :data:`y_ticks_minor` is a
    :class:`~kivy.properties.BoundedNumericProperty`, defaults to 0.
    '''

    y_grid = BooleanProperty(False)
    '''Determines whether the y-axis has tick marks or a full grid. See
    :data:`x_grid`.

    :data:`y_grid` is a :class:`~kivy.properties.BooleanProperty`, defaults
    to False.
    '''

    y_grid_label = BooleanProperty(False)
    '''Whether labels should be displayed beneath each major tick. If true,
    each major tick will have a label containing the axis value.

    :data:`y_grid_label` is a :class:`~kivy.properties.BooleanProperty`,
    defaults to False.
    '''

    ylabel = StringProperty('')
    '''The label for the y-axis. If not empty it is displayed in the center of
    the axis.

    :data:`ylabel` is a :class:`~kivy.properties.StringProperty`,
    defaults to ''.
    '''

    padding = NumericProperty('5dp')
    '''Padding distances between the labels, axes titles and graph, as
    well between the widget and the objects near the boundaries.

    :data:`padding` is a :class:`~kivy.properties.NumericProperty`, defaults
    to 5dp.
    '''

    font_size = NumericProperty('15sp')
    '''Font size of the labels.

    :data:`font_size` is a :class:`~kivy.properties.NumericProperty`, defaults
    to 15sp.
    '''

    x_ticks_angle = NumericProperty(0)
    '''Rotate angle of the x-axis tick marks.

    :data:`x_ticks_angle` is a :class:`~kivy.properties.NumericProperty`,
    defaults to 0.
    '''

    precision = StringProperty('%g')
    '''Determines the numerical precision of the tick mark labels. This value
    governs how the numbers are converted into string representation. Accepted
    values are those listed in Python's manual in the
    "String Formatting Operations" section.

    :data:`precision` is a :class:`~kivy.properties.StringProperty`, defaults
    to '%g'.
    '''

    draw_border = BooleanProperty(True)
    '''Whether a border is drawn around the canvas of the graph where the
    plots are displayed.

    :data:`draw_border` is a :class:`~kivy.properties.BooleanProperty`,
    defaults to True.
    '''

    plots = ListProperty([])
    '''Holds a list of all the plots in the graph. To add and remove plots
    from the graph use :data:`add_plot` and :data:`add_plot`. Do not add
    directly edit this list.

    :data:`plots` is a :class:`~kivy.properties.ListProperty`,
    defaults to [].
    '''

    view_size = ObjectProperty((0, 0))
    '''The size of the graph viewing area - the area where the plots are
    displayed, excluding labels etc.
    '''

    view_pos = ObjectProperty((0, 0))
    '''The pos of the graph viewing area - the area where the plots are
    displayed, excluding labels etc. It is relative to the graph's pos.
    '''
    
    title = StringProperty('')
    '''The label for the title. If not empty it is displayed in the top of
    the graph.

    :data:`title` is a :class:`~kivy.properties.StringProperty`,
    defaults to ''.
    '''
    
    legend = BooleanProperty(False)
    '''Whether a legend is added.
    Don't forget to set the `label` property of the plot, otherwise no legend
    will be added for this plot.
    
    :data:`legend` is a :class:`~kivy.properties.BooleanProperty`,
    defaults to False.
    
    >>> graph = Graph()
    >>> plot = MeshLinePlot(mode='line_strip', color=[1, 0, 0, 1])
    >>> plot.points = [(x / 10., sin(x / 50.)) for x in range(-0, 101)]
    >>> plot.label = "sin plot"
    >>> graph.add_plot(plot)
    >>> graph.legend = True
    '''
    
    legend_pos = OptionProperty("top right", options=["top right", 
                                                      "bottom right", 
                                                      "bottom left", 
                                                      "top left"])
    '''The pos of the legend, relative to the graph viewing area.
    
    :data:`legend_pos` is a :class:`~kivy.properties.OptionProperty`,
    defaults to "top right".
    
    >>> graph = Graph()
    >>> plot = MeshLinePlot(mode='line_strip', color=[1, 0, 0, 1])
    >>> plot.points = [(x / 10., 200) for x in range(-0, 101)]
    >>> plot.label = "constant"
    >>> graph.add_plot(plot)
    >>> graph.legend = True
    >>> graph.legend_pos = "bottom left"
    '''

class Plot(EventDispatcher):
    '''Plot class, see module documentation for more information.

    :Events:
        `on_clear_plot`
            Fired before a plot updates the display and lets the fbo know that
            it should clear the old drawings.

    ..versionadded:: 0.4
    '''

    __events__ = ('on_clear_plot', )

    # most recent values of the params used to draw the plot
    params = DictProperty({'xlog': False, 'xmin': 0, 'xmax': 100,
                           'ylog': False, 'ymin': 0, 'ymax': 100,
                           'size': (0, 0, 0, 0)})

    color = ListProperty([1, 1, 1, 1])
    '''Color of the plot.
    
    :data:`color` is a :class:`~kivy.properties.ListProperty`, defaults to
    [1, 1, 1, 1].
    '''

    points = ListProperty([])
    '''List of (x, y) points to be displayed in the plot.

    The elements of points are 2-tuples, (x, y). The points are displayed
    based on the mode setting.

    :data:`points` is a :class:`~kivy.properties.ListProperty`, defaults to
    [].
    '''

    x_axis = NumericProperty(0)
    '''Index of the X axis to use, defaults to 0.
    
    :data:`x_axis` is a :class:`~kivy.properties.NumericProperty`, defaults to
    0.
    '''

    y_axis = NumericProperty(0)
    '''Index of the Y axis to use, defaults to 0
    
    :data:`y_axis` is a :class:`~kivy.properties.NumericProperty`, defaults to
    0.
    '''
    
    label = StringProperty('')
    '''Set the label for auto legend.
    if `label` is empty, no legend will be added for this plot.
    
    :data:`label` is a :class:`~kivy.properties.StringProperty`, defaults to
    ''.
    '''

    def __init__(self, **kwargs):
        super(Plot, self).__init__(**kwargs)
        self.ask_draw = Clock.create_trigger(self.draw)
        self.bind(params=self.ask_draw, points=self.ask_draw)
        self._drawings = self.create_drawings()

    def funcx(self):
        """Return a function that convert or not the X value according to plot
        prameters"""
        return log10 if self.params["xlog"] else lambda x: x

    def funcy(self):
        """Return a function that convert or not the Y value according to plot
        prameters"""
        return log10 if self.params["ylog"] else lambda y: y

    def x_px(self):
        """Return a function that convert the X value of the graph to the
        pixel coordinate on the plot, according to the plot settings and axis
        settings. It's relative to the graph pos.
        """
        funcx = self.funcx()
        params = self.params
        size = params["size"]
        xmin = funcx(params["xmin"])
        xmax = funcx(params["xmax"])
        ratiox = (size[2] - size[0]) / float(xmax - xmin)
        return lambda x: (funcx(x) - xmin) * ratiox + size[0]

    def y_px(self):
        """Return a function that convert the Y value of the graph to the
        pixel coordinate on the plot, according to the plot settings and axis
        settings. The returned value is relative to the graph pos.
        """
        funcy = self.funcy()
        params = self.params
        size = params["size"]
        ymin = funcy(params["ymin"])
        ymax = funcy(params["ymax"])
        ratioy = (size[3] - size[1]) / float(ymax - ymin)
        return lambda y: (funcy(y) - ymin) * ratioy + size[1]

    def unproject(self, x, y):
        """Return a function that unproject a pixel to a X/Y value on the plot
        (works only for linear, not log yet). `x`, `y`, is relative to the
        graph pos, so the graph's pos needs to be subtracted from x, y before
        passing it in.
        """
        params = self.params
        size = params["size"]
        xmin = params["xmin"]
        xmax = params["xmax"]
        ymin = params["ymin"]
        ymax = params["ymax"]
        ratiox = (size[2] - size[0]) / float(xmax - xmin)
        ratioy = (size[3] - size[1]) / float(ymax - ymin)
        x0 = (x - size[0]) / ratiox + xmin
        y0 = (y - size[1]) / ratioy + ymin
        return x0, y0

    def get_px_bounds(self):
        """Returns a dict containing the pixels bounds from the plot parameters.
         The returned values are relative to the graph pos.
        """
        params = self.params
        x_px = self.x_px()
        y_px = self.y_px()
        return {
            "xmin": x_px(params["xmin"]),
            "xmax": x_px(params["xmax"]),
            "ymin": y_px(params["ymin"]),
            "ymax": y_px(params["ymax"]),
        }

    def update(self, xlog, xmin, xmax, ylog, ymin, ymax, size):
        '''Called by graph whenever any of the parameters
        change. The plot should be recalculated then.
        log, min, max indicate the axis settings.
        size a 4-tuple describing the bounding box in which we can draw
        graphs, it's (x0, y0, x1, y1), which correspond with the bottom left
        and top right corner locations, respectively.
        '''
        self.params.update({
            'xlog': xlog, 'xmin': xmin, 'xmax': xmax, 'ylog': ylog,
            'ymin': ymin, 'ymax': ymax, 'size': size})

    def get_group(self):
        '''returns a string which is unique and is the group name given to all
        the instructions returned by _get_drawings. Graph uses this to remove
        these instructions when needed.
        '''
        return ''

    def get_drawings(self):
        '''returns a list of canvas instructions that will be added to the
        graph's canvas.
        '''
        if isinstance(self._drawings, (tuple, list)):
            return self._drawings
        return []

    def create_drawings(self):
        '''called once to create all the canvas instructions needed for the
        plot
        '''
        pass

    def draw(self, *largs):
        '''draw the plot according to the params. It dispatches on_clear_plot
        so derived classes should call super before updating.
        '''
        self.dispatch('on_clear_plot')

    def iterate_points(self):
        '''Iterate on all the points adjusted to the graph settings
        '''
        x_px = self.x_px()
        y_px = self.y_px()
        for x, y in self.points:
            yield x_px(x), y_px(y)

    def on_clear_plot(self, *largs):
        pass

    # compatibility layer
    _update = update
    _get_drawings = get_drawings
    _params = params


class DotPlot(Plot):
    '''DotPlot draw a set of points.
    '''
        
    def create_drawings(self):
        self._color = Color(*self.color)
        self._mesh = Point(points=(0, 0), pointsize=1)
        self.bind(color=lambda instr, value: setattr(self._color.rgba, value))
        return [self._color, self._mesh]

    def draw(self, *args):
        points = self.points
        mesh = self._mesh
        params = self._params
        funcx = log10 if params['xlog'] else identity
        funcy = log10 if params['ylog'] else identity
        xmin = funcx(params['xmin'])
        ymin = funcy(params['ymin'])
        size = params['size']
        ratiox = (size[2] - size[0]) / float(funcx(params['xmax']) - xmin)
        ratioy = (size[3] - size[1]) / float(funcy(params['ymax']) - ymin)
        mesh.points = ()
        for k in range(len(points)):
            x = (funcx(points[k][0]) - xmin) * ratiox + size[0]
            y = (funcy(points[k][1]) - ymin) * ratioy + size[1]
            mesh.add_point(x, y)

    def _set_pointsize(self, value):
        if hasattr(self, '_mesh'):
            self._mesh.pointsize = value
    point_size = AliasProperty(lambda self: self._mesh.pointsize, _set_pointsize)
    '''Set the point size.
    
    :data:`point_size` is a :class:`~kivy.properties.AliasProperty`, defaults 
    to 1.
    '''

    def _set_source(self, value):
        if hasattr(self, '_mesh'):
            self._mesh.source = value
    source = AliasProperty(lambda self: self._mesh.source, _set_source)

class MeshLinePlot(Plot):
    '''MeshLinePlot class which displays a set of points similar to a mesh.
    '''

    def _set_mode(self, value):
        if hasattr(self, '_mesh'):
            self._mesh.mode = value

    mode = AliasProperty(lambda self: self._mesh.mode, _set_mode)
    '''VBO Mode used for drawing the points. Can be one of: 'points',
    'line_strip', 'line_loop', 'lines', 'triangle_strip', 'triangle_fan'.
    See :class:`~kivy.graphics.Mesh` for more details.

    Defaults to 'line_strip'.
    '''

    def create_drawings(self):
        self._color = Color(*self.color)
        self._mesh = Mesh(mode='line_strip')
        self.bind(color=lambda instr, value: setattr(self._color, "rgba", value))
        return [self._color, self._mesh]

    def draw(self, *args):
        super(MeshLinePlot, self).draw(*args)
        self.plot_mesh()

    def plot_mesh(self):
        points = [p for p in self.iterate_points()]
        mesh, vert, _ = self.set_mesh_size(len(points))
        for k, (x, y) in enumerate(points):
            vert[k * 4] = x
            vert[k * 4 + 1] = y
        mesh.vertices = vert

    def set_mesh_size(self, size):
        mesh = self._mesh
        vert = mesh.vertices
        ind = mesh.indices
        diff = size - len(vert) // 4
        if diff < 0:
            del vert[4 * size:]
            del ind[size:]
        elif diff > 0:
            ind.extend(range(len(ind), len(ind) + diff))
            vert.extend([0] * (diff * 4))
        mesh.vertices = vert
        return mesh, vert, ind


class MeshStemPlot(MeshLinePlot):
    '''MeshStemPlot uses the MeshLinePlot class to draw a stem plot. The data
    provided is graphed from origin to the data point.
    '''

    def plot_mesh(self):
        points = [p for p in self.iterate_points()]
        mesh, vert, _ = self.set_mesh_size(len(points) * 2)
        y0 = self.y_px()(0)
        for k, (x, y) in enumerate(self.iterate_points()):
            vert[k * 8] = x
            vert[k * 8 + 1] = y0
            vert[k * 8 + 4] = x
            vert[k * 8 + 5] = y
        mesh.vertices = vert


class LinePlot(Plot):
    """LinePlot draws using a standard Line object.
    """

    line_width = NumericProperty(1)

    def create_drawings(self):
        from kivy.graphics import Line, RenderContext

        self._grc = RenderContext(
                use_parent_modelview=True,
                use_parent_projection=True)
        with self._grc:
            self._gcolor = Color(*self.color)
            self._gline = Line(
                points=[], cap='none',
                width=self.line_width, joint='round')

        return [self._grc]

    def draw(self, *args):
        super(LinePlot, self).draw(*args)
        # flatten the list
        points = []
        for x, y in self.iterate_points():
            points += [x, y]
        self._gline.points = points

    def on_line_width(self, *largs):
        if hasattr(self, "_gline"):
            self._gline.width = self.line_width


class SmoothLinePlot(Plot):
    '''Smooth Plot class, see module documentation for more information.
    This plot use a specific Fragment shader for a custom anti aliasing.
    '''
    
    line_width = NumericProperty(2.)
    
    SMOOTH_FS = '''
    $HEADER$

    void main(void) {
        float edgewidth = 0.015625 * 64.;
        float t = texture2D(texture0, tex_coord0).r;
        float e = smoothstep(0., edgewidth, t);
        gl_FragColor = frag_color * vec4(1, 1, 1, e);
    }
    '''

    # XXX This gradient data is a 64x1 RGB image, and
    # values goes from 0 -> 255 -> 0.
    GRADIENT_DATA = (
        b"\x00\x00\x00\x07\x07\x07\x0f\x0f\x0f\x17\x17\x17\x1f\x1f\x1f"
        b"'''///777???GGGOOOWWW___gggooowww\x7f\x7f\x7f\x87\x87\x87"
        b"\x8f\x8f\x8f\x97\x97\x97\x9f\x9f\x9f\xa7\xa7\xa7\xaf\xaf\xaf"
        b"\xb7\xb7\xb7\xbf\xbf\xbf\xc7\xc7\xc7\xcf\xcf\xcf\xd7\xd7\xd7"
        b"\xdf\xdf\xdf\xe7\xe7\xe7\xef\xef\xef\xf7\xf7\xf7\xff\xff\xff"
        b"\xf6\xf6\xf6\xee\xee\xee\xe6\xe6\xe6\xde\xde\xde\xd5\xd5\xd5"
        b"\xcd\xcd\xcd\xc5\xc5\xc5\xbd\xbd\xbd\xb4\xb4\xb4\xac\xac\xac"
        b"\xa4\xa4\xa4\x9c\x9c\x9c\x94\x94\x94\x8b\x8b\x8b\x83\x83\x83"
        b"{{{sssjjjbbbZZZRRRJJJAAA999111)))   \x18\x18\x18\x10\x10\x10"
        b"\x08\x08\x08\x00\x00\x00")

    def create_drawings(self):
        from kivy.graphics import Line, RenderContext

        # very first time, create a texture for the shader
        if not hasattr(SmoothLinePlot, '_texture'):
            tex = Texture.create(size=(1, 64), colorfmt='rgb')
            tex.add_reload_observer(SmoothLinePlot._smooth_reload_observer)
            SmoothLinePlot._texture = tex
            SmoothLinePlot._smooth_reload_observer(tex)

        self._grc = RenderContext(
            fs=SmoothLinePlot.SMOOTH_FS,
            use_parent_modelview=True,
            use_parent_projection=True)
        with self._grc:
            self._gcolor = Color(*self.color)
            self._gline = Line(
                points=[], cap='none', width=self.line_width,
                texture=SmoothLinePlot._texture)

        return [self._grc]

    @staticmethod
    def _smooth_reload_observer(texture):
        texture.blit_buffer(SmoothLinePlot.GRADIENT_DATA, colorfmt="rgb")

    def draw(self, *args):
        super(SmoothLinePlot, self).draw(*args)
        # flatten the list
        points = []
        for x, y in self.iterate_points():
            points += [x, y]
        self._gline.points = points


class ContourPlot(Plot):
    """
    ContourPlot visualizes 3 dimensional data as an intensity map image.
    The user must first specify 'xrange' and 'yrange' (tuples of min,max) and
    then 'data', the intensity values.
    `data`, is a MxN matrix, where the first dimension of size M specifies the
    `y` values, and the second dimension of size N specifies the `x` values.
    Axis Y and X values are assumed to be linearly spaced values from
    xrange/yrange and the dimensions of 'data', `MxN`, respectively.
    The color values are automatically scaled to the min and max z range of the
    data set.
    """
    _image = ObjectProperty(None)
    data = ObjectProperty(None, force_dispatch=True)
    xrange = ListProperty([0, 100])
    yrange = ListProperty([0, 100])

    def __init__(self, **kwargs):
        super(ContourPlot, self).__init__(**kwargs)
        self.bind(data=self.ask_draw, xrange=self.ask_draw,
                  yrange=self.ask_draw)

    def create_drawings(self):
        self._image = Rectangle()
        self._color = Color([1, 1, 1, 1])
        self.bind(color=lambda instr, value: setattr(self._color, 'rgba', value))
        return [self._color, self._image]

    def draw(self, *args):
        super(ContourPlot, self).draw(*args)
        data = self.data
        xdim, ydim = data.shape

        # Find the minimum and maximum z values
        zmax = data.max()
        zmin = data.min()
        rgb_scale_factor = 1.0 / (zmax - zmin) * 255
        # Scale the z values into RGB data
        buf = np.array(data, dtype=float, copy=True)
        np.subtract(buf, zmin, out=buf)
        np.multiply(buf, rgb_scale_factor, out=buf)
        # Duplicate into 3 dimensions (RGB) and convert to byte array
        buf = np.asarray(buf, dtype=np.uint8)
        buf = np.expand_dims(buf, axis=2)
        buf = np.concatenate((buf, buf, buf), axis=2)
        buf = np.reshape(buf, (xdim, ydim, 3))

        charbuf = bytearray(np.reshape(buf, (buf.size)))
        self._texture = Texture.create(size=(xdim, ydim), colorfmt='rgb')
        self._texture.blit_buffer(charbuf, colorfmt='rgb', bufferfmt='ubyte')
        image = self._image
        image.texture = self._texture

        x_px = self.x_px()
        y_px = self.y_px()
        bl = x_px(self.xrange[0]), y_px(self.yrange[0])
        tr = x_px(self.xrange[1]), y_px(self.yrange[1])
        image.pos = bl
        w = tr[0] - bl[0]
        h = tr[1] - bl[1]
        image.size = (w, h)


class BarPlot(Plot):
    '''BarPlot class which displays a bar graph.
    '''

    bar_width = NumericProperty(1)
    bar_spacing = NumericProperty(1.)
    graph = ObjectProperty(allownone=True)

    def __init__(self, *ar, **kw):
        super(BarPlot, self).__init__(*ar, **kw)
        self.bind(bar_width=self.ask_draw)
        self.bind(points=self.update_bar_width)
        self.bind(graph=self.update_bar_width)

    def update_bar_width(self, *ar):
        if not self.graph:
            return
        if len(self.points) < 2:
            return
        if self.graph.xmax == self.graph.xmin:
            return

        point_width = (
            len(self.points) *
            float(abs(self.graph.xmax) + abs(self.graph.xmin)) /
            float(abs(max(self.points)[0]) + abs(min(self.points)[0])))

        if not self.points:
            self.bar_width = 1
        else:
            self.bar_width = (
                (self.graph.width - self.graph.padding) /
                point_width * self.bar_spacing)

    def create_drawings(self):
        self._color = Color(*self.color)
        self._mesh = Mesh()
        self.bind(color=lambda instr, value: setattr(self._color, 'rgba', value))
        return [self._color, self._mesh]

    def draw(self, *args):
        super(BarPlot, self).draw(*args)
        points = self.points

        # The mesh only supports (2^16) - 1 indices, so...
        if len(points) * 6 > 65535:
            Logger.error(
                "BarPlot: cannot support more than 10922 points. "
                "Ignoring extra points.")
            points = points[:10922]

        point_len = len(points)
        mesh = self._mesh
        mesh.mode = 'triangles'
        vert = mesh.vertices
        ind = mesh.indices
        diff = len(points) * 6 - len(vert) // 4
        if diff < 0:
            del vert[4 * point_len:]
            del ind[point_len:]
        elif diff > 0:
            ind.extend(range(len(ind), len(ind) + diff))
            vert.extend([0] * (diff * 4))

        bounds = self.get_px_bounds()
        x_px = self.x_px()
        y_px = self.y_px()
        ymin = y_px(0)

        bar_width = self.bar_width
        if bar_width < 0:
            bar_width = x_px(bar_width) - bounds["xmin"]

        for k in range(point_len):
            p = points[k]
            x1 = x_px(p[0])
            x2 = x1 + bar_width
            y1 = ymin
            y2 = y_px(p[1])

            idx = k * 24
            # first triangle
            vert[idx] = x1
            vert[idx + 1] = y2
            vert[idx + 4] = x1
            vert[idx + 5] = y1
            vert[idx + 8] = x2
            vert[idx + 9] = y1
            # second triangle
            vert[idx + 12] = x1
            vert[idx + 13] = y2
            vert[idx + 16] = x2
            vert[idx + 17] = y2
            vert[idx + 20] = x2
            vert[idx + 21] = y1
        mesh.vertices = vert

    def _unbind_graph(self, graph):
        graph.unbind(width=self.update_bar_width,
                     xmin=self.update_bar_width,
                     ymin=self.update_bar_width)

    def bind_to_graph(self, graph):
        old_graph = self.graph

        if old_graph:
            # unbind from the old one
            self._unbind_graph(old_graph)

        # bind to the new one
        self.graph = graph
        graph.bind(width=self.update_bar_width,
                   xmin=self.update_bar_width,
                   ymin=self.update_bar_width)

    def unbind_from_graph(self):
        if self.graph:
            self._unbind_graph(self.graph)


class HBar(MeshLinePlot):
    '''HBar draw horizontal bar on all the Y points provided
    '''

    def plot_mesh(self, *args):
        points = self.points
        mesh, vert, ind = self.set_mesh_size(len(points) * 2)
        mesh.mode = "lines"

        bounds = self.get_px_bounds()
        px_xmin = bounds["xmin"]
        px_xmax = bounds["xmax"]
        y_px = self.y_px()
        for k, y in enumerate(points):
            y = y_px(y)
            vert[k * 8] = px_xmin
            vert[k * 8 + 1] = y
            vert[k * 8 + 4] = px_xmax
            vert[k * 8 + 5] = y
        mesh.vertices = vert


class VBar(MeshLinePlot):
    '''VBar draw vertical bar on all the X points provided
    '''

    def plot_mesh(self, *args):
        points = self.points
        mesh, vert, ind = self.set_mesh_size(len(points) * 2)
        mesh.mode = "lines"

        bounds = self.get_px_bounds()
        px_ymin = bounds["ymin"]
        px_ymax = bounds["ymax"]
        x_px = self.x_px()
        for k, x in enumerate(points):
            x = x_px(x)
            vert[k * 8] = x
            vert[k * 8 + 1] = px_ymin
            vert[k * 8 + 4] = x
            vert[k * 8 + 5] = px_ymax
        mesh.vertices = vert

class _LegendSymbol(Widget):
    
    # triggers an update of graphics
    _trigger = ObjectProperty(None)
    
    background_color = ListProperty([0, 0, 0, 0])
    '''Color of the background. Default Transparent.
    
    :data:`background_color` is a :class:`~kivy.properties.ListProperty`, defaults to
    [0, 0, 0, 0].
    '''
    plot_color = ListProperty([1, 1, 1, 1])
    '''Color of the plot.
    
    :data:`plot_color` is a :class:`~kivy.properties.ListProperty`, defaults to
    [1, 1, 1, 1].
    '''
    
    def __init__(self, plot, **kwargs):
        from kivy.graphics import Line
        
        super(_LegendSymbol, self).__init__(**kwargs)
        
        self.size_hint = (None, None)
        self.size = (75, 25)
        with self.canvas:
            self._background_color = Color(*self.background_color)
            self._background_rect = Rectangle(size=self.size, pos=self.pos)
            
            self.plot_color = plot.color
            Color(*self.plot_color)
            
            first_third = self.x + self.width/4
            second_third = self.x + 3*self.width/4
            
            if isinstance(plot, DotPlot):
                self._plot = Point(points=self.center, pointsize=plot.point_size)
                self.plot_type = DotPlot
            elif isinstance(plot, (SmoothLinePlot, LinePlot) ):
                self._plot = Line(points=[first_third, self.center_y, second_third, self.center_y], width=plot.line_width)
                self.plot_type = LinePlot
            elif isinstance(plot, (MeshLinePlot, MeshStemPlot)):
                self._plot = Line(points=[first_third, self.center_y, second_third, self.center_y], width=2.)
                self.plot_type = MeshLinePlot
            
        t = self._trigger = Clock.create_trigger(self._update_pos)
        self.bind(pos=t, size=t)
        
    def _update_pos(self, *args):
        self._background_rect.pos = self.pos
        self._background_rect.size = self.size
        
        first_third = self.x + self.width/4
        second_third = self.x + 3*self.width/4
        
        if self.plot_type == DotPlot:
            points = self.center
        elif self.plot_type == LinePlot:
            points = [first_third, self.center_y, second_third, self.center_y]
        elif self.plot_type == MeshLinePlot:
            points = [first_third, self.center_y, second_third, self.center_y]
        self._plot.points = points

class LegendBox(Widget):
    '''LegendBox draw a legend top right of the grapĥ.
    This class should not be used externaly.
    '''
    # triggers a full reload of graphics
    _trigger = ObjectProperty(None)
    # triggers only a update of colors, e.g. tick_color
    _trigger_color = ObjectProperty(None)
    # holds Instruction object for border
    _border = ObjectProperty(None)
    
    font_size = NumericProperty('15sp')
    '''Font size of the labels.

    :data:`font_size` is a :class:`~kivy.properties.NumericProperty`, defaults
    to 15sp.
    '''
    background_color = ListProperty([0, 0, 0, 0])
    '''Color of the background, defaults to transparent
    '''
    border_color = ListProperty([0.7, 0.7, 0.7, 1])
    '''Color of the border, defaults to grey
    '''
    label_options = DictProperty()
    '''Label options that will be passed to `:class:`kivy.uix.Label`.
    '''
    draw_border = BooleanProperty(True)
    '''Whether a border is drawn around the canvas of the legend.

    :data:`draw_border` is a :class:`~kivy.properties.BooleanProperty`,
    defaults to True.
    '''
    
    _plots = ListProperty([])
    '''List of plots to legend.
    '''  
    _labels = ListProperty([])
    '''List of Label objects that hold the labels.
    '''
    _symbols = ListProperty([])
    '''List of object (_LegendSymbol) that represent the line symbols.
    '''
    
    def __init__(self, **kwargs):
        super(LegendBox, self).__init__(**kwargs)
        
        self.size_hint = (None, None)
        
        self.root = GridLayout(cols=2)
        self.root.height = self.root.minimum_height
        self.root.width = self.root.minimum_width
        self.add_widget(self.root)
        
        with self.canvas.before:
            self._background_color = Color(*self.background_color)
            self._background_rect = RoundedRectangle(size=(self.width+5,self.height), pos=self.pos, radius=[10])
        
        self._border_color = Color(*self.border_color)
        
        t = self._trigger = Clock.create_trigger(self._redraw_all)
        tc = self._trigger_color = Clock.create_trigger(self._update_colors)
        
        self.bind(label_options=t, font_size=t, pos=t, size=t, draw_border=t)
        self.bind(background_color=tc, border_color=tc)
        self._trigger()
            
    def add_plot(self, plot):
        """Add the plot so that it will be legended.
        :Parameters:
            `plot`:
                Plot to add.
                `plot` will be added only if his label is not empty and if it 
                is not already legended.
        """
        if plot in self._plots or not plot.label:
            return
        self._plots.append(plot)
        plot.bind(label=self._update_labels)
        self._update_widgets()
        self._redraw_all()
        
    def remove_plot(self, plot):
        """Remove the plot so that it will not be legended.
        :Parameters:
            `plot`:
                Plot to remove.
        """
        if plot not in self._plots:
            return
        self._plots.remove(plot)
        plot.unbind(label=self._update_labels)
        self._update_widgets()
        self._redraw_all()
    
    def update_plots(self, plots):
        """Update the plot list to legend.
        :Parameters:
            `plots`:
                Plot list to legend.
                A plot will be added only if his label is not empty and if it 
                is not already legended.
                All plots already legended that does not appear in `plots` will
                be removed.
        """
        for plot in self._plots:
            if plot not in plots or not plot.label:
                plot.unbind(label=self._update_labels)
                self._plots.remove(plot)
        for plot in plots:
            if plot in self._plots or not plot.label:
                continue
            plot.bind(label=self._update_labels)
            self._plots.append(plot)
        
        self._update_widgets()
        self._redraw_all()
        
    def _redraw_all(self, *args):
        self._update_colors()
        self._redraw_widgets()
        self._update_size()
        
    
    def _update_size(self, *args):
        self._background_rect.size = (self.root.width+5, self.root.height)
        
        self._background_rect.pos = self.pos
        self.root.pos = self.pos
        
        self._update_border()
        
        if self.draw_border:
            self.width = self.root.width + 8
            self.height = self.root.height + 3
        else:
            self.size = self.root.size
        
    def _update_colors(self, *args):
        self._background_color.rgba = tuple(self.background_color)
        self._border_color.rgba = tuple(self.border_color)
    
    def _update_border(self, *args):
        from kivy.graphics import Line
        if self.draw_border:
            if self._border:
                self.canvas.remove(self._border)
            with self.canvas:
                self._border_color = Color(*self.border_color)
                self._border = Line(rounded_rectangle=(self.x, self.y, self.root.width + 5, self.root.height, 10))
        else:
            if self._border:
                self.canvas.remove(self._border)
                self._border = None      
                
    def _redraw_widgets(self, *args):
        width_symbol = 0
        for label, symbol in zip(self._labels, self._symbols):
            for k, v in self.label_options.items():
                setattr(label, k, v)
            label.font_size = self.font_size
            label.texture_update()
            label.size = label.texture_size
            label.height += 10
            width_symbol = symbol.width
        if self._labels:
            width = max(label.width for label in self._labels)
            height = sum(label.height for label in self._labels)
            self.root.width = width + width_symbol
            self.root.height = height
    
    def _update_widgets(self, *args):
        self.root.clear_widgets()
        self._labels.clear()
        self._symbols.clear(), 
        width_symbol = 0
        for plot in self._plots:
            label = Label(text=plot.label, **self.label_options)
            label.font_size = self.font_size
            label.texture_update()
            label.size_hint = (None, None)
            label.size = label.texture_size
            label.height += 10
            symbol = _LegendSymbol(plot, pos = self.pos)
            symbol.height = label.height
            width_symbol = symbol.width
            self._labels.append(label)
            self._symbols.append(symbol)
        
        if self._labels:
            width = max(label.width for label in self._labels)
            height = sum(label.height for label in self._labels)
            
            self.root.width = width + width_symbol
            self.root.height = height
        
        for label, symbol in zip(self._labels, self._symbols):
            self.root.add_widget(symbol)
            self.root.add_widget(label)
            symbol.pos = self.pos
    
    def _update_labels(self, *args):
        width_symbol = 0
        for plot, label, symbol in zip(self._plots, self._labels, self._symbols):
            label.text=plot.label
            label.font_size = self.font_size
            label.texture_update()
            label.size_hint = (None, None)
            label.size = label.texture_size
            label.height += 10
            symbol.height = label.height
            width_symbol = symbol.width
        
        if self._labels:
            width = max(label.width for label in self._labels)
            height = sum(label.height for label in self._labels)
            
            self.root.width = width + width_symbol
            self.root.height = height
        
        for symbol in self._symbols:
            symbol.pos = self.pos

if __name__ == '__main__':
    import itertools
    from math import sin, cos, pi, sqrt
    from random import randrange
    from kivy.utils import get_color_from_hex as rgb
    from kivy.uix.boxlayout import BoxLayout
    from kivy.app import App

    class TestApp(App):

        def build(self):
            b = BoxLayout(orientation='vertical')
            # example of a custom theme
            colors = itertools.cycle([
                rgb('7dac9f'), rgb('dc7062'), rgb('66a8d4'), rgb('e5b060')])
            graph_theme = {
                'label_options': {
                    'color': rgb('444444'),  # color of tick labels and titles
                    'bold': True},
                'background_color': rgb('f8f8f2'),  # back ground color of canvas
                'tick_color': rgb('808080'),  # ticks and grid
                'border_color': rgb('808080')}  # border drawn around each graph

            graph = Graph(
                xlabel='Cheese',
                ylabel='Apples',
                x_ticks_minor=5,
                x_ticks_major=25,
                y_ticks_major=1,
                y_grid_label=True,
                x_grid_label=True,
                padding=5,
                xlog=False,
                ylog=False,
                x_grid=True,
                y_grid=True,
                xmin=-50,
                xmax=50,
                ymin=-1,
                ymax=1,
                **graph_theme)

            plot = SmoothLinePlot(color=next(colors))
            plot.points = [(x / 10., sin(x / 50.)) for x in range(-500, 501)]
            # for efficiency, the x range matches xmin, xmax
            graph.add_plot(plot)

            plot = MeshLinePlot(color=next(colors))
            plot.points = [(x / 10., cos(x / 50.)) for x in range(-500, 501)]
            graph.add_plot(plot)
            self.plot = plot  # this is the moving graph, so keep a reference

            plot = MeshStemPlot(color=next(colors))
            graph.add_plot(plot)
            plot.points = [(x, x / 50.) for x in range(-50, 51)]

            plot = BarPlot(color=next(colors), bar_spacing=.72)
            graph.add_plot(plot)
            plot.bind_to_graph(graph)
            plot.points = [(x, .1 + randrange(10) / 10.) for x in range(-50, 1)]

            Clock.schedule_interval(self.update_points, 1 / 60.)
            
            b.add_widget(graph)

            graph2 = Graph(
                xlabel='Position (m)',
                ylabel='Time (s)',
                x_ticks_minor=0,
                x_ticks_major=1,
                y_ticks_major=10,
                y_grid_label=True,
                x_grid_label=True,
                padding=5,
                xlog=False,
                ylog=False,
                xmin=0,
                ymin=0,
                **graph_theme)

            if np is not None:
                (xbounds, ybounds, data) = self.make_contour_data()
                # This is required to fit the graph to the data extents
                graph2.xmin, graph2.xmax = xbounds
                graph2.ymin, graph2.ymax = ybounds

                plot = ContourPlot()
                plot.data = data
                plot.xrange = xbounds
                plot.yrange = ybounds
                plot.color = [1, 0.7, 0.2, 1]
                graph2.add_plot(plot)

                b.add_widget(graph2)
                self.contourplot = plot

                Clock.schedule_interval(self.update_contour, 1 / 60.)
            
            graph3 = Graph(
                title='Some curves',
                xlabel='x',
                ylabel='y',
                x_ticks_minor=5,
                x_ticks_major=25,
                y_ticks_major=1,
                y_grid_label=True,
                x_grid_label=True,
                padding=5,
                xlog=False,
                ylog=False,
                x_grid=True,
                y_grid=True,
                xmin=0,
                xmax=100,
                ymin=0,
                ymax=10,
                **graph_theme)
            
            plot = SmoothLinePlot(color=next(colors))
            plot.points = [(x/10., sqrt(x/10.)) for x in range(0, 1000)]
            plot.label = "y = sqrt(x)"
            graph3.add_plot(plot)

            plot = DotPlot(color=next(colors))
            plot.points = [(x,x*1/10.) for x in range(0, 100)]
            plot.point_size = 3
            plot.label="y = x * 1/10"
            graph3.add_plot(plot)
            
            graph3.legend = True
            graph3.legend_pos = "bottom right"
            
            b.add_widget(graph3)

            return b

        def make_contour_data(self, ts=0):
            omega = 2 * pi / 30
            k = (2 * pi) / 2.0

            ts = sin(ts * 2) + 1.5  # emperically determined 'pretty' values
            npoints = 100
            data = np.ones((npoints, npoints))

            position = [ii * 0.1 for ii in range(npoints)]
            time = [(ii % 100) * 0.6 for ii in range(npoints)]

            for ii, t in enumerate(time):
                for jj, x in enumerate(position):
                    data[ii, jj] = sin(k * x + omega * t) + sin(-k * x + omega * t) / ts
            return ((0, max(position)), (0, max(time)), data)

        def update_points(self, *args):
            self.plot.points = [(x / 10., cos(Clock.get_time() + x / 50.)) for x in range(-500, 501)]

        def update_contour(self, *args):
            _, _, self.contourplot.data[:] = self.make_contour_data(Clock.get_time())
            # this does not trigger an update, because we replace the
            # values of the arry and do not change the object.
            # However, we cannot do "...data = make_contour_data()" as
            # kivy will try to check for the identity of the new and
            # old values.  In numpy, 'nd1 == nd2' leads to an error
            # (you have to use np.all).  Ideally, property should be patched
            # for this.
            self.contourplot.ask_draw()

    TestApp().run()
