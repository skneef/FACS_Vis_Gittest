Hello,

this is my first trial of making my code into a package usable by others


WorkspaceAnalysis
The first module is WorkspaceAnalysis. This module contains the class Workspace which filters and analysis the workspace
from the program FlowJo in combination with the associated FCS files. This module is largely based on the package
Flowkit, but heavily simplified, to allow for more easy use. Furthermore, it can also calculate the positive populations
and gMFI.

SanquinPackageModule.WorkspaceAnalysis.Workspace(
            wsp_file,
            samples_directory=None,
            ignore_missing_samples=True,
            find_fcs_files=False,
            main_gate=None
            )

Parameters:
wsp_file: string/path
    Path to the .wsp file
        The workspace file originating from FlowJo

sample_directory: string/path, default None
    Path to the directory containing the .fcs files
        Only FCS files mathing the ones referenced in the .wsp file will be retained

ignore_missing_samples: bool, default True
    Controls behaviour for missing FCS files
        If False, gives warning when missing .FCS files found in the Workspace

find_fcs_files: bool, default False
    Controls whether to search for FCS files based on parameters from the FlowJo workspace file

main_gate: string, default None
    Name of the main gate.
        The gate name of the population of interest. For example, the gate after which only live, single cells
        are selected

Attributes:
    - sample_ids
        List of the sample ids
    - gate_ids
        List of the gate ids in format (gate_name, (gate_path))
    - channels
        List of all channels
    - stained_channels
        List of all channels that measured a specific fluorphore
    - main_population
        Gate id of the main gate in format (gate_name, (gate_path))
    - positive_population_gate_names
        Gate names of the gates following the main_population
    - positive_population_gate_path
        Gate path of the positive_population_gate_names
    - keywords
        List of all keywords present in the Workspace

Methods:
sample_overview(keywords=None)
    Returns a pandas.DataFrame listing all sample ids. If keywords are specified, will also list all keywords of each sample id

    Parameters:
        keywords: string, 'All', list of strings, default None
            Returns the specified keywords of all sample ids per column

positive_populations(keywords=None)
    Returns a pandas.DataFrame listing all sample ids and the population fraction for all positive population gates.
    If keywords are specified, will also list the specified keywords of each sample id.

    Parameters:
        keywords: string, 'All', list of strings, default None
            Returns the specified keywords of all sample ids per column

gmfi(channels='All', data_source='comp', keywords=None)
    Returns a pandas.DataFrame listing all sample ids and the gMFI for the specified channels of the main population.
    If keywords are specified, will also list the specified keywords of each sample id.

    Parameters:
        channels: {'All', 'Stained'}, default 'All'
            Determines if the gMFI of all channels or of only the channels that measured a fluorphore are returned

        data_source: {'comp', 'raw'}, default 'comp'
            Determines if the gMFI is calculated based on the raw values, or the compensated values.

        keywords: string, 'All', list of strings, default None
            Returns the specified keywords of all sample ids per column

events_per_sample(sample_ID, channels='All', data_source='comp')
    Returns a pandas.DataFrame with the values of all events for the specified channels of the main population.

    Parameters:
        sample_id: string
            The sample id for which to return the pandas.DataFrame

        channels: {'All', 'Stained'}, default 'All'
            Determines if events of all channels or of only the channels that measured a fluorphore are returned

        data_source: {'comp', 'raw'}, default 'comp'
            Determines if the raw or compensated values of the events are returned


LogicleTransform
The next module is LogicleTransform. This module is to transform values to a logicle scale and to generate the
associated axis scale using the same parameters.
The module is based on the follow two papers:
    - Parks, D.R., Roederer, M. and Moore, W.A. (2006), A new “Logicle” display method avoids deceptive effects of
        logarithmic scaling for low signals and compensated data. Cytometry, 69A: 541-551. doi: 10.1002/cyto.a.20258
    - Moore WA, Parks DR. Update for the logicle data scale including operational code implementations. Cytometry A.
        2012 Apr;81(4):273-7. doi: 10.1002/cyto.a.22030. Epub 2012 Mar 12. PMID: 22411901; PMCID: PMC4761345.

LogicleTransform consists of three functions:
    1. calculate_logicle(t, m, w, a, p, s)
        - Transforms the value into a logicle value using parameters t, m, w, a, and p
            ∙ t : Maximum of the potential range of dataset
            ∙ m : The width over which the dataset is spread in natural log units
            ∙ w : The width of the linear range
            ∙ a : Additional negative range to be included in natural log units
            ∙ p : Secondary parameter based on w to reduce stress on calculations
            ∙ s : Value to transform
        - Parameters are calculated using calculate_parameters

    2. calculate_parameters(T=(1<<18), M=4.5, r=100)
        - Calculates the parameters needed to calculate the logicle value
        - Requires three inputs:
            ∙ T : Maximum of the potential range of dataset
                    ◦ Default is 262144 (top of an 18 bit data range)
                    ◦ Recommended to use default
            ∙ M : The width over which the dataset is spread in decades
                    ◦ Default is 4.5
                    ◦ Increase for larger spread of data
                    ◦ Decrease for smaller spread of data
            ∙ r : The smallest value in the dataset
                    ◦ Default is 100
                    ◦ Recommended to use the smallest value of the dataset

    3. axis_scale(t, m, w, a, p, min=None, max=None)
        - Creates three dataframes to transform the scale of graph to a logicle scale including the correct ticks
            ∙ main_axis_scale : Contains the coordinates, labels, and ticks for large ticks (0, 10, 100, 1000, etc)
            ∙ sec_axis_scale  : Contains the coordinates and ticks for the medium ticks (5, 50, 500, 5000, etc)
            ∙ ter_axis_scale  : Contains the coordinates and ticks for the small ticks (200, 300, 400, 600, etc)

Graphs
The last module is Graphs. This module is to visualize data through graphs. This module consists of three functions.

Dotplots

dotplot(
    data,
    xvalue,
    yvalue,
    save=None,
    legend=False,
    logicle_axis="Both",
    xline=None,
    yline=None,
    xlim=None,
    ylim=None
)

Parameters
    data: pandas.DataFrame
        The data used for the dotplot. It is recommended to use the Workspace.events_per_sample() method to generate
        this data

    xvalue: string
        The xvalue of the dotplot. The column name of the data

    yvalue: string
         The yvalue of the dotplot. The column name of the data

    save: string/path, default None
        The file name where the image will be saved. If None, will show the image instead of saving it.

    legend: bool, default False
        Controls whether to show the legend or not

    logicle_axis: {"Both", "x", "y", "None"}, default "Both"
        Controls whether to have the axis in a logicle scale, calculated using functions from the LogicleTransform module

    xline: {None, int, float}, default None
        Show an xline

    yline: {None, int, float}, default None
        Show an yline

    xlim: {None, (xmin, xmax)}, default None
        Set a limit for xmin and xmax

    ylim: {None, (ymin, ymax)}, default None
        Set a limit for ymin and ymax

