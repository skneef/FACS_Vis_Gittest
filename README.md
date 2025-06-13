# FACS_Visualization

* [Overview](#overview)
* [Installation](#installation)
* [Tutorial](#tutorial)
* [Features](#features)
* [Modules](#modules)
  * [WorkspaceAnalysis](#workspaceanalysis)
  * [LogicleTransform](#logicletransform)
  * [Graphs](#graphs)



## Overview

FACS_Visualization is a python toolkit for flow cytometry analysis and visualization. This package allows for singular and batch analysis of flow cytometry data as well as to create singular and batch dotplots, histograms and boxplots. This package is to be used in combination with FlowJo 10 workspace files and FCS files. It is also based on the package FlowKit.

## Installation
FACS_Visualization can be installed directly from Github, or by downloading the package [here](https://github.com/skneef/FACS_Visualization_Package/tree/master/dist/facs_visualization_package-0.0.1.tar.gz) and installing the package from the local drive.


## Tutorial
For a quick start, you can use the [Jupyter Notebook template file](https://github.com/skneef/FACS_Visualization_Package/tree/master/Template_files) and follow the steps below:

### Set-up
**Step 1:**

This will be the only step which requires input directly into the code. You need to enter the path of the WSP file and the path of the directory containing all the FCS files associated with the WSP file.
After running this step, you need to select which gate will be considered the main gate from which information will be retrieved.
![step_1](https://github.com/skneef/FACS_Visualization_Package/blob/master/data/Images/step_1.png)

**Step 2:**

After running this step, you need to select which keywords you have used to differentiate between different samples.
![step_2](https://github.com/skneef/FACS_Visualization_Package/blob/master/data/Images/step_2.png)

**Step 3:**

After running this step, you have finished the setup and can choose to make either dotplots, histograms, or boxplots.
![step_3](https://github.com/skneef/FACS_Visualization_Package/blob/master/data/Images/step_3.png)

### Dotplots
**Step 1:**

Select from which files you would like a dotplot, both the file name and chosen keywords will be displayed.
![step_4](https://github.com/skneef/FACS_Visualization_Package/blob/master/data/Images/step_4.png)

**Step 2:**

Select which value you would like displayed on the x-axis and y-axis.
![step_5](https://github.com/skneef/FACS_Visualization_Package/blob/master/data/Images/step_5.png)

**Step 3:**

This will return the dotplots. The title of the dotplots will be the file name and chosen keywords.
![step_6](https://github.com/skneef/FACS_Visualization_Package/blob/master/data/Images/step_6.png)

### Histograms
**Step 1:**

Select from which files you would like a dotplot, both the file name and chosen keywords will be displayed.
Also select which value you would like displayed on the x-axis.

If multiple files were selected, chose if you want a seperate figure for each file (Separate), or display them on the same figure (Together)
![step_7](https://github.com/skneef/FACS_Visualization_Package/blob/master/data/Images/step_7.png)

**Step 2:**

This will return the histograms. If the histograms are on seperate figures, the title will be the file name and chosen keywords. If the histograms are on the same figure, the title will be the x-value and a legend will be added below the figure.
![step_8](https://github.com/skneef/FACS_Visualization_Package/blob/master/data/Images/step_8.png)

### Boxplots
**Step 1:**

Select the y-axis value and based on which keyword the samples should be divided.
![step_9](https://github.com/skneef/FACS_Visualization_Package/blob/master/data/Images/step_9.png)

**Step 2:**

Select based on which keyword the samples should be grouped.
Also select if a legend is desired.
![step_10](https://github.com/skneef/FACS_Visualization_Package/blob/master/data/Images/step_10.png)

**Step 3:**

This will return the boxplot. The title will be the x-value.
![step_11](https://github.com/skneef/FACS_Visualization_Package/blob/master/data/Images/step_11.png)

## Features

* Read FCS and FlowJo Workspace files
* Analysis of FCS data
  * Calculate positive populations
  * Calculate gMFI
* Visualize FCS data
  * Dotplots
  * Histograms
  * Boxplots to compare multiple samples

## Modules
### WorkspaceAnalysis
The first module is WorkspaceAnalysis. This module contains the class Workspace which filters and analysis the workspace from the program FlowJo in combination with the associated FCS files. This module is largely based on the package Flowkit, but heavily simplified, to allow for more easy use. Furthermore, it can also calculate the positive populations and gMFI.

<div style="background-color:rgba(250, 230, 7, 1); color:red "> 
FACS_Visualization.WorkspaceAnalysis.Workspace(wsp_file, samples_directory=None, ignore_missing_samples=True, find_fcs_files=False, main_gate=None)
</div>

> **Parameters**

* **wsp_file**: string/path, _required_  
    Path to the .wsp file. The workspace file originating from FlowJo


* **sample_directory**: string/path, _default_ None  
    Path to the directory containing the .fcs files. Only FCS files mathing the ones referenced in the .wsp file will be retained


* **ignore_missing_samples**: bool, _default_ True  
    Controls behaviour for missing FCS files. If False, gives warning when missing .FCS files found in the Workspace


* **find_fcs_files**: bool, _default_ False  
    Controls whether to search for FCS files based on parameters from the FlowJo workspace file


* **main_gate**: string, _default_ None  
    Name of the main gate.The gate name of the population of interest. For example, the gate after which only live, single cells are selected

> **Attributes**

- **sample_ids**  
    List of the sample ids
- **gate_ids**  
    List of the gate ids in format (gate_name, (gate_path))
- **channels**  
    List of all channels
- **stained_channels**  
    List of all channels that measured a specific fluorphore
- **main_population**  
    Gate id of the main gate in format (gate_name, (gate_path))
- **positive_population_gate_names**  
    Gate names of the gates following the main_population
- **positive_population_gate_path**  
    Gate path of the positive_population_gate_names
- **keywords**  
    List of all keywords present in the Workspace
- **count**
    Dataframe with the number of events per sample
- **minimum_count**
    Minimum amount of events present

> **Methods**

<div style="background-color:rgba(250, 230, 7, 1); color:red "> 
Workspace.sample_overview(keywords=None)
</div>

Returns a pandas.DataFrame listing all sample ids. If keywords are specified, will also list all keywords of each sample id

>    Parameters:  
- **keywords**: string, 'All', list of strings, _default_ None  
  Returns the specified keywords of all sample ids per column

<div style="background-color:rgba(250, 230, 7, 1); color:red "> 
Workspace.positive_populations(keywords=None)
</div>

Returns a pandas.DataFrame listing all sample ids and the population fraction for all positive population gates.If keywords are specified, will also list the specified keywords of each sample id.
 
>    Parameters:  
- **keywords**: string, 'All', list of strings, default None  
  Returns the specified keywords of all sample ids per column

<div style="background-color:rgba(250, 230, 7, 1); color:red "> 
Workspace.gmfi(channels='All', data_source='comp', keywords=None)
</div>

Returns a pandas.DataFrame listing all sample ids and the gMFI for the specified channels of the main population.If keywords are specified, will also list the specified keywords of each sample id.
 
>    Parameters:  
- **channels**:{'All', 'Stained'}, default 'All'  
   Determines if the gMFI of all channels or of only the channels that measured a fluorphore are returned
- **data_source**: {'comp', 'raw'}, default 'comp'  
   Determines if the gMFI is calculated based on the raw values, or the compensated values.
- **keywords**: string, 'All', list of strings, default None  
   Returns the specified keywords of all sample ids per column

<div style="background-color:rgba(250, 230, 7, 1); color:red "> 
Workspace.events_per_sample(sample_ID, channels='All', data_source='comp')
</div>

Returns a pandas.DataFrame with the values of all events for the specified channels of the main population.

> Parameters:  
- **sample_id**: string  
The sample id for which to return the pandas.DataFrame
- **channels**: {'All', 'Stained'}, default 'All'  
Determines if events of all channels or of only the channels that measured a fluorphore are returned
- **data_source**: {'comp', 'raw'}, default 'comp'  
Determines if the raw or compensated values of the events are returned

<div style="background-color:rgba(250, 230, 7, 1); color:red "> 
Workspace.events_per_channel(channel, samples='All', data_source='comp')
</div>

> Parameters:  
- **channel**: string  
The channel for which to return the pandas.DataFrame
- **samples**: {'All', list}, default 'All'
Determines if events of all samples or of only the samples listed are returned
- **data_source**: {'comp', 'raw'}, default 'comp'  
Determines if the raw or compensated values of the events are returned

### LogicleTransform
The next module is LogicleTransform. This module is to transform values to a logicle scale and to generate the associated axis scale using the same parameters. The module is based on the follow two papers:

- Parks, D.R., Roederer, M. and Moore, W.A. (2006), A new “Logicle” display method avoids deceptive effects of logarithmic scaling for low signals and compensated data. Cytometry, 69A: 541-551. doi: 10.1002/cyto.a.20258
- Moore WA, Parks DR. Update for the logicle data scale including operational code implementations. Cytometry A. 2012 Apr;81(4):273-7. doi: 10.1002/cyto.a.22030. Epub 2012 Mar 12. PMID: 22411901; PMCID: PMC4761345.

<div style="background-color:rgba(250, 230, 7, 1); color:red "> 
FACS_Visualization.LogicleTransform.calculate_logicle(t, m, w, a, p, s)
</div>

Transforms the value (s) into a logicle value using parameters t, m, w, a, and p

> **Parameters**

* **t**: {int, float}, _required_  
    Maximum of the potential range of dataset
* **m**: {int, float}, _required_  
    The width over which the dataset is spread in natural log units
* **w**: {int, float}, _required_  
    The width of the linear range
* **a**: {int, float}, _required_  
    Additional negative range to be included in natural log units
* **p**: {int, float}, _required_  
    Secondary parameter based on w to reduce stress on calculations
* **s**: {int, float}, _required_  
    Value to transform

> **Returns**

* **Logicle**: {float}  
    The transformed value of **s**

<div style="background-color:rgba(250, 230, 7, 1); color:red "> 
FACS_Visualization.LogicleTransform.calculate_parameters(T=262144, M=4.5, r=100)
</div>

Calculates the parameters needed to calculate the logicle value

> **Parameters**

* **T**: {int, float}, _required_, default (1<<18)  
    Maximum of the potential range of dataset in bits. Default is an 18 bit data range (262144). It is recommended to use the default.
*  **M**: {int, float}, _required_, default (4.5)
    The width over which the dataset is spread in decades. Increase in case of a larger spread of data, and decrease in case of a smaller spread of data
*  **r**: {int, float}, _required_, default (100)
    The smallest value in the dataset. Recommended to use the smallest value of the dataset

> **Returns**

* **t**: float   
    Maximum of the potential range of dataset
* **m**: float   
    The width over which the dataset is spread in natural log units
* **w**: float   
    The width of the linear range
* **a**: float   
    Additional negative range to be included in natural log units
* **p**: float   
    Secondary parameter based on w to reduce stress on calculations

<div style="background-color:rgba(250, 230, 7, 1); color:red "> 
FACS_Visualization.LogicleTransform.axis_scale(t, m, w, a, p, min=None, max=None)
</div>

Creates three dataframes to transform the scale of graph to a logicle scale including the correct ticks

> **Parameters**

* **t**: {int, float}, _required_  
    Maximum of the potential range of dataset
* **m**: {int, float}, _required_  
    The width over which the dataset is spread in natural log units
* **w**: {int, float}, _required_  
    The width of the linear range
* **a**: {int, float}, _required_  
    Additional negative range to be included in natural log units
* **p**: {int, float}, _required_  
    Secondary parameter based on w to reduce stress on calculations
* **min**: {int, float}, _default_ None  
    The smallest value in the dataset.  
* **max**: {int, float}, _default_ None  
    The largest value in the dataset.  

> **Returns**

* **main_axis_scale**: pandas.DataFrame  
    Contains the coordinates, labels, and ticks for large ticks (0, 10, 100, 1000, etc.)
* **sec_axis_scale**: pandas.DataFrame  
    Contains the coordinates and ticks for the medium ticks (5, 50, 500, 5000, etc)
* **ter_axis_scale**: pandas.DataFrame  
    Contains the coordinates and ticks for the small ticks (200, 300, 400, 600, etc)

### Graphs
The last module is Graphs. This module is to visualize data through graphs. 

<div style="background-color:rgba(250, 230, 7, 1); color:red "> 
FACS_Visualization.Graphs.dotplot(data, xvalue, yvalue, save=None, legend=False, logicle_axis="Both", xline=None, yline=None, xlim=None, ylim=None, title=None)
</div>

> **Parameters**

* **data**: pandas.DataFrame, _required_  
    The data used for the dotplot. It is recommended to use the Workspace.events_per_sample() method to generate this data
* **xvalue**: string, _required_  
    The xvalue of the dotplot. The column name of the data
* **yvalue**: string, _required_  
    The yvalue of the dotplot. The column name of the data
* **save**: string/path, _default_ None  
    The file name where the image will be saved. If None, will show the image instead of saving it.
* **legend**: bool, _default_ False  
    Controls whether to show the legend or not
* **logicle_axis**: {"Both", "x", "y", "None"}, _default_ "Both"  
    Controls whether to have the axis in a logicle scale, calculated using functions from the LogicleTransform module
* **xline**: {None, int, float}, _default_ None  
    Show an xline
* **yline**: {None, int, float}, _default_ None  
    Show an yline
* **xlim**: {None, (xmin, xmax)}, _default_ None  
    Set a limit for xmin and xmax
* **ylim**: {None, (ymin, ymax)}, _default_ None  
    Set a limit for ymin and ymax
* **title**: {None, str}, _default_ None
    Title for the graph.

<div style="background-color:rgba(250, 230, 7, 1); color:red "> 
FACS_Visualization.Graphs.histogram(data, save=None, legend=False, logicle_axis=True, xline=None, xlim=None, ylim=None, column="All", xaxis_label=None, legend_data=None, title=None)
</div>

> **Parameters**

* **data**: pandas.DataFrame, _required_  
    The data used for the dotplot. It is recommended to use the Workspace.events_per_channel() method to generate this data
* **save**: string/path, _default_ None  
    The file name where the image will be saved. If None, will show the image instead of saving it.
* **legend**: bool, _default_ False  
    Controls whether to show the legend or not.
* **logicle_axis**: bool, _default_ True  
    Controls whether to have the axis in a logicle scale, calculated using functions from the LogicleTransform module.
* **xline**: {None, int, float}, _default_ None  
    Show an xline.
* **xlim**: {None, (xmin, xmax)}, _default_ None  
    Set a limit for xmin and xmax.
* **ylim**: {None, (ymin, ymax)}, _default_ None  
    Set a limit for ymin and ymax.
* **column**: {"All", list}, _default_ "All"
    Whether to include all columns of the data. If using the method Workspace.events_per_channel(), this refers to which samples to use.
* **xaxis_label**: {None, str}, _default_ None
    Label for the xaxis.
* **legend_data**: {None, pandas.DataFrame}, _default_ None
    If legend is True, this data will be used to generate the legend.
* **title**: {None, str}, _default_ None
    Title for the graph.

<div style="background-color:rgba(250, 230, 7, 1); color:red "> 
FACS_Visualization.Graphs.boxplot(data, xvariable, yvalue, group, save=None, legend=False, yaxis_scale="Linear", xvariable2=None, x_control=None, title=None)
</div>

> **Parameters**

* **data**: pandas.DataFrame, _required_  
    The data used for the dotplot. It is recommended to use the Workspace.gmfi() method to generate this data
* **xvariable**: string, _required_
    The variable on which to compare the samples, recommended to use a keyword. The column name of the data
* **yvalue**: string, _required_  
    The yvalue of the boxplot. The column name of the data.
* **group**: string, _required_
    The variable on which to group the samples, recommended to use a keyword. The column name of the data
* **save**: string/path, _default_ None  
    The file name where the image will be saved. If None, will show the image instead of saving it.
* **legend**: bool, _default_ False  
    Controls whether to show the legend or not.
* **yaxis_scale**: {"Linear", "Log"}, _default_ "Linear"  
    Controls whether to have the axis in a linear or logarithmic scale.
* **xvariable2**: [None, string}, _default_ None
    The second variable on which to compare the samples, recommended to use a keyword. The column name of the data
* **x_control**: {None, string}, _default_ None  
    One of the values of the xvariable that should be considered control.
* **title**: {None, str}, _default_ None
    Title for the graph.

