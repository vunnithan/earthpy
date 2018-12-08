"""Tests for the plot module"""

import numpy as np
import pytest
import earthpy.spatial as es
# For builds on travis to avoid plot display errors
import matplotlib as mpl
#mpl.use('agg')
import matplotlib.pyplot as plt
plt.show = lambda: None



""" General functions for matplotlib elements """


# Create tuple
tuups = (1, 2)
im = np.random.randint(10, size=(2, 4, 5))

def test_arr_parameter():
    """Raise an AttributeError if an array is not provided."""
    with pytest.raises(AttributeError):
        es.plot_bands(arr=tuups)

def test_num_titles():
    """If a user provides two titles for a single band array, the function
    should raise an error OR if the title list is a different length than
    the array it should also raise an errors"""

    single_band = im[0]

    with pytest.raises(ValueError):
        es.plot_bands(arr=single_band,
                      title=["Title1", "Title2"])
    with pytest.raises(ValueError):
        es.plot_bands(arr=im,
                      title=["Title1", "Title2", "Title3"])

def test_num_axes():
    """If provided with a 2 band array, plot_bands should return 3 axes by
    default"""
    fig, ax = es.plot_bands(im)
    assert len(fig.axes) == 3


def test_two_plot_title():
    """Test that the default title is provided for a 2 band array plot"""
    fig, ax = es.plot_bands(im)
    ax = fig.axes
    num_plts = im.shape[0]
    # Get titles
    all_titles = [ax[i].get_title() for i in range(num_plts)]
    assert all_titles == ['Band 1', 'Band 2']


def test_custom_plot_title():
    """Test that the custom title is applied for a 2 band array plot"""
    im = np.indices((4, 4))
    fig, ax = es.plot_bands(im, title=["Red Band", "Green Band"])
    ax = fig.axes
    num_plts = im.shape[0]
    # Get titles
    all_titles = [ax[i].get_title() for i in range(num_plts)]
    assert all_titles == ['Red Band', 'Green Band']


def test_single_band_3dims():
    """If you provide a single band array with 3 dimensions (shape[0]==1
    test that it still plots and only returns a single axis"""

    single_band_3dims = np.random.randint(10, size=(1, 4, 5))
    fig, ax = es.plot_bands(single_band_3dims)
    # Get array from mpl figure
    arr = fig.axes[0].get_images()[0].get_array()
    assert arr.ndim == 2
    assert len(fig.axes[0].get_images()) == 1


def test_single_band_2dims():
    """If you provide a single band array with 3 dimensions (shape[0]==1
    test that it still plots and only returns a single axis"""

    single_band_2dims = np.random.randint(10, size=(4, 5))
    fig, ax = es.plot_bands(single_band_2dims)
    # Get array from mpl figure
    arr = fig.axes[0].get_images()[0].get_array()
    assert arr.ndim == 2
    assert len(fig.axes[0].get_images()) == 1


""" Draw legend tests """

# Array to use in tests below - could become a fixture
im_arr = np.random.randint(10, size=(15, 15))
im_cl_all = np.digitize(im_arr, [-np.inf, 2, 7, np.inf])

# Basic plot
fig, ax = plt.subplots(figsize=(5, 5))
imp2 = ax.imshow(im_cl_all, cmap='Blues')

def test_num_titles_classes():
    """Test to ensure the the number of "handles" or classes provided for each
    legend items matches the number of classes being used to build the legend.
    This case should return a ValueError if these items are different"""

    im_cl_1_3 = im_cl_all.copy()
    im_cl_1_3[im_cl_1_3 == 2] = 3

    fig, ax = plt.subplots(figsize=(5, 5))
    im_ax = ax.imshow(im_cl_1_3, cmap='Blues')

    with pytest.raises(ValueError):
        es.draw_legend(im_ax=im_ax,
                       classes=[1, 2],
                       titles=["small", "medium", "large"])

    with pytest.raises(ValueError):
        es.draw_legend(im_ax=im_ax,
                       classes=[1, 2, 3],
                       titles=["small", "large"])

def test_stock_legend_titles():
    """Test that the correct number of generic titles plot when titles
    parameter = None"""

    # Default legend title values should be
    def_titles = ["Category {}".format(i) for i in np.unique(im_cl_all)]

    the_legend = es.draw_legend(im_ax=imp2)
    # Legend handle titles should equal unique values in ax array
    assert len(the_legend.get_texts()) == len(np.unique(imp2.get_array().data))
    assert def_titles == [text.get_text() for text in the_legend.get_texts()]


def test_custom_legend_titles():
    """Test that the correct number of generic titles plot when titles
    parameter = None"""

    # Default legend title values should be
    custom_titles = ["one", "two", "three"]

    the_legend = es.draw_legend(im_ax=imp2,
                                titles=custom_titles)
    # Legend handle titles should equal unique values in ax array
    assert len(the_legend.get_texts()) == len(np.unique(imp2.get_array().data))
    assert custom_titles == [text.get_text() for text in the_legend.get_texts()]


def test_non_ax_obj():
    """draw_legend fun should raise ValueError if provided with a
    non mpl axis object"""

    with pytest.raises(AttributeError):
        es.draw_legend(im_ax=list())


def test_colors():
    """Test that the correct colors appear in the patches of the legend"""
    the_legend = es.draw_legend(im_ax=imp2)
    # NOTE: Do I know for sure things are rendering in the right order?
    legend_cols = [i.get_facecolor() for i in the_legend.get_patches()]
    # Get the array and cmap from axis object
    cmap_name = imp2.axes.get_images()[0].get_cmap().name
    unique_vals = np.unique(imp2.get_array().data)
    image_colors = es.make_col_list(unique_vals, cmap=cmap_name)

    assert image_colors == legend_cols


# TODO add tests for plots where there are non continuous / missing classes
# Like in the jupyter notebook demo!
