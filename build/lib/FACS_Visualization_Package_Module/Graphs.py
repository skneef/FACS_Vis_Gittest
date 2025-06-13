import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .LogicleTransform import *
from scipy import stats
from matplotlib import cm
from sklearn.neighbors import KernelDensity
import seaborn as sns
import seaborn.objects as so
import matplotlib.lines as mpl
import matplotlib.patches as mpp

def dotplot(data, xvalue, yvalue, gui=False, save=None, legend=False, logicle_axis="Both", xline=None, yline=None, xlim=None, ylim=None, title=None):
    if not isinstance(legend, bool):
        raise ValueError("Invalid legend input. Expected True or False")
    logicle_axis_types = ["Both", "x", "y", "None"]
    if logicle_axis not in logicle_axis_types:
        raise ValueError("Invalid logicle_axis input. Expected on of: %s" % logicle_axis_types)

    if xline != None:
        if not isinstance(xline, (int | float)):
            raise ValueError("Invalid xline input. Expected an integer or float")

    if yline != None:
        if not isinstance(yline, (int | float)):
            raise ValueError("Invalid yline input. Expected an integer or float")

    if xlim != None:
        if type(xlim) != tuple or len(xlim) != 2 :
            raise ValueError("Invalid xlim input. Expected a tuple of xmin and xmax: (xmin, xmax)")

    if ylim != None:
        if type(ylim) != tuple or len(ylim) != 2 :
            raise ValueError("Invalid ylim input. Expected a tuple of ymin and ymax: (ymin, ymax)")

    if title != None:
        if not isinstance(title, str):
            raise ValueError("Invalid title input. Expected None or a string")


    xdata = data[xvalue]
    ydata = data[yvalue]

    T = 262144
    M = 4.5
    #x data transformation
    if logicle_axis in ["Both", "x"]:
        r = min(xdata)
        h = max(xdata)

        t, m, w, a, p = calculate_parameters(T, M, r)
        if len(xdata < 0) / len(xdata) < 0.01:
            a = 0

        xlogicle = [calculate_logicle(t, m, w, a, p, x) for x in xdata]

        main_xaxis_scale, sec_xaxis_scale, ter_xaxis_scale = axis_scale(t, m, w, a, p, min=r, max=h)

        if xline != None:
            xline = calculate_logicle(t, m, w, a, p, xline)
    else:
        xlogicle = xdata


    #y data transformation
    if logicle_axis in ["Both", "y"]:
        r = min(ydata)
        h = max(ydata)

        t, m, w, a, p = calculate_parameters(T, M, r)
        if len(ydata < 0) / len(ydata) < 0.01:
            a = 0

        ylogicle = [calculate_logicle(t, m, w, a, p, y) for y in ydata]

        main_yaxis_scale, sec_yaxis_scale, ter_yaxis_scale = axis_scale(t, m, w, a, p, min=r, max=h)

        if yline != None:
            yline = calculate_logicle(t, m, w, a, p, yline)
    else:
        ylogicle = ydata


    #calculate density colour scheme
    kde = stats.gaussian_kde([xlogicle, ylogicle])
    zz = kde([xlogicle, ylogicle])
    cc = cm.jet((zz - zz.min()) / (zz.max() - zz.min()))

    # Create the plot
    fig = plt.figure(figsize=(5, 5))

    ax = fig.add_subplot()
    plt.subplots_adjust(right=0.98, top=0.98)
    if title != None:
        ax.title.set_text(title)
    ax.scatter(xlogicle, ylogicle, marker='o', facecolor=cc, s=1)

    # set correct labels and title
    ax.set_xlabel(xvalue, labelpad=30)
    ax.set_ylabel(yvalue, labelpad=30)

    # Add legend
    if legend == True:
        cb = cm.ScalarMappable(cmap='jet')
        fig.colorbar(cb, ax=ax, label="Density", shrink=0.4, aspect=10)

    # set the axis to use the logicle scale
    if logicle_axis in ["Both", "x"]:
        ax.set_xticks([])

        main_xax = ax.secondary_xaxis(location=0)
        main_xax.set_xticks(list(main_xaxis_scale["Logicle"]), labels=list(main_xaxis_scale["Name"]))
        main_xax.tick_params("x", length=10)
        sec_xax = ax.secondary_xaxis(location=0)
        sec_xax.set_xticks(list(sec_xaxis_scale["Logicle"]), labels=list(sec_xaxis_scale["Name"]))
        sec_xax.tick_params("x", length=6)
        ter_xax = ax.secondary_xaxis(location=0)
        ter_xax.set_xticks(list(ter_xaxis_scale["Logicle"]), labels=list(ter_xaxis_scale["Name"]))
        ter_xax.tick_params("x", length=3)

    if logicle_axis in ["Both", "y"]:
        ax.set_yticks([])

        main_yax = ax.secondary_yaxis(location=0)
        main_yax.set_yticks(list(main_yaxis_scale["Logicle"]), labels=list(main_yaxis_scale["Name"]))
        main_yax.tick_params("y", length=10)
        sec_yax = ax.secondary_yaxis(location=0)
        sec_yax.set_yticks(list(sec_yaxis_scale["Logicle"]), labels=list(sec_yaxis_scale["Name"]))
        sec_yax.tick_params("y", length=6)
        ter_yax = ax.secondary_yaxis(location=0)
        ter_yax.set_yticks(list(ter_yaxis_scale["Logicle"]), labels=list(ter_yaxis_scale["Name"]))
        ter_yax.tick_params("y", length=3)


    # set gating lines and axis limit
    if xline != None:
        ax.axvline(xline, c='k')

    if yline != None:
        ax.axhline(yline, c='k')

    if xlim != None:
        ax.set_xlim(xlim)
    if ylim != None:
        ax.set_ylim(ylim)


    if gui:
        return fig
    else:
        if save == None:
            plt.show()

        if save != None:
            plt.savefig(save)
            print(str(save) + " image finished")

        plt.close()



