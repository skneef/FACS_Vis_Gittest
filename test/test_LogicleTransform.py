from FACS_Visualization import LogicleTransform
import flowkit as fk
import numpy as np
import pandas as pd
import pytest
import unittest

data_sample_fk = fk.Sample("data/test_LogicleTransform/Sub_sample_fcs_test.fcs", cache_original_events=True)
data_sample_df = data_sample_fk.as_dataframe(source='orig')
data_sample_channel = data_sample_df.iloc[:,7]
data_sample_channel_transformed = np.loadtxt("data/test_LogicleTransform/channel_trans_test.csv", delimiter=',').tolist()

default_axis_primary = pd.read_csv("data/test_LogicleTransform/default_axis_primary.csv", index_col=[0]).fillna('')
default_axis_secondary = pd.read_csv("data/test_LogicleTransform/default_axis_secondary.csv", index_col=[0]).fillna('')
default_axis_tertiary = pd.read_csv("data/test_LogicleTransform/default_axis_tertiary.csv", index_col=[0]).fillna('')
sample_axis_primary = pd.read_csv("data/test_LogicleTransform/sample_axis_primary.csv", index_col=[0]).fillna('')
sample_axis_secondary = pd.read_csv("data/test_LogicleTransform/sample_axis_secondary.csv", index_col=[0]).fillna('')
sample_axis_tertiary = pd.read_csv("data/test_LogicleTransform/sample_axis_tertiary.csv", index_col=[0]).fillna('')
decimal_check = 10

def test_calculate_parameters():
    assert LogicleTransform.calculate_parameters() == (262144, 10.361632918473207, 0.5407300390241692, 0, 1.5586579402633183)

def test_calculate_parameters_sample():
    r_test = data_sample_channel.min()
    assert LogicleTransform.calculate_parameters(r=r_test) == (262144, 10.361632918473207, 0.705339412972315, 0, 1.7421258474073675)

def test_calculate_logicle_sample():
    r_test = data_sample_channel.min()
    t, m, w, a, p = LogicleTransform.calculate_parameters(r=r_test)
    logicles = []
    for x in data_sample_channel:
        logicles.append(LogicleTransform.calculate_logicle(t, m, w, a, p, x))
    assert logicles == data_sample_channel_transformed

def test_axis_scale():
    t, m, w, a, p = LogicleTransform.calculate_parameters()
    primary, secondary, tertiary = LogicleTransform.axis_scale(t, m, w, a, p)
    pd.testing.assert_frame_equal(primary, default_axis_primary)
    pd.testing.assert_frame_equal(secondary, default_axis_secondary)
    pd.testing.assert_frame_equal(tertiary, default_axis_tertiary)


def test_axis_scale_sample():
    r_test = data_sample_channel.min()
    h_test = data_sample_channel.max()
    t, m, w, a, p = LogicleTransform.calculate_parameters(r=r_test)
    primary, secondary, tertiary = LogicleTransform.axis_scale(t, m, w, a, p, min=r_test, max=h_test)
    pd.testing.assert_frame_equal(primary, sample_axis_primary)
    pd.testing.assert_frame_equal(secondary, sample_axis_secondary)
    pd.testing.assert_frame_equal(tertiary, sample_axis_tertiary)
