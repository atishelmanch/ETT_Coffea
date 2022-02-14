"""
Abraham Tishelman-Charny
17 November 2021

The purpose of this notebook is to plot quantities from ETTAnalyzer outputs.

Example commands:

python3 ETTPlot.py --variables oneMinusEmuOverRealvstwrADCCourseBinning  --plotTogether --fromParquet

python3 ETTPlot.py --variables oneMinusEmuOverRealvstwrADCCourseBinning --severities zero --times inTime --maxFiles 10000 --outputLocation "/eos/user/a/atishelm/www/EcalL1Optimization/PilotBeam2021/MinDelta0p5prime_WithOddPF_MultiFitReco/" --plotIndividuals
python3 ETTPlot.py --variables oneMinusEmuOverRealvstwrADCCourseBinning --severities zero --times inTime --maxFiles 100000 --outputLocation "/eos/user/a/atishelm/www/EcalL1Optimization/PilotBeam2021/MinDelta0p5prime_WithOddPF_MultiFitReco/" --plotTogether --fromParquet

python3 ETTPlot.py --directory /eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_MultifitRecoMethod_StripZeroingMode_WithOddPeakFinder_0p5PrimeODDweights/220210_094402/all_output/ --variables oneMinusEmuOverRealvstwrADCCourseBinning,EnergyVsTimeOccupancy --severities zero --times inTime --maxFiles 100 --outputLocation "/eos/user/a/atishelm/www/EcalL1Optimization/PilotBeam2021/MinDelta0p5prime_WithOddPF_MultiFitReco/" --plotIndividuals --plotTogether --fromParquet

python3 ETTPlot.py --directory /eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_weightsRecoMethod_StripZeroingMode_WithOddPeakFinder_0p5PrimeODDweights/220210_104615/all_output/ --variables oneMinusEmuOverRealvstwrADCCourseBinning,EnergyVsTimeOccupancy --severities zero --times inTime --maxFiles 10000 --outputLocation "/eos/user/a/atishelm/www/EcalL1Optimization/PilotBeam2021/MinDelta0p5prime_WithOddPF_WeightsReco/"
python3 ETTPlot.py --directory /eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_MultifitRecoMethod_StripZeroingMode_WithOddPeakFinder_0p5PrimeODDweights/220210_094402/all_output/ --variables oneMinusEmuOverRealvstwrADCCourseBinning,EnergyVsTimeOccupancy --severities zero --times inTime --maxFiles 10000 --outputLocation "/eos/user/a/atishelm/www/EcalL1Optimization/PilotBeam2021/MinDelta0p5prime_WithOddPF_MultiFitReco/"
python3 ETTPlot.py --directory /eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_MultifitRecoMethod_StripZeroingMode_WithOddPeakFinder_2p5PrimeODDweights/220209_125921/all_output/ --variables oneMinusEmuOverRealvstwrADCCourseBinning,EnergyVsTimeOccupancy --maxFiles 100 
"""

import numpy as np
import os 
import argparse 
import uproot 
import pickle
from matplotlib import pyplot as plt 

from python.ETTPlot_Tools import * 

import pyarrow as pa
import pyarrow.parquet as pq

parser = argparse.ArgumentParser()
# parser.add_argument("--directory", type = str, default = "NODIRECTORY", required=True, help = "Directory with input files")
parser.add_argument("--variables", type = str, default = "RealVsEmu", help = "Comma separated list of variables to plot") 
parser.add_argument("--times", type = str, default = "all,Early,inTime,Late,VeryLate", help = "Comma separated list of times to plot") 
parser.add_argument("--severities", type = str, default = "zero,three,four", help = "Comma separated list of severities to plot") 
parser.add_argument("--maxFiles", type = int, default = 1, help = "Max number of files to process")
parser.add_argument("--outputLocation", type = str, required = True, help = "Output directory for beautiful plots") 
parser.add_argument("--plotIndividuals", action="store_true", default = False, help = "Produce a plot for each selection")
parser.add_argument("--plotTogether", action="store_true", default = False, help = "Produce a plot for each selection")
parser.add_argument("--fromParquet", action="store_true", default = False, help = "Plot using parquet files")

# For real vs. emu plots:
# parser.add_argument("--plotRatio", action="store_true", default = False, help = "Produce a ratio plot of tagged / all TPs")
# parser.add_argument("--doSymLog", action="store_true", default = False, help = "Plot with symmetric log scale")
# parser.add_argument("--addPlotText", type = int, default = 1, help = "Add text on plot")
# parser.add_argument("--selections", type = str, default = "clean", help = "Comma separated list of selections to apply")
# parser.add_argument("--ymax", type = float, default = 256, help = "ymax")
# parser.add_argument("--xmax", type = float, default = 256, help = "xmax")
# parser.add_argument("--zmax", type = float, default = -1, help = "zmax")

args = parser.parse_args()

# directory = args.directory 

directories = [
    "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_MultifitRecoMethod_StripZeroingMode_WithoutOddPeakFinder_0p5PrimeODDweights/220210_104023/all_output/",
    "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_MultifitRecoMethod_StripZeroingMode_WithoutOddPeakFinder_2p5PrimeODDweights/220210_103954/all_output/",
    # "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_weightsRecoMethod_StripZeroingMode_WithOddPeakFinder_0p5PrimeODDweights/220210_104615/all_output/",
    "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_MultifitRecoMethod_StripZeroingMode_WithOddPeakFinder_0p5PrimeODDweights/220210_094402/all_output/",
    "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_MultifitRecoMethod_StripZeroingMode_WithOddPeakFinder_2p5PrimeODDweights/220209_125921/all_output/"
]

direc_ol_dict = {
    "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_MultifitRecoMethod_StripZeroingMode_WithoutOddPeakFinder_0p5PrimeODDweights/220210_104023/all_output/" : "/eos/user/a/atishelm/www/EcalL1Optimization/PilotBeam2021/MinDelta0p5prime_WithoutOddPF_MultiFitReco/",
    "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_MultifitRecoMethod_StripZeroingMode_WithoutOddPeakFinder_2p5PrimeODDweights/220210_103954/all_output/" : "/eos/user/a/atishelm/www/EcalL1Optimization/PilotBeam2021/MinDelta2p5prime_WithoutOddPF_MultiFitReco/",
    # "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_weightsRecoMethod_StripZeroingMode_WithOddPeakFinder_0p5PrimeODDweights/220210_104615/all_output/" : "/eos/user/a/atishelm/www/EcalL1Optimization/PilotBeam2021/MinDelta0p5prime_WithOddPF_WeightsReco/",
    "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_MultifitRecoMethod_StripZeroingMode_WithOddPeakFinder_0p5PrimeODDweights/220210_094402/all_output/" : "/eos/user/a/atishelm/www/EcalL1Optimization/PilotBeam2021/MinDelta0p5prime_WithOddPF_MultiFitReco/",
    "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Runs_346446_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeights_MultifitRecoMethod_StripZeroingMode_WithOddPeakFinder_2p5PrimeODDweights/220209_125921/all_output/" : "/eos/user/a/atishelm/www/EcalL1Optimization/PilotBeam2021/MinDelta2p5prime_WithOddPF_MultiFitReco/",    
}

variables = args.variables.split(',')
times = args.times.split(',')
severities = args.severities.split(',')
maxFiles = args.maxFiles 
#ol = args.outputLocation
plotIndividuals = args.plotIndividuals 
plotTogether = args.plotTogether
fromParquet = args.fromParquet

ol = "/eos/user/a/atishelm/www/EcalL1Optimization/PilotBeam2021/AllWorkingPoints/"

# For real vs. emu plots:
# zmax = args.zmax 
# ymax = args.ymax
# xmax = args.xmax 
# selections = args.selections.split(',')
# doSymLog = args.doSymLog 
# plotIndividuals = args.plotIndividuals
# plotRatio = args.plotRatio 
# addPlotText = args.addPlotText

if(__name__ == '__main__'):

    varLabelDict = {
        "realVsEmu": "realVsEmu",
        "EnergyVsTimeOccupancy" : "EnergyVsTimeOccupancy",
        "oneMinusEmuOverRealvstwrADCCourseBinning" : "oneMinusEmuOverRealvstwrADCCourseBinning"
    }

    # Make output directory if it doesn't exist 
    mkdirCmd = "mkdir -p {ol}".format(ol=ol)
    cpIndCmd = "cp {ol}/../index.php {ol}".format(ol=ol)
    print("$",mkdirCmd)
    os.system(mkdirCmd)
    print("$",cpIndCmd)
    os.system(cpIndCmd)

    # go through variables to plot 
    for variable in variables:
        varLabel = varLabelDict[variable]
        if(plotIndividuals):
            for direc in directories:
                print("direc:",direc)
                WP, PF, RECO = GetWorkingPointLabels(direc)

                direc_ol = direc_ol_dict[direc]

                for severity in severities:
                    print("On severity:",severity)
                    for time in times:
                        print("On time:",time)
                        if(time == "inTime" and severity == "three"):
                            print("Skipping in time severity three as they shouldn't exist by definition")
                            continue 
                        print("On Var: %s, Sev: %s, time: %s"%(variable, severity, time))
                        thisDirec = "%s/%s/%s/%s/"%(direc, variable, severity, time) # directory for a given variable, severity, time 
                        files = [f for f in os.listdir(thisDirec)]
                        n_files = len(files)
                        values_0 = pickle.load(open("%s/%s_sev%s_%s_values_0.p"%(thisDirec, variable, severity, time), "rb"))
                        values_1 = pickle.load(open("%s/%s_sev%s_%s_values_1.p"%(thisDirec, variable, severity, time), "rb"))
                        total_values = np.add(values_0, values_1)
                        for i in range(n_files):
                            if(i > maxFiles):
                                print("Max files reached: ",i)
                                break 
                            if(i == 0 or i == 1): continue 
                            if(i%100 == 0): print("on file %s / %s"%(i, n_files))

                            exec('thisValues = pickle.load(open("%s/%s_sev%s_%s_values_%s.p"%(thisDirec, variable, severity, time, i), "rb"))')  
                            total_values = np.add(total_values, thisValues)

                        exec("%s_%s_%s_values = np.copy(total_values)"%(variable, severity, time)) # copy with unique name to plot together on same plot later 
                        exec("These_Values = np.copy(total_values)") 
                        os.system("mkdir -p %s"%(direc_ol))
                        os.system("cp %s/../index.php %s"%(direc_ol, direc_ol))
                        averages, stdevs = MakeETTPlot(These_Values, variable, severity, time, direc_ol) # make plots and return averages 

                        # save averages and stdevs as parquet files (choosing parquet for fun / experience) to combine everything later 
                        # save averages for each case: var, WP, PF, RECO, Sev, Time

                        if(variable == "oneMinusEmuOverRealvstwrADCCourseBinning"):                                   

                            parquetOutDir = "output"
                            os.system("mkdir -p %s"%(parquetOutDir))
                            outName_averages = "%s/%s_%s_%s_%s_%s_%s_averages.parquet"%(parquetOutDir, variable, WP, PF, RECO, severity, time)
                            outName_stdevs = "%s/%s_%s_%s_%s_%s_%s_stdevs.parquet"%(parquetOutDir, variable, WP, PF, RECO, severity, time)

                            averages_table = pa.table({"data": averages})
                            stdevs_table = pa.table({"data": stdevs})
                            print("Saving parquet file:",outName_averages)   
                            print("Saving parquet file:",outName_stdevs)                   
                            pa.parquet.write_table(averages_table, outName_averages)                
                            pa.parquet.write_table(stdevs_table, outName_stdevs)    

                            exec("%s_%s_averages = np.copy(averages)"%(severity, time))
                            exec("%s_%s_stdevs = np.copy(stdevs)"%(severity, time))

        if(plotTogether):

            colorDict = {
                "all" : "blue",
                "Early" : "cyan",
                "inTime" : "green",
                "Late" : "orange",
                "VeryLate" : "red"
            }

            shapeDict = {
                "zero" : "o",
                "three" : "^",
                "four" : "s"
            }   

            error = 1 
            log = 1

            # plot average lines on same plots
            if(variable == "oneMinusEmuOverRealvstwrADCCourseBinning"):
                xbins, ybins = GetBins(variable)
                for time in times:
                    print("On time:",time)
                    for sev_i, severity in enumerate(severities):
                        print("On severity:",severity)
                        if(time == "inTime" and severity == "three"): 
                            print("Skipping in time severity 3")
                            continue     
                        shape = shapeDict[severity]
                        color = colorDict[time]
                        fig, ax = plt.subplots()
                        for direc in directories:
                            WP, PF, RECO = GetWorkingPointLabels(direc)                        

                            if(fromParquet):
                                parquetOutDir = "output/%s_%s_%s_%s/"%(variable, WP, PF, RECO)
                                os.system("mkdir -p %s"%(parquetOutDir))
                                averages_path = "%s/%s_%s_%s_%s_%s_%s_averages.parquet"%(parquetOutDir, variable, WP, PF, RECO, severity, time)
                                stdevs_path = "%s/%s_%s_%s_%s_%s_%s_stdevs.parquet"%(parquetOutDir, variable, WP, PF, RECO, severity, time)                            
                                averages_table = pq.read_table(averages_path)
                                stdevs_table = pq.read_table(stdevs_path)
                                data_averages = averages_table.to_pandas()
                                stdevs_averages = stdevs_table.to_pandas()

                                averages_ = data_averages.to_numpy().ravel()
                                stdevs_ = stdevs_averages.to_numpy().ravel()

                                # save values 
                                averages_path_txt = averages_path.replace(".parquet", ".txt")
                                stdevs_path_txt = stdevs_path.replace(".parquet", ".txt") 

                                np.savetxt(averages_path_txt, averages_, delimiter =', ')   
                                np.savetxt(stdevs_path_txt, stdevs_, delimiter =', ')                           

                            else:
                                exec("averages_ = np.copy(%s_%s_averages)"%(severity, time))
                                exec("stdevs_ = np.copy(%s_%s_stdevs)"%(severity, time))

                            energy_bins = xbins
                            energies_ = xbins
                            xmin_, xmax_ = xbins[0], xbins[-1]
                            centered_energy_bins_ = [ ((energy_bins[i+1] - energy_bins[i]) / 2.) + energy_bins[i] for i in range(len(energy_bins) - 1) ]
                            xerrors_ = [ ((energy_bins[i+1] - energy_bins[i]) / 2.) for i in range(len(energy_bins) - 1) ]   
                            
                            averages = np.array(averages_) 
                            stdevs = np.array(stdevs_) 
                            centered_energy_bins = np.array(centered_energy_bins_)
                            xerrors = np.array(xerrors_)

                            MASK = tuple([averages != -1])

                            centered_energy_bins = centered_energy_bins[MASK]
                            averages = averages[MASK]
                            stdevs = stdevs[MASK]  
                            xerrors = xerrors[MASK]

                            zero_errors = [0. for i in range(0, len(averages))]            
                
                            if(error):
                                labelReplaceDict = {
                                    "MinDelta": "$\delta_{min}$",
                                    "0p5prime" : "0.5$^\prime$",
                                    "2p5prime" : "2.5$^\prime$",
                                    "zero" : "0",
                                    "three" : "3",
                                    "four" : "4"
                                }
                                plotLabel = "Sev %s, %s, %s, %s, %s"%(severity, time, WP, PF, RECO)
                                for key in labelReplaceDict:
                                    val = labelReplaceDict[key]
                                    plotLabel = plotLabel.replace(key, val)
                                plt.scatter(x = centered_energy_bins, y = averages, label = plotLabel, s = 15)
                                plt.errorbar(x = centered_energy_bins, y = averages, xerr = xerrors, yerr = zero_errors, fmt = " ")  
                            else:
                                plt.scatter(x = energies, y = averages, label = plotLabel, s = 10, marker = shape, color = color)


                        plt.legend(loc = 'best', fontsize = 10)
                        plt.ylim(0, 1.01)
                        plt.xlim(xmin_, xmax_)
                        plt.xlabel("Real data TP Et (ADC)", fontsize=15)
                        # plt.ylabel("Average 1 - (Emulated / Real)", fontsize=15)
                        plt.ylabel("Average TP fraction subtracted", fontsize=15)
                        plt.grid()
                        plt.xticks(fontsize = 15)
                        plt.yticks(fontsize = 15)
                        upperRightText = "Pilot Beam 2021"
                        text_xmin = 0.135
                        Add_CMS_Header(plt, ax, upperRightText, text_xmin)
                        fig.tight_layout()
                        plt.savefig("%s/Sev_%s_%s_Average_%s_linear.png"%(ol, severity, time, varLabel), dpi = 300)
                        plt.savefig("%s/Sev_%s_%s_Average_%s_linear.pdf"%(ol, severity, time, varLabel), dpi = 300)   

                        if(log):
                            plt.ylim(0.001, 1)
                            plt.yscale('log')  
                            fig.tight_layout()
                            plt.savefig("%s/Sev_%s_%s_Average_%s_log.png"%(ol, severity, time, varLabel), dpi = 300)
                            plt.savefig("%s/Sev_%s_%s_Average_%s_log.pdf"%(ol, severity, time, varLabel), dpi = 300)    
                        plt.close()

    print("DONE")

    # Population fraction plots:
    """

    # The purpose of this cell is to produce plots of population of sev X timing divided by total 
    # Previous plots showed us, e.g., that we are good at zeroing very late spikes.
    # However, it would help to know what percentage of the total spikes are very late in order to 
    # begin to get an idea of how we can lower the overall spike rate, as a function of TP energy. 

    ##-- stack plots are used when the total is of important interest in addition to the per piece 
    ##-- in this case we already know the total is 1. Line plots may be more useful to show. 

    ##-- Parameters
    log = 0
    xmin, xmax = 1, 256
    lumi = "XXX" 
    isWide = 0

    ##-- One plot per severity 
    for severity in severities:
        print("severity:",severity)
        colors = ["C%s"%(i) for i in range(0,4)]
        fig, ax = plt.subplots()
        fig.set_size_inches(10, 7.5)
        for timing_i, timing in enumerate(timings):  
            if(timing == "inTime" and severity == "three"): continue
            print("timing:",timing)
            color = colors[timing_i]
            exec("N_all_entries_per_slice = np.copy(%s_N_entries_per_slice_all_timings)"%(severity))
            energy_bins = [1.0, 8.0, 16.0, 24.0, 32.0, 40.0, 48.0, 56.0, 64.0, 72.0, 80.0, 88.0, 96.0, 104.0, 112.0, 150.0, 256.0]
            centered_energy_bins_ = [ ((energy_bins[i+1] - energy_bins[i]) / 2.) + energy_bins[i] for i in range(len(energy_bins) - 1) ]
            centered_energy_bins = np.array(centered_energy_bins_)
            xerrors_ = [ ((energy_bins[i+1] - energy_bins[i]) / 2.) for i in range(len(energy_bins) - 1) ]  
            xerrors = np.array(xerrors_)        
            exec("N_entries = np.copy(%s_%s_N_entries_per_slice)"%(severity, timing))

            MASK = tuple([N_entries != 0])
            
            zero_errors_ = [0. for i in range(0, len(zero_Early_N_entries_per_slice))] 
            zero_errors = np.array(zero_errors_)
            
            centered_energy_bins = centered_energy_bins[MASK]
            xerrors = xerrors[MASK]
            zero_errors = zero_errors[MASK]
            
            N_all_entries_per_slice = N_all_entries_per_slice[MASK]
            N_entries = N_entries[MASK]
            N_entries = np.divide(N_entries, N_all_entries_per_slice)
            
            plt.scatter(x = centered_energy_bins, y = N_entries, label = "%s"%(timing), s = 13, color = color)
            plt.plot(centered_energy_bins, N_entries, color = color )
            plt.errorbar(x = centered_energy_bins, y = N_entries, xerr = xerrors, yerr = zero_errors, fmt = " ", color = color )  
            
        plt.xlabel("Real data TP Et (ADC)", fontsize = 20)
        plt.ylabel("Population fraction", fontsize = 20)    
        legend = plt.legend(loc = 'best', fontsize = 15, title = 'Severity %s'%(severity))
        plt.setp(legend.get_title(),fontsize='15')
        plt.ylim(0, 1.1)
        plt.xlim(xmin, xmax)
        plt.grid()
        if(log):
            plt.ylim(0.0001, 1)
            plt.yscale('log')    
            
        Add_CMS_Header(plt, lumi, isWide, ax)
            
        plt.show()
        plt.close()
            
    print("DONE")    

    """

    # Real vs emu plots, maybe 

    """

        # ##-- EB Occupancy
        # #direc = "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Run_346446_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeightsTaggingMode/211115_170649/0000_output/"
        # n_files = 384 # number of input files 

        # for selection in selections:
        #     values_0 = pickle.load(open("%s/%s_%s_values_0.p"%(direc, varLabel, selection), "rb"))
        #     values_1 = pickle.load(open("%s/%s_%s_values_1.p"%(direc, varLabel, selection), "rb"))

        #     total_values = np.add(values_0, values_1)

        #     for i in range(n_files):
        #         if(i > maxFiles):
        #             print("Max files reached: ",i)
        #             break 
        #         if(i == 0 or i == 1): continue 
        #         if(i%10 == 0): print("on file %s / %s"%(i, n_files))

        #         exec('thisValues = pickle.load(open("%s/%s_%s_values_%s.p"%(direc, varLabel, selection, i), "rb"))')  
        #         total_values = np.add(total_values, thisValues)

        #     exec("%s_%s_values = np.copy(total_values)"%(varLabel, selection))

        
        # # add a second directory 
        # #n_files_2 = 1000 
        # direc_2 = "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/Run_346447_PilotBeam_2021/ETTAnalyzer_CMSSW_12_1_0_pre3_DoubleWeightsTaggingMode/211116_115908/0000_output/"
        # files_2 = ["%s/%s"%(direc_2, f) for f in os.listdir(direc_2) if varLabel in f]

        # for file_i,file in enumerate(files_2):
        #     if(i > maxFiles):
        #         print("Max files reached: ",i)
        #         break         
        #     if(file_i%10 == 0): print("on file %s / %s"%(file_i, len(files_2)))

        #     thisValues = pickle.load(open(file, "rb"))
        #     # exec('thisValues = pickle.load(open("%s"%(file), "rb"))')  
        #     total_values = np.add(total_values, thisValues)     

        # # Plot 
        # vmaxAll = -1
        # if(plotIndividuals):
        #     for selection in selections:
        #         print("On selection:",selection)
        #         exec("Values_array = %s_%s_values"%(varLabel, selection))
        #         isRatio = 0 
        #         plotText = selection
        #         if("all" in selection):
        #             vmaxAll = np.max(Values_array)
        #         plotText_params = [plotText, addPlotText]
        #         MakeETTPlot(Values_array, varLabel, selection, doSymLog, 0, plotText_params, vmaxAll, ymax, zmax)

        # # take ratio 
        # if(plotRatio):
        #     if(("clean_all" in selections) and ("clean_tagged" in selections)):

        #         exec("total_values = np.copy(%s_clean_all_values)"%(varLabel))
        #         exec("tagged_values = np.copy(%s_clean_tagged_values)"%(varLabel))

        #         total_values = np.array(total_values, dtype=float) 
        #         tagged_values = np.array(tagged_values, dtype=float)   

        #         # See which region of phase space is tagged 
        #         fraction = np.divide(tagged_values, total_values, out=np.zeros_like(tagged_values), where=total_values!=0)
        #         isRatio = 1 
        #         # doSymLog = 0 
        #         plotText = "Tagged / Total"
        #         plotText_params = [plotText, addPlotText]
        #         MakeETTPlot(fraction, "%s_ratio"%(varLabel), "clean", doSymLog, isRatio, plotText_params, vmaxAll, ymax, zmax)

        #print("DONE")    

        """