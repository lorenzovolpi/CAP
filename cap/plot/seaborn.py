import os
from pathlib import Path

import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes

from cap.plot.utils import get_binned_values
from cap.utils.commons import get_plots_path

sns.set_theme(style="whitegrid")
sns.set_palette("colorblind")

DPI = 300


def _save_figure(
    plot: Axes, basedir, problem, cls_name, acc_name, dataset_name, plot_type
):
    exts = [
        "svg",
        "png",
    ]
    plotsubdir = "all" if dataset_name == "*" else dataset_name
    files = [
        get_plots_path(
            basedir, problem, cls_name, acc_name, plotsubdir, plot_type, ext=e
        )
        for e in exts
    ]
    for f in files:
        os.makedirs(Path(f).parent, exist_ok=True)
        plot.figure.savefig(f, bbox_inches="tight", dpi=DPI)
    plot.figure.clear()


def _config_legend(plot: Axes):
    plot.legend(title="")
    sns.move_legend(plot, "lower center", bbox_to_anchor=(1, 0.5), ncol=1)


def plot_diagonal(
    df: pd.DataFrame,
    cls_name,
    acc_name,
    dataset_name,
    *,
    basedir="results",
    problem="binary",
    file_name=None,
    **kwargs,
):
    plot = sns.relplot(
        data=df,
        kind="scatter",
        x="true_accs",
        y="estim_accs",
        hue="method",
        alpha=0.2,
        aspect=1,
        facet_kws=dict(xlim=(0, 1), ylim=(0, 1)),
    )
    for ax in plot.axes.flat:
        ax.axline((0, 0), slope=1, color="black", linestyle="--", linewidth=1)

    sns.move_legend(
        plot,
        "lower center",
        bbox_to_anchor=(0.78, 0.5),
        ncol=kwargs.get("legend_ncol", 1),
    )
    plot.legend.set_title("")
    plot.legend.set_frame_on(True)
    for lh in plot.legend.legend_handles:
        lh.set_alpha(1)
        lh.set_markersize(8)

    if "x_label" in kwargs:
        plot.set_xlabels(kwargs["x_label"])
    if "y_label" in kwargs:
        plot.set_ylabels(kwargs["y_label"])

    return _save_figure(
        plot=plot,
        basedir=basedir,
        problem=problem,
        cls_name=cls_name,
        acc_name=acc_name,
        dataset_name=dataset_name,
        plot_type="diagonal" if file_name is None else file_name,
    )


def plot_diagonal_grid(
    df: pd.DataFrame,
    cls_name,
    acc_name,
    dataset_names,
    *,
    basedir="results",
    problem="binary",
    file_name=None,
    n_cols=1,
    x_label="true accs.",
    y_label="estim. accs.",
    aspect=1,
    xticks=None,
    yticks=None,
    xtick_vert=False,
    hspace=0.1,
    wspace=0.1,
    legend_bbox_to_anchor=(1, 0.5),
    **kwargs,
):
    plot = sns.FacetGrid(
        df,
        col="dataset",
        col_wrap=n_cols,
        hue="method",
        xlim=(0, 1),
        ylim=(0, 1),
        aspect=aspect,
    )
    plot.map(
        sns.scatterplot, "true_accs", "estim_accs", alpha=0.2, s=20, edgecolor=None
    )
    for ax in plot.axes.flat:
        ax.axline((0, 0), slope=1, color="black", linestyle="--", linewidth=1)
        if xtick_vert:
            ax.tick_params(axis="x", labelrotation=90, labelsize=10)
            ax.tick_params(axis="y", labelsize=10)
        if xticks is not None:
            ax.set_xticks(xticks)
        if yticks is not None:
            ax.set_yticks(yticks)

    plot.figure.subplots_adjust(hspace=hspace, wspace=wspace)
    plot.set_titles("{col_name}")

    plot.add_legend(title="")
    sns.move_legend(
        plot,
        "lower center",
        bbox_to_anchor=legend_bbox_to_anchor,
        ncol=kwargs.get("legend_ncol", 1),
    )
    for lh in plot.legend.legend_handles:
        lh.set_alpha(1)
        lh.set_sizes([100])

    plot.set_xlabels(x_label)
    plot.set_ylabels(y_label)

    return _save_figure(
        plot=plot,
        basedir=basedir,
        problem=problem,
        cls_name=cls_name,
        acc_name=acc_name,
        dataset_name="grid",
        plot_type="diagonal" if file_name is None else file_name,
    )


def plot_shift(
    df: pd.DataFrame,
    cls_name,
    acc_name,
    dataset_name,
    *,
    n_bins=20,
    basedir="results",
    problem="binary",
    file_name=None,
    linewidth=1,
    **kwargs,
):
    # binning on shift values
    df.loc[:, "shifts_bin"] = get_binned_values(df, "shifts", n_bins)

    plot = sns.lineplot(
        data=df,
        x="shifts_bin",
        y="acc_err",
        hue="method",
        estimator="mean",
        errorbar=None,
        linewidth=linewidth,
    )

    _config_legend(plot)
    if "x_label" in kwargs:
        plot.set_xlabel(kwargs["x_label"])
    if "y_label" in kwargs:
        plot.set_ylabel(kwargs["y_label"])
    return _save_figure(
        plot=plot,
        basedir=basedir,
        problem=problem,
        cls_name=cls_name,
        acc_name=acc_name,
        dataset_name=dataset_name,
        plot_type="shift" if file_name is None else file_name,
    )


# def plot_delta(
#     df: pd.DataFrame,
#     cls_name,
#     acc_name,
#     dataset_name,
#     *,
#     bins=10,
#     basedir=None,
#     stdev=False,
# ):
#     plot = sns.lineplot(
#         data=df,
#         x="prevs",
#         y="acc_err",
#         hue="method",
#         estimator="mean",
#         errorbar=("sd" if stdev else None),
#     )

#     _config_legend(plot)
#     return _save_figure(
#         plot, basedir, cls_name, acc_name, dataset_name, "stdev" if stdev else "delta"
#     )