def histogram(data, save=None, legend=False, logicle_axis=True, xline=None, xlim=None, ylim=None, column="All", xaxis_label=None, legend_data=None, title=None):
    #if not isinstance(data, (list | np.array | pd.DataFrame | pd.Series)):
    #    raise ValueError("Invalid data input. Expected a list, numpy.array, pandas.DataFrame, or pandas.Series")

    if not isinstance(legend, bool):
        raise ValueError("Invalid legend input. Expected True or False")

    if not isinstance(logicle_axis, bool):
        raise ValueError("Invalid logicle_axis input. Expected True or False")

    if xline != None:
        if not isinstance(xline, (int | float)):
            raise ValueError("Invalid xline input. Expected an integer or float")

    if xlim != None:
        if type(xlim) != tuple or len(xlim) != 2:
            raise ValueError("Invalid xlim input. Expected a tuple of xmin and xmax: (xmin, xmax)")

    if ylim != None:
        if type(ylim) != tuple or len(ylim) != 2:
            raise ValueError("Invalid ylim input. Expected a tuple of ymin and ymax: (ymin, ymax)")
    if xaxis_label != None:
        if not isinstance(xaxis_label, str):
            raise ValueError("Invalid xaxis_label input. Expected a string")

    if title != None:
        if not isinstance(title, str):
            raise ValueError("Invalid title input. Expected None or a string")

    other_columns = pd.DataFrame()
    other_columns_graph = pd.DataFrame()
    data_name = "1"
    if type(data) == np.array:
        data = data[~np.isnan(data)].tolist()
    if type(data) == pd.Series:
        data = data.dropna(inplace=False, ignore_index = True).to_list()
    if type(data) == pd.DataFrame:
        if column == "All":
            other_columns = data[data.columns[1:]]
            data_name = data.columns[0]
            data = data[data.columns[0]].to_list()
        else:
            if not isinstance(column, list):
                raise ValueError("Invalid column input. Expected 'All' or a list")
            if len(column) > 2:
                other_columns = data[column[1:]]
                data = data[[column[0]]].to_list()
            elif len(column) == 2:
                other_columns = data[[column[1]]].to_list()
                data = data[[column[0]]].to_list()
            else:
                data = data[[column[0]]].to_list()

    size = len(data)
    x_axis = np.linspace(0, 4.5, size)
    if logicle_axis == True:
        T = 262144
        M = 4.5
        r = min(data)
        h = max(data)

        t, m, w, a, p = calculate_parameters(T, M, r)

        if (len([x for x in data if x < 0]) / len(data)) < 0.01:
            a = 0

        data_graph = [calculate_logicle(t, m, w, a, p, x) for x in data]

        main_xaxis_scale, sec_xaxis_scale, ter_xaxis_scale = axis_scale(t, m, w, a, p, min=r, max=h)

        if xline != None:
            xline = calculate_logicle(t, m, w, a, p, xline)
        if not other_columns.empty:
            if isinstance(other_columns, list):
                other_columns_graph = [calculate_logicle(t, m, w, a, p, x) for x in other_columns]

            if isinstance(other_columns, pd.DataFrame):
                other_columns_graph = pd.DataFrame(columns= other_columns.columns)
                for cols in other_columns.columns:
                    other_columns_graph[cols] = [calculate_logicle(t, m, w, a, p, x) for x in other_columns[cols]]

    else:
        data_graph = data

    def kde_sklearn(x, x_grid, bandwidth=0.2, **kwargs):
        kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs)
        kde_skl.fit(x[:, np.newaxis])
        log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
        return kde_skl, np.exp(log_pdf)

    data_graph = np.array(data_graph)
    kde, pdf = kde_sklearn(data_graph, x_axis, bandwidth="scott", kernel="epanechnikov")

    fig, ax = plt.subplots(figsize=(5, 5))
    if title != None:
        ax.title.set_text(title)

    ax.plot(x_axis, pdf, label=data_name)

    if not other_columns_graph.empty:
        for cols in other_columns_graph.columns:
            data_graph = np.array(other_columns_graph[cols])
            kde, pdf = kde_sklearn(data_graph, x_axis, bandwidth="scott", kernel="epanechnikov")
            ax.plot(x_axis, pdf, label=cols)


    if logicle_axis == True:
        ax.set_xticks([])
        ax.set_xlim((0, 4.5))

        main_xax = ax.secondary_xaxis(location=0)
        main_xax.set_xticks(list(main_xaxis_scale["Logicle"]), labels=list(main_xaxis_scale["Name"]))
        main_xax.tick_params("x", length=10)
        sec_xax = ax.secondary_xaxis(location=0)
        sec_xax.set_xticks(list(sec_xaxis_scale["Logicle"]), labels=list(sec_xaxis_scale["Name"]))
        sec_xax.tick_params("x", length=6)
        ter_xax = ax.secondary_xaxis(location=0)
        ter_xax.set_xticks(list(ter_xaxis_scale["Logicle"]), labels=list(ter_xaxis_scale["Name"]))
        ter_xax.tick_params("x", length=3)

    if xline != None:
        ax.axvline(xline, c='k')

    if xlim != None:
        ax.set_xlim(xlim)
    if ylim != None:
        ax.set_ylim(ylim)

    if xaxis_label != None:
        ax.set_xlabel(xaxis_label, labelpad=30)

    if save == None:
        plt.show()

    if save != None:
        plt.savefig(save)
        print(str(save) + " image finished")

    if legend:
        h, l = ax.get_legend_handles_labels()
        h_colours = []
        for x in h:
            h_colours.append(x.get_color())
        table_text = pd.DataFrame()
        table_text["File"] = l
        table_text = pd.merge(table_text, legend_data, how='inner', on='File')
        plt.close()
        fig, ax = plt.subplots()
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        ax.table(cellText=table_text.values, rowColours=h_colours, colLabels=["File", "Patient ID", "Sample ID"])
        fig.tight_layout()

        if save == None:
            plt.show()
        if save != None:
            save_legend = save[:-4] + "_legend1.png"
            plt.savefig(save_legend)
            print(str(save_legend) + " image finished")

    plt.close()

def boxplot(data, xvariable, yvalue, group, save=None, legend=False, yaxis_scale="Linear", xvariable2=None, x_control=None, title=None):
    if not isinstance(legend, bool):
        raise ValueError("Invalid legend input. Expected True or False")

    if not xvariable in data.columns:
        raise ValueError("Invalid xvariable input. Expected a column name of data")

    if not yvalue in data.columns:
        raise ValueError("Invalid yvalue input. Expected a column name of data")

    if xvariable2 != None:
        if not xvariable2 in data.columns:
            raise ValueError("Invalid xvariable2 input. Expected a column name of data or None")

    if not yaxis_scale in ["Linear", "Log"]:
        raise ValueError("Invalid yaxis_scale input. Expected 'Linear' or 'Log'")

    if title != None:
        if not isinstance(title, str):
            raise ValueError("Invalid title input. Expected None or a string")

    group_markers = data[group].unique()
    style_markers = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']
    marker_dict = dict(zip(group_markers, style_markers[0:len(group_markers)]))

    xvariable_colours = data[xvariable].unique()
    style_colours = ["#ffffcc", "#c7e9b4", "#7fcdbb", "#41b6c4", "#2c7fb8", "#253494"]
    colour_dict = dict(zip(xvariable_colours, style_colours[0:len(xvariable_colours)]))

    def boxplot_one_variable(data, x, y, axis, group, second_x=""):
        sns.boxplot(data=data, x=x, y=y, color="#adadad", fill=False, ax=axis, zorder=1, showfliers=False)

        (
            so.Plot(data=data, x=x, y=y, marker=group, linestyle=group, group=group)
            .add(so.Dot(pointsize=9, artist_kws={"zorder": 2}), so.Jitter(), legend=False, color=x, marker=group)
            .add(so.Line(color="#000000", marker="", artist_kws={"zorder": 2}), legend=False)
            .label(x=second_x, y="")
            .scale(marker=marker_dict, color=colour_dict)
            .on(axis).plot()
        )

    xvars = data[xvariable].unique()
    if x_control is None:
        x_control = xvars[0]
    itemindex = np.where(xvars == x_control)
    xvars = np.delete(xvars, itemindex)

    fig_ncols = 1
    if xvariable2 != None:
        xvariable2_list = data[xvariable2].unique()
        fig_ncols = len(xvariable2_list)
    else:
        xvariable2_list = []

    fig_width = fig_ncols * 2

    if fig_ncols == 2:
        fig, (ax1, ax2) = plt.subplots(ncols=fig_ncols, figsize=(fig_width, 3), sharey=True)
        axes = [ax1, ax2]
    elif fig_ncols == 3:
        fig, (ax1, ax2, ax3) = plt.subplots(ncols=fig_ncols, figsize=(fig_width, 3), sharey=True)
        axes = [ax1, ax2, ax3]
    elif fig_ncols == 4:
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(ncols=fig_ncols, figsize=(fig_width, 3), sharey=True)
        axes = [ax1, ax2, ax3, ax4]
    elif fig_ncols == 5:
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(ncols=fig_ncols, figsize=(fig_width, 3), sharey=True)
        axes = [ax1, ax2, ax3, ax4, ax5]
    elif fig_ncols == 6:
        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(ncols=fig_ncols, figsize=(fig_width, 3), sharey=True)
        axes = [ax1, ax2, ax3, ax4, ax5, ax6]
    else:
        fig, ax1 = plt.subplots(ncols=fig_ncols, figsize=(fig_width, 3), sharey=True)
        axes = [ax1]


    for n in list(range(fig_ncols)):
        if xvariable2 != None:
            n_data = data[data[xvariable2] == xvariable2_list[n]]
            boxplot_one_variable(n_data, xvariable, yvalue, axes[n], group=group, second_x=xvariable2_list[n])
        else:
            n_data = data
            boxplot_one_variable(n_data, xvariable, yvalue, axes[n], group=group)

        axes[n].spines[['right', 'top']].set_visible(False)
        if yaxis_scale == "Linear":
            axes[n].ticklabel_format(axis="y", style='sci', scilimits=(-3, 3))

        # Calculate p-value
        p_data = n_data[[xvariable, group, yvalue]].copy()
        p_data = p_data.pivot_table(values=yvalue, index=group, columns=xvariable, observed=False)

        if len(xvars) == 1:
            a, b = stats.ttest_rel(p_data[x_control], p_data[xvars[0]])

            if b < 0.05:
                p_value = "P: " + str(round(b, 4))
                axes[n].plot([0.25, 0.25, 0.75, 0.75], [1.01, 1.03, 1.03, 1.01],
                         transform=axes[n].transAxes,
                         clip_on=False, c='k')
                axes[n].text(0.5, 1.03, p_value, ha='center', va='bottom', transform=axes[n].transAxes,
                         clip_on=False, c='k')
        elif len(xvars) == 2:
            a, b1 = stats.ttest_rel(p_data[x_control], p_data[xvars[0]])
            a, b2 = stats.ttest_rel(p_data[x_control], p_data[xvars[1]])

            if b1 < 0.05:
                p_value = "P: " + str(round(b1, 4))
                axes[n].plot([0.165, 0.165, 0.5, 0.5], [1.01, 1.03, 1.03, 1.01],
                         transform=axes[n].transAxes,
                         clip_on=False, c='k')
                axes[n].text(0.33, 1.03, p_value, ha='center', va='bottom', transform=axes[n].transAxes,
                         clip_on=False, c='k')

            if b2 < 0.05:
                p_value = "P: " + str(round(b2, 4))
                axes[n].plot([0.165, 0.165, 0.833, 0.833], [1.01, 1.03, 1.03, 1.01],
                         transform=axes[n].transAxes,
                         clip_on=False, c='k')
                axes[n].text(0.5, 1.03, p_value, ha='center', va='bottom', transform=axes[n].transAxes,
                         clip_on=False, c='k')

        else:
            raise ValueError("Current function can only handle comparison a maximum of 3 variables")

    if len(axes) > 1:
        for ax in axes[1:]:
            ax.spines[['left']].set_visible(False)
            ax.tick_params(axis='y', which='both', labelleft=False, length=0)


    if title != None:
        ax1.set_title(title, pad=20)

    if save == None:
        plt.show()
    else:
        plt.savefig(save)

    if legend:
        plt.close()
        lines = {}
        for x in marker_dict.keys():
            lines["line{0}".format(x)] = mpl.Line2D([], [], linestyle="", marker=marker_dict[x], color="#000000", fillstyle='none')

        cols = {}
        for x in colour_dict.keys():
            cols["cols{0}".format(x)] = mpp.Rectangle((0, 0), 0.1, 0.05, ec="none", color=colour_dict[x])

        line0 = mpl.Line2D([], [], linestyle="", label="Empty")

        handles = [line0] + list(lines.values()) + [line0] + list(cols.values())
        labels = [group] +  list(marker_dict.keys()) + [xvariable] + list(colour_dict.keys())

        legend = plt.legend(handles=handles, labels=labels)

        fig.canvas.draw()

        legend_bbox = legend.get_tightbbox()
        legend_bbox = legend_bbox.transformed(fig.dpi_scale_trans.inverted())
        plt.close()
        legend_fig, legend_ax = plt.subplots(figsize=(legend_bbox.width * 2, legend_bbox.height))
        legend_squared = legend_ax.legend(
            handles, labels,
            bbox_to_anchor=(0, 0, 1, 1),
            bbox_transform=legend_fig.transFigure,
            frameon=False,
            fancybox=None,
            shadow=False,
            ncol=1,
            mode='expand',
        )
        legend_ax.axis('off')

        if save == None:
            plt.show()
        if save != None:
            save_legend = save[:-4] + "_legend1.png"
            plt.savefig(save_legend, bbox_inches='tight', bbox_extra_artists=[legend_squared])
            print(str(save_legend) + " image finished")

    plt.close()