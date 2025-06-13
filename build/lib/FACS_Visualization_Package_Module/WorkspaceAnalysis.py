import flowkit as fk
import numpy as np
import pandas as pd
import scipy.stats as sstats

class Workspace(object):

    def __init__(
            self,
            wsp_file,
            samples_directory=None,
            ignore_missing_samples=True,
            find_fcs_files=False,
            main_gate=None
    ):
        self.workspace = fk.Workspace(wsp_file_path=wsp_file, fcs_samples=samples_directory,
                                 ignore_missing_files=ignore_missing_samples, find_fcs_files_from_wsp=find_fcs_files)
        self.workspace.analyze_samples(verbose=False, use_mp=False)
        self.sample_ids = self.workspace.get_sample_ids()
        same_gates = []
        for samples in self.sample_ids[1:]:
            same_gates.append(self.workspace.get_gate_ids(self.sample_ids[0]) == self.workspace.get_gate_ids(samples))
        if all(same_gates):
            self.gate_ids = self.workspace.get_gate_ids(self.sample_ids[0])
        else:
            raise KeyError("Gates not the same for all samples")

        channels_pns = self.workspace.get_sample(self.sample_ids[0]).channels['pns'].to_list()
        channels_pnn = self.workspace.get_sample(self.sample_ids[0]).channels['pnn'].to_list()
        self.channels = []
        self.stained_channels = []
        for x in range(len(channels_pns)):
            if channels_pns[x] == "":
                self.channels.append(channels_pnn[x])
            else:
                self.channels.append(channels_pnn[x] + " " + channels_pns[x])
                self.stained_channels.append(channels_pnn[x] + " " + channels_pns[x])

        if main_gate is not None:
            if isinstance(main_gate, str):
                same_gate_names = []
                for x, y in self.gate_ids:
                    same_gate_names.append(x == main_gate)
                if same_gate_names.count(True) == 1:
                    main_gate = same_gate_names.index(True)
                elif same_gate_names.count(True) > 1:
                    raise KeyError("Multiple gates with the same name")
                else:
                    raise KeyError("No gates with the given name")
        else:
            main_gate = 0

        self.main_population = self.gate_ids[main_gate]
        self.positive_population_gate_names = list(zip(*self.gate_ids[main_gate + 1 :]))[0]
        self.positive_population_gate_path = list(zip(*self.gate_ids[main_gate + 1 :]))[1][0]
        self.keywords = self.workspace.get_keywords(self.sample_ids[0])
        self.analysis_report = self.workspace.get_analysis_report()
        self.count = self.analysis_report[self.analysis_report['level'] == main_gate + 1][['sample', 'count']]
        self.minimum_count = self.count['count'].min()

    def sample_overview(self, keywords=None):
        if keywords is not None:
            if type(keywords) == list:
                for key in keywords:
                    if key not in list(self.keywords.keys()):
                        raise KeyError("Keywords not available")
            else:
                if keywords not in list(self.keywords.keys()):
                    raise KeyError("Keywords not available")

        if keywords == None:
            cols = ["File"]
        elif type(keywords) == list:
            cols = ["File"] + keywords
        elif keywords == "All":
            cols = ["File"] + self.keywords.keys()
        else:
            cols = ["File", keywords]

        df_samples = pd.DataFrame(columns=cols)
        for sample in self.sample_ids:
            new_row = [sample]
            all_keywords = self.workspace.get_keywords(sample)
            if keywords is not None:
                if type(keywords) == list:
                    for key in keywords:
                        new_row.append(all_keywords[key])
                else:
                    new_row.append(all_keywords[keywords])

            df_samples.loc[len(df_samples)] = new_row
        return df_samples

    def positive_populations(self, keywords=None):
        cols = ["Sample name"] + list(self.positive_population_gate_names)
        df_positive_populations = pd.DataFrame(columns=cols)

        for sample in self.sample_ids:
            new_row = [sample]
            total_cells = list(
                self.workspace.get_gate_membership(sample_id=sample, gate_name=self.main_population[0])).count(True)
            for positive_gate in self.positive_population_gate_names:
                new_row.append(
                    list(self.workspace.get_gate_membership(sample_id=sample, gate_name=positive_gate)).count(
                        True) / total_cells)
            df_positive_populations.loc[len(df_positive_populations)] = new_row
        df_samples = self.sample_overview(keywords=keywords)
        df_positives = pd.merge(df_samples, df_positive_populations, on="Sample name")

        return df_positives

    def gmfi(self, channels="All", data_source="comp", keywords=None):
        channels_types = ["All", "Stained"]
        data_source_types = ["raw", "comp"]
        if channels not in channels_types:
            raise ValueError("Invalid channels. Expected one of: %s" % channels_types)
        if data_source not in data_source_types:
            raise ValueError("Invalid data source. Expected one of: %s" % data_source_types)
        if channels == "All":
            cols = ["File"] + list(self.channels)
            gmfi_channels = list(self.channels)
        elif channels == "Stained":
            cols = ["File"] + list(self.stained_channels)
            gmfi_channels = list(self.stained_channels)
        else:
            raise ValueError("Invalid channels. Expected one of: %s" % channels_types)

        df_gmfi = pd.DataFrame(columns=cols)

        for sample in self.sample_ids:
            new_row = [sample]
            gated_events = self.workspace.get_gate_events(sample, gate_name=self.main_population[0], source=data_source)
            for channel in gmfi_channels:
                new_row.append(sstats.gmean(gated_events.loc[(gated_events != 0).all(axis=1)][channel].abs().to_list()))

            df_gmfi.loc[len(df_gmfi)] = new_row

        df_samples = self.sample_overview(keywords=keywords)

        df_gmfi = pd.merge(df_samples, df_gmfi, on="File")

        return df_gmfi

    def events_per_sample(self, sample_ID, channels="All", data_source="comp"):
        channels_types = ["All", "Stained"]
        data_source_types = ["raw", "comp"]
        if sample_ID not in self.sample_ids:
            raise ValueError("Invalid sample_id")
        if channels not in channels_types:
            raise ValueError("Invalid channels. Expected one of: %s" % channels_types)
        if data_source not in data_source_types:
            raise ValueError("Invalid data source. Expected one of: %s" % data_source_types)

        gated_events = self.workspace.get_gate_events(sample_ID, gate_name=self.main_population[0], source=data_source).reset_index(drop=True)

        if channels == "Stained":
            gated_events = gated_events[self.stained_channels]

        return gated_events

    def events_per_channel(self, channel, samples="All", data_source="comp"):
        if channel not in self.channels:
            raise ValueError("Invalid channel.")
        if samples != "All":
            if type(samples) is not list:
                raise ValueError("Invalid samples. Expected a list")
            else:
                for x in samples:
                    if x not in self.sample_ids:
                        raise ValueError("Invalid sample_ids in samples.")
        data_source_types = ["raw", "comp"]
        if data_source not in data_source_types:
            raise ValueError("Invalid data source. Expected one of: %s" % data_source_types)

        if samples == "All":
            samples = self.sample_ids

        events = pd.DataFrame()
        for x in samples:
            sample_events = self.workspace.get_gate_events(x, gate_name=self.main_population[0], source=data_source).reset_index(drop=True)
            sample_events = sample_events.sample(n = self.minimum_count, random_state = 1, ignore_index=True, axis=0)
            sample_events = sample_events[channel]
            events[x] = sample_events

        return events
