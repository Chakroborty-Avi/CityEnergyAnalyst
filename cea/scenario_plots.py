"""
scenario_plots.py

Create a list of plots for comparing multiple scenarios.
"""
import os
import inputlocator
import matplotlib.pyplot as plt
import pandas as pd


def plot_scenarios(scenarios_root, output_file):
    """
    List each scenario in the folder `scenario_root` and plot demand and lca (operations, embodied) data.

    :param scenarios_root: A folder containing scenario folders.
    :param output_file: The filename (pdf) to save the results as.
    :return: (None)
    """
    locators = [inputlocator.InputLocator(os.path.join(scenarios_root, scenario)) for scenario in
                os.listdir(scenarios_root) if os.path.isdir(os.path.join(scenarios_root))]

    plot_config = {
        'Demand': {'columns': ['Ef_MWhyr', 'QHf_MWhyr', 'QCf_MWhyr'],
                   'titles': ['Ef_MWhyr', 'QHf_MWhyr', 'QCf_MWhyr'],
                   'locator_method': 'get_total_demand'},
        'LCA Embodied': {'columns': ['pen_MJm2', 'pen_GJ', 'ghg_kgm2', 'ghg_ton'],
                         'titles': ['pen_MJm2', 'pen_GJ', 'ghg_kgm2', 'ghg_ton'],
                         'locator_method': 'get_lca_embodied'},
        'LCA Operation': {'columns': ['pen_MJm2', 'pen_GJ', 'ghg_kgm2', 'ghg_ton'],
                         'titles': ['pen_MJm2', 'pen_GJ', 'ghg_kgm2', 'ghg_ton'],
                         'locator_method': 'get_lca_operation'},
    }

    nrows = sum(len(plot_config[prefix]['columns']) for prefix in plot_config.keys())
    fig, axes = plt.subplots(nrows=nrows, figsize=(10, 30))

    dfs = {}
    for prefix in plot_config.keys():
        dfs.update(read_scenario_data(locators, prefix, plot_config[prefix]))

    for i, key in enumerate(sorted(dfs.keys())):
        dfs[key].boxplot(ax=axes[i], sym='')
        axes[i].set_title(key)

    fig.subplots_adjust(hspace=0.5)

    # save to pdf
    plt.savefig(output_file)
    plt.clf()
    plt.close()


def read_scenario_data(locators, prefix, config):
    dfs = {'%s:%s' % (prefix, key): pd.DataFrame() for key in config['columns']}
    for locator in locators:
        scenario_name = os.path.basename(locator.scenario_path)
        data_path = getattr(locator, config['locator_method'])()
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            for key in config['columns']:
                df_name = '%s:%s' % (prefix, key)
                dfs[df_name][scenario_name] = df[key]
    return dfs


def test_plot_scenarios():
    output_file = os.path.expandvars(r'%TEMP%\scenario_plots.pdf')
    scenarios_root = r'c:\reference-case'
    plot_scenarios(scenarios_root, output_file)
    print 'plot_scenarios succeeded.'

if __name__ == '__main__':
    test_plot_scenarios()