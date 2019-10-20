# import packages
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.ticker as mticker
from matplotlib import gridspec
from matplotlib import rcParams

rcParams['mathtext.default'] = 'regular'

# # fix on times new roman font
# del matplotlib.font_manager.weight_dict['roman']
# matplotlib.font_manager._rebuild()

COLOR_TABLE = {'base': sns.xkcd_rgb["pale red"], 'separated': sns.xkcd_rgb["sea blue"]}
COLOR_LIST = ['#C96A50', '#3E9AA3', '#3E9BA3']
PLOT_SPECS = {'icc':{'ylabel':'Temperature [C]', 'xlabel':'Heat Load [kW]', 'ylim':(0,50)},
              'carnot':{'ylabel':'Carnot factor [-]', 'xlabel':'Heat Load [kW]'}}

def plot_base_and_separated(path, t, plot_type, model_name):
    # figure size
    plt.figure(figsize=(8, 7))
    ax1 = plt.subplot()
    # plot the lines
    line_types = ['base', 'separated']
    for line_type in line_types:
        x, y = load_data_from_txt(path, plot_type, line_type, model_name, t)
        ax1.plot(x, y, '-', color=COLOR_TABLE[line_type], label=line_type)

    # save the figure
    set_plot_parameters(ax1, PLOT_SPECS[plot_type])
    fig1 = plt.gcf()
    os.chdir("..\\")
    print('saving fig to...', os.path.abspath(os.curdir))
    fig1.savefig(plot_type + '_' + model_name + '_t' + str(t) + '_DefaultHeatCascade.png', transparent=True)
    return

##===================
## general functions
##===================

def set_plot_parameters(ax1, plot_specs):
    fontname = 'Times New Roman'
    fontsize = 18
    # set the legend
    ax1.legend(loc='lower left', shadow=False, fancybox=True,
               fontsize=fontsize, prop={'family': 'Times New Roman', 'size': str(fontsize)})
    # set x and y range
    # plt.set_xlim([-766.00311044128,8090.8964687342])
    ax1.set(ylim=plot_specs['ylim'])
    # format ticks
    plt.xticks(fontname=fontname, fontsize=fontsize)
    plt.yticks(fontname=fontname, fontsize=fontsize)
    for label in ax1.xaxis.get_majorticklabels():
        label.set_fontsize(fontsize)
        label.set_fontname(fontname)
    for label in ax1.yaxis.get_majorticklabels():
        label.set_fontsize(fontsize)
        label.set_fontname(fontname)
    # set the axis labels
    ax1.set_ylabel(plot_specs['ylabel'], fontsize=fontsize, color='black', fontname=fontname, fontweight='normal')
    ax1.set_xlabel(plot_specs['xlabel'], fontsize=fontsize, color='black', fontname=fontname, fontweight='normal')
    # tight layout prevents axis title overlapping
    plt.tight_layout(pad=1, w_pad=3, h_pad=1.0)
    return


def load_data_from_txt(path, plot_type, line_type, model_name, t):
    os.chdir(path)
    if model_name == '':
        file_name = plot_type + '_' + line_type + '_m_loc_loc1_t' + str(t) + '_c1_DefaultHeatCascade.txt'
    else:
        file_name = plot_type + '_' + line_type + '_m_' + model_name + '_loc_loc1_t' + str(t) + '_c1_DefaultHeatCascade.txt'
    data = np.genfromtxt(file_name, delimiter=' ')
    # x and y axes
    x = data[:, 0]
    y = data[:, 1]
    return x, y


def main():
    plot_type = 'icc'
    model_name = 'chillers'

    # path
    # folder_layers = ['E:\\HCS_results_1003',
    #                  'WTP_CBD_m_WP1_OFF', 'B005_1_24', 'base_3for2',
    #                  'run', 's_001', 'plots',
    #                  'carnot', 'models']
    folder_layers = ['E:\\OSMOSE_projects\\HCS_mk\\results\\HCS_base','run_021_OFF_B001_1_168',
                     's_001\\plots\\' + plot_type, 'models']
    path_to_folder = os.path.join('', *folder_layers)

    # plot specifications


    # plotting
    # for t in np.arange(1,25,1):
    for t in [146]:
        plot_base_and_separated(path_to_folder, t, plot_type, model_name)



if __name__ == '__main__':
    main()