from FACS_Visualization import WorkspaceAnalysis
import pandas as pd
import json
#sample_ids, gate_ids, channels, stained_channels, main_population, positive_population_gate_names, positive_population_gate_path, keywords
attribute_names = ['sample_ids', 'gate_ids', 'channels', 'stained_channels', 'main_population', 'positive_population_gate_names', 'positive_population_gate_path', 'keywords']
function_names = ['sample_overview', 'positive_populations', 'gmfi_all_raw', 'gmfi_all_comp', 'gmfi_stained_raw', 'gmfi_stained_comp', 'events_per_sample']

attribute_dict = {}
for x in attribute_names:
    file_name = "data/test_WorkspaceAnalysis/Correct_result_files/" + x + ".json"
    with open(file_name, 'r') as f:
        temp = json.load(f)
    f.close()
    attribute_dict[x] = temp

temp_list = []
for x in attribute_dict["gate_ids"]:
    new_val = (x[0], tuple(x[-1]))
    temp_list.append(new_val)
attribute_dict["gate_ids"] = temp_list

attribute_dict["main_population"] =  (attribute_dict["main_population"][0], tuple(attribute_dict["main_population"][1]))
attribute_dict["positive_population_gate_names"] = tuple(attribute_dict["positive_population_gate_names"])
attribute_dict["positive_population_gate_path"] = tuple(attribute_dict["positive_population_gate_path"])

function_dict = {}
for x in function_names:
    file_name = "data/test_WorkspaceAnalysis/Correct_result_files/" + x + ".csv"
    function_dict[x] = pd.read_csv(file_name, index_col=[0])

wsp = "data/test_WorkspaceAnalysis/Test_WorkspaceAnalysis_wsp_file.wsp"
samples = "data/test_WorkspaceAnalysis/FCS_files"

test_workspace = WorkspaceAnalysis.Workspace(wsp_file=wsp, samples_directory=samples, main_gate='CD8+')

def test_sample_ids():
    assert test_workspace.sample_ids == attribute_dict["sample_ids"]

def test_gate_ids():
    assert test_workspace.gate_ids == attribute_dict["gate_ids"]

def test_channels():
    assert test_workspace.channels == attribute_dict["channels"]

def test_stained_channels():
    assert test_workspace.stained_channels == attribute_dict["stained_channels"]

def test_main_population():
    assert test_workspace.main_population == attribute_dict["main_population"]

def test_positive_population_gate_names():
    assert test_workspace.positive_population_gate_names == attribute_dict["positive_population_gate_names"]

def test_positive_population_gate_path():
    assert test_workspace.positive_population_gate_path == attribute_dict["positive_population_gate_path"]

def test_keywords():
    assert test_workspace.keywords == attribute_dict["keywords"]

def test_sample_overview():
    pd.testing.assert_frame_equal(test_workspace.sample_overview(), function_dict["sample_overview"])

def test_positive_populations():
    pd.testing.assert_frame_equal(test_workspace.positive_populations(), function_dict["positive_populations"])

def test_gmfi_all_raw():
    pd.testing.assert_frame_equal(test_workspace.gmfi(channels='All', data_source='raw'), function_dict["gmfi_all_raw"])

def test_gmfi_all_comp():
    pd.testing.assert_frame_equal(test_workspace.gmfi(channels='All', data_source='comp'), function_dict["gmfi_all_comp"])

def test_gmfi_stained_raw():
    pd.testing.assert_frame_equal(test_workspace.gmfi(channels='Stained', data_source='raw'), function_dict["gmfi_stained_raw"])

def test_gmfi_stained_comp():
    pd.testing.assert_frame_equal(test_workspace.gmfi(channels='Stained', data_source='comp'), function_dict["gmfi_stained_comp"])

def test_events_per_sample():
    pd.testing.assert_frame_equal(test_workspace.events_per_sample(test_workspace.sample_ids[0]), function_dict["events_per_sample"])
