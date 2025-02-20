from matplotlib.colors import to_rgba, to_rgba_array

from numpy.testing import assert_array_equal

from seaborn._core.plot import Plot
from seaborn._marks.scatter import Dot, Scatter


class ScatterBase:

    def check_offsets(self, points, x, y):

        offsets = points.get_offsets().T
        assert_array_equal(offsets[0], x)
        assert_array_equal(offsets[1], y)

    def check_colors(self, part, points, colors, alpha=None):

        rgba = to_rgba_array(colors, alpha)

        getter = getattr(points, f"get_{part}colors")
        assert_array_equal(getter(), rgba)


class TestScatter(ScatterBase):

    def test_simple(self):

        x = [1, 2, 3]
        y = [4, 5, 2]
        p = Plot(x=x, y=y).add(Scatter()).plot()
        ax = p._figure.axes[0]
        points, = ax.collections
        self.check_offsets(points, x, y)
        self.check_colors("face", points, ["C0"] * 3, .2)
        self.check_colors("edge", points, ["C0"] * 3, 1)

    def test_color_direct(self):

        x = [1, 2, 3]
        y = [4, 5, 2]
        p = Plot(x=x, y=y).add(Scatter(color="g")).plot()
        ax = p._figure.axes[0]
        points, = ax.collections
        self.check_offsets(points, x, y)
        self.check_colors("face", points, ["g"] * 3, .2)
        self.check_colors("edge", points, ["g"] * 3, 1)

    def test_color_mapped(self):

        x = [1, 2, 3]
        y = [4, 5, 2]
        c = ["a", "b", "a"]
        p = Plot(x=x, y=y, color=c).add(Scatter()).plot()
        ax = p._figure.axes[0]
        points, = ax.collections
        self.check_offsets(points, x, y)
        self.check_colors("face", points, ["C0", "C1", "C0"], .2)
        self.check_colors("edge", points, ["C0", "C1", "C0"], 1)

    def test_fill(self):

        x = [1, 2, 3]
        y = [4, 5, 2]
        c = ["a", "b", "a"]
        p = Plot(x=x, y=y, color=c).add(Scatter(fill=False)).plot()
        ax = p._figure.axes[0]
        points, = ax.collections
        self.check_offsets(points, x, y)
        self.check_colors("face", points, ["C0", "C1", "C0"], 0)
        self.check_colors("edge", points, ["C0", "C1", "C0"], 1)

    def test_pointsize(self):

        x = [1, 2, 3]
        y = [4, 5, 2]
        s = 3
        p = Plot(x=x, y=y).add(Scatter(pointsize=s)).plot()
        ax = p._figure.axes[0]
        points, = ax.collections
        self.check_offsets(points, x, y)
        assert_array_equal(points.get_sizes(), [s ** 2] * 3)

    def test_stroke(self):

        x = [1, 2, 3]
        y = [4, 5, 2]
        s = 3
        p = Plot(x=x, y=y).add(Scatter(stroke=s)).plot()
        ax = p._figure.axes[0]
        points, = ax.collections
        self.check_offsets(points, x, y)
        assert_array_equal(points.get_linewidths(), [s] * 3)

    def test_filled_unfilled_mix(self):

        x = [1, 2]
        y = [4, 5]
        marker = ["a", "b"]
        shapes = ["o", "x"]

        mark = Scatter(stroke=2)
        p = Plot(x=x, y=y).add(mark, marker=marker).scale(marker=shapes).plot()
        ax = p._figure.axes[0]
        points, = ax.collections
        self.check_offsets(points, x, y)
        self.check_colors("face", points, [to_rgba("C0", .2), to_rgba("C0", 0)], None)
        self.check_colors("edge", points, ["C0", "C0"], 1)
        assert_array_equal(points.get_linewidths(), [mark.stroke] * 2)


class TestDot(ScatterBase):

    def test_simple(self):

        x = [1, 2, 3]
        y = [4, 5, 2]
        p = Plot(x=x, y=y).add(Dot()).plot()
        ax = p._figure.axes[0]
        points, = ax.collections
        self.check_offsets(points, x, y)
        self.check_colors("face", points, ["C0"] * 3, 1)
        self.check_colors("edge", points, ["C0"] * 3, 1)

    def test_filled_unfilled_mix(self):

        x = [1, 2]
        y = [4, 5]
        marker = ["a", "b"]
        shapes = ["o", "x"]

        mark = Dot(edgecolor="k", stroke=2, edgewidth=1)
        p = Plot(x=x, y=y).add(mark, marker=marker).scale(marker=shapes).plot()
        ax = p._figure.axes[0]
        points, = ax.collections
        self.check_offsets(points, x, y)
        self.check_colors("face", points, ["C0", to_rgba("C0", 0)], None)
        self.check_colors("edge", points, ["k", "C0"], 1)

        expected = [mark.edgewidth, mark.stroke]
        assert_array_equal(points.get_linewidths(), expected)
