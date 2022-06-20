"""
17 November 2021
Abraham Tishelman-Charny 

The purpose of this module is to provide tools for ETTPlot. 
"""

import numpy as np 
import matplotlib
from matplotlib import pyplot as plt 
from matplotlib.colors import LogNorm, SymLogNorm
import copy 
import matplotlib as mpl

def GetWorkingPointLabels(direc_):
    if("0p5Prime" in direc_):
        WP = "MinDelta0p5prime"
    elif("2p5Prime" in direc_):
        WP = "MinDelta2p5prime"
    else:
        raise Exception("Cannot find 0p5 or 2p5 WP in output location name")

    if("WithOddPeakFinder" in direc_):
        PF = "WithOddPF"
    elif("WithoutOddPeakFinder" in direc_):
        PF = "WithoutOddPF"
    else:
        raise Exception("Cannot find WithOddPF or WithoutOddPF in output location name")   

    if("weightsReco" in direc_):
        RECO = "Weights"
    elif("MultifitReco" in direc_):
        RECO = "MultiFit"
    else:
        raise Exception("Cannot find WeightsReco or MultiFitReco RECO in output location name")     

    return WP, PF, RECO

def Add_CMS_Header(plt, ax, upperRightText, xmin, addLumi, lumi, fontsize, unit, sqrts):
    
    plt.text(
        0., 1., u"CMS ",
        fontsize=fontsize, fontweight='bold',
        # fontsize=fontsize * 0.7, fontweight='bold',
        horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes
    )

    prelim_x = xmin
    
    ##-- Preliminary 
    plt.text(
        # prelim_x, 1., u"$\it{Preliminary}$",
        # prelim_x, 1., u"$\it{Work}$ $\it{In}$ $\it{Progress}$",
        # prelim_x * 0.75, 1., u"$\it{Work}$ $\it{In}$ $\it{Progress}$",
        prelim_x * 0.75, 1., u"$\it{Preliminary}$",
        # prelim_x * 0.75, 1., u"$\it{Supplementary}$",
        fontsize=(fontsize) * (0.93),
        # fontsize=fontsize,
        horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes
    )    

    # # upper right text 
    # plt.text(
    #     1., 1., upperRightText,
    #     fontsize=16, horizontalalignment='right', 
    #     verticalalignment='bottom', 
    #     transform=ax.transAxes
    # )  

    if(addLumi):
        upperRightText = r"%s $%s^{-1}$ (%s)"%(str(lumi), str(unit), str(sqrts))
        # upperRightText = r"%s fb$^{-1}$ (13 TeV)"%(str(lumi))
    else:
        upperRightText = r"(%s)"%(sqrts)

    ##-- Lumi 
    plt.text(
        1., 1., upperRightText,
        # fontsize=fontsize, horizontalalignment='right', 
        fontsize=fontsize, horizontalalignment='right', 
        verticalalignment='bottom', 
        transform=ax.transAxes
    )   

    #plt.title('Left Title', loc='left')
    #plt.title('Right Title', loc='right')    

# for changing the axes of plots made from pickled arrays 
def SetYMin(Values_array_, ymin_, binWidth_):
    Transformed_List = []
    ymin_bin_i = (1./binWidth_) * ymin_ + 10./binWidth_ 
    for i, xBinVals in enumerate(Values_array_):
        nVals = len(xBinVals)
        MASK = [i > ((ymin_bin_i) - 1) for i, val in enumerate(xBinVals)]
        xBinVals = xBinVals[MASK]
        Transformed_List.append(xBinVals)
    Transformed_List = np.array(Transformed_List)
    return Transformed_List

def SetYMax(Values_array_, ymax_, binWidth_, ybins):
    Transformed_List = [] 
    ymax_bin_i = ymax_ # for [0, 256] with 1 spaced binnings 
    for i, xBinVals in enumerate(Values_array_):
        nVals = len(xBinVals)
        MASK = [i < ((ymax_bin_i)) for i, val in enumerate(xBinVals)]
        xBinVals = xBinVals[MASK]
        Transformed_List.append(xBinVals)        
    Transformed_List = np.array(Transformed_List)

    ybins = np.linspace(0, int(ymax_), int(ymax_)+1) # assumes starting at zero and binwidth of 1 

    return [Transformed_List, ybins]

def SetXMax(Values_array_, xmax_, binWidth_): # as you loop the Values_array, each object is a y slice starting from the left 
    Transformed_List = [] 
    xmax_bin_i = xmax_ # for [0, 256] with 1 spaced binnings 
    for i, xBinVals in enumerate(Values_array_):
        if(i > xmax_bin_i): continue 
        else: Transformed_List.append(xBinVals)        
    Transformed_List = np.array(Transformed_List)
    return Transformed_List    

def GetBins(varLabel_, dataset_):

    # larger energy range for full readout 2017 / 2018 data 
    if(dataset_ == "FullReadoutData_2018"):
        binDict = {
            "realVsEmu" : [[0, 256, 256], [0, 256, 256]],
            "EnergyVsTimeOccupancy" : [[-50, 50, 100],[0, 256, 256]], # full ET range 
            "EnergyVsTimeOccupancy_ratio" : [[-50, 50, 100],[0, 35, 35]],
            "oneMinusEmuOverRealvstwrADCCourseBinning" : [[1.0, 8.0, 16.0, 24.0, 32.0, 40.0, 48.0, 56.0, 64.0, 72.0, 80.0, 88.0, 96.0, 104.0, 112.0, 150.0, 256.0], [0, 1.2, 48]],
            "oneMinusEmuOverRealvstwrADCCourseBinningZoomed" : [[1, 41, 40], [0, 1.2, 48]]
        }
    elif(dataset_ == "PilotBeam2021"):
        binDict = {
            "realVsEmu" : [[0, 256, 256], [0, 256, 256]],
            "EnergyVsTimeOccupancy" : [[-50, 50, 100],[0, 35, 35]], # shorter ET range 
            "EnergyVsTimeOccupancy_ratio" : [[-50, 50, 100],[0, 35, 35]],
            "oneMinusEmuOverRealvstwrADCCourseBinning" : [[1, 41, 40], [0, 1.2, 48]]
        }
    elif(dataset_ == "Run352912"):
        binDict = {
            "realVsEmu" : [[0, 256, 256], [0, 256, 256]],
            "EnergyVsTimeOccupancy" : [[-50, 50, 100],[0, 256, 256]], # Full ET range 
            # "EnergyVsTimeOccupancy" : [[-50, 50, 100],[0, 35, 35]], # shorter ET range 
            "EnergyVsTimeOccupancy_ratio" : [[-50, 50, 100],[0, 35, 35]],
            "oneMinusEmuOverRealvstwrADCCourseBinning" : [[1, 41, 40], [0, 1.2, 48]]
        }

    xinfo = binDict[varLabel_][0]
    yinfo = binDict[varLabel_][1]

    # x bins 
    xinfo_len = len(xinfo)
    if(xinfo_len == 3): # assume equal bin widths 
        xmin, xmax, xbins = xinfo
        xbinning = np.linspace(xmin, xmax, xbins + 1)
    else: # assume non-equal bin widths 
        xbinning = np.array(xinfo) 

    # y bins 
    yinfo_len = len(yinfo)
    if(yinfo_len == 3): # assume equal bin widths 
        ymin, ymax, ybins = yinfo
        ybinning = np.linspace(ymin, ymax, ybins + 1)
    else: # assume non-equal bin widths 
        ybinning = np.array(yinfo) 

    return [xbinning, ybinning]

def GetPlotLabels(varLabel_):
    labelDict = {
        "realVsEmu" : ["Emulated TP Et (ADC)", "Real data TP Et (ADC)"],
        "EnergyVsTimeOccupancy" : ["time (ns)", "Real data TP Et (ADC)"],
        "EnergyVsTimeOccupancy_ratio" : ["time (ns)", "Real data TP Et (ADC)"],
        "oneMinusEmuOverRealvstwrADCCourseBinning" : ["Real data TP Et (ADC)", "1 - (emu / real)"],
        "oneMinusEmuOverRealvstwrADCCourseBinningZoomed" : ["Readl data TP Et (ADC)", "1 - (emu / real)"]

    }

    return labelDict[varLabel_]     

# Compute averages values per bin
def ComputeAverages(xbins_, Values_array_):
    # make average per bin plot as well 
    averages = []
    stdevs = [] 

    ybinVals = range(0, 1200, 25)
    ybinVals = [val/1000. for val in ybinVals] ##-- y bins (1 - emu/real)

    ##-- x bins 
    for bin_i, binmin in enumerate(xbins_[:-1]):
        h_slice_vals = Values_array_[bin_i]
        #average_conts = np.multiply(ybinVals, h_slice_vals)
        if(np.sum(h_slice_vals) == 0):
            average = -1 
            stdev = -1 
        else:
            average = np.average(ybinVals, weights=h_slice_vals)
            variance = np.average((ybinVals-average)**2, weights=h_slice_vals)
            stdev = np.sqrt(variance)
        averages.append(average)
        stdevs.append(stdev)

    averages = np.array(averages)
    stdevs = np.array(stdevs)
    
    return averages, stdevs 

def MakeETTPlot(Values_array, variable_, severity, time, ol, upperRightText, dataset, lumi, unit, sqrts, FGSelection):
    print("Making plot")  

    # Prepare figure and axes 
    fig, ax = plt.subplots()
    fig.set_dpi(100)
    fig.set_size_inches(10, 7.5)
    cmap = copy.copy(matplotlib.cm.get_cmap("jet"))
    cmap.set_under(color='white')     
    xbins, ybins = GetBins(variable_, dataset)

    ymax = 35
    binWidth = 1 
    Values_array, ybins = SetYMax(Values_array, ymax, binWidth, ybins)      

    # plot with colormesh 
    # if(isRatio): 
    #     vmin = 0.00000001
    # else: 
    # vmin = 1 
    # if(doSymLog): 
        # norm = norm = SymLogNorm(linthresh=0.03, vmin = vmin)
    # else: 
        # norm = None     

    if(variable_ == "EnergyVsTimeOccupancy"):
        normalize = 0
    else:
        normalize = 0 

    if(normalize):
        maxVal = np.max(Values_array)
        Values_array = Values_array / maxVal 
        vmin = 0.000000001
        zLabel = "Fraction"
        norm = LogNorm(vmin=vmin)

    else: 
        vmin = 1 
        zLabel = "Entries"

    # If plotting the ratio, don't want the min z value to be 1. 
    if(FGSelection == "ratio"): 
        normalize = 0
        vmin = 0.000000001
        vmax = 1 
        zLabel = "Fraction"
        norm = None 
        norm = norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    else:
        maxVal = np.max(Values_array)
        vmax = maxVal
        norm = LogNorm(vmin=vmin, vmax=vmax)

    pos = ax.pcolormesh(xbins, 
                        ybins, 
                        Values_array.transpose(1,0), 
                        cmap = cmap, 
                        # vmin = vmin,
                        norm = norm,
                        #vmax = vmax,
                        # norm = norm
                        )
    cb = fig.colorbar(pos, 
                    ax=ax,
                )   

    cb.set_label(zLabel, rotation=270, fontsize = 25, labelpad = 30)
    cb.ax.tick_params(labelsize=20) 

    xLabel, yLabel = GetPlotLabels(variable_)
    plt.xlabel(xLabel, fontsize=25)
    plt.ylabel(yLabel, fontsize=25)
    addLumi = 1
    # fontsize = 22.5
    fontsize = 18
    text_xmin = 0.12
    Add_CMS_Header(plt, ax, upperRightText, text_xmin, addLumi, lumi, fontsize, unit, sqrts)
    plt.grid()
    plotText = "Sev = %s, time = %s"%(severity, time)
    addPlotText = 1 

    if(addPlotText):
        plt.text(
            0.1, 0.75, plotText,
            fontsize=30, fontweight='bold',
            horizontalalignment='left',
            verticalalignment='bottom',
            transform=ax.transAxes
        )

    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    fig.tight_layout()
    for fileType in ["png", "pdf"]:
        plt.savefig("{ol}/{variable_}_sev{severity}_{time}_{FGSelection}.{fileType}".format(ol=ol, variable_=variable_, severity=severity, time=time, FGSelection=FGSelection, fileType=fileType), dpi = 300)  #bbox_inches='tight', dpi = 300)
    plt.close()    

    # make average per bin plot as well 
    averages = []
    stdevs = [] 

    ybinVals = range(0, 1200, 25)
    ybinVals = [val/1000. for val in ybinVals] ##-- y bins (1 - emu/real)

    if( (variable_ == "oneMinusEmuOverRealvstwrADCCourseBinning") or (variable_ == "oneMinusEmuOverRealvstwrADCCourseBinningZoomed")):
        averages, stdevs = ComputeAverages(xbins, Values_array)

        # Prepare figure and axes 
        fig, ax = plt.subplots()
        fig.set_dpi(100)
        fig.set_size_inches(10, 7.5)

        energy_bins = xbins
        centered_energy_bins_ = [ ((energy_bins[i+1] - energy_bins[i]) / 2.) + energy_bins[i] for i in range(len(energy_bins) - 1) ]
        xerrors_ = [ ((energy_bins[i+1] - energy_bins[i]) / 2.) for i in range(len(energy_bins) - 1) ]  
        centered_energy_bins = np.array(centered_energy_bins_)
        xerrors = np.array(xerrors_)

        # zero errors: 
        # xerrors_ = np.array([0 for i in len(xerrors)])

        averages_before_mask = np.copy(averages)
        stdevs_before_mask = np.copy(stdevs)
        MASK = tuple([averages != -1])
        centered_energy_bins = centered_energy_bins[MASK]
        averages = averages[MASK]
        stdevs = stdevs[MASK]  
        xerrors = xerrors[MASK]

        zero_errors = [0. for i in range(0, len(averages))]
        error = 0
        log = 1
        xmin_, xmax_ = xbins[0], xbins[-1]

        print("here")

        if(error):
            plt.scatter(x = centered_energy_bins, y = averages, label = "Severity = %s, %s"%(severity, time), s = 15)
            # plt.errorbar(x = centered_energy_bins, y = averages, xerr = xerrors, yerr = zero_errors, fmt = " ")            
            plt.errorbar(x = centered_energy_bins, y = averages, xerr = zero_errors, yerr = zero_errors, fmt = " ")            
        else:
            plt.scatter(x = centered_energy_bins, y = averages, label = "Severity = %s, %s"%(severity, time), s = 10)
            plt.plot(x = centered_energy_bins, y = averages, label = "__nolegend__", linestyle = '-')

        plt.xlabel("Real data TP Et (ADC)", fontsize=15)
        plt.ylabel("Average 1 - (Emulated / Real)", fontsize=15)    
        plt.legend(loc = 'best', fontsize = 15)
        plt.ylim(0, 1.01)
        plt.xlim(xmin_, xmax_)
        plt.grid()
        if(log):
            plt.ylim(0.0001, 1)
            plt.yscale('log')    
        plt.savefig("%s/Sev_%s_Average_%s_%s.png"%(ol, severity, variable_, time), dpi = 100)
        plt.savefig("%s/Sev_%s_Average_%s_%s.pdf"%(ol, severity, variable_, time), dpi = 100)        
        plt.close()

        return averages_before_mask, stdevs_before_mask 

    else:
        return None, None

"""

def MakeETTPlot(Values_array, varLabel, selection, doSymLog, isRatio, plotText_params, vmaxAll, ymax, zmax):

    # parameters 
    upperRightText = "Pilot Beam 2021"
    text_xmin = 0.1

    ##-- Prepare figure and axes 
    fig, ax = plt.subplots()
    
    fig.set_dpi(100)
    fig.set_size_inches(10, 7.5)
    # cmap = plt.cm.Blues
    # cmap = plt.cm.RdBu_r # for sym log 
    cmap = plt.cm.jet
    cmap.set_under(color='white') 

    xbins, ybins = GetBins(varLabel)

    # ##-- Custom binning 
    # ymin_large = int(ymin * 1000)
    # ymin = 0 
    # ybins = range()
    # ybins = range(ymin_large, 1200, 25)

    # ymin = 0 
    # binWidth = 1
    # Values_array = SetYMin(Values_array, ymin, binWidth)
    # Values_array = SetYMin(Values_array, ymin)
    # xmax = 50
    # ymax = 50

    # custom binning for realVsEmu    
    # binWidth = 1 
    # Values_array = SetYMax(Values_array, ymax, binWidth)
    # Values_array = SetXMax(Values_array, xmax, binWidth)
    #xbins = np.linspace(0, xmax, int(xmax)+1)
    #ybins = np.linspace(0, ymax, int(ymax)+1)

    binWidth = 1 
    # print("Before:")
    # for i,thing in enumerate(Values_array):
        # print("%s: %s"%(i, thing))
    Values_array, ybins = SetYMax(Values_array, ymax, binWidth, ybins)
    # print("After:")
    # for i,thing in enumerate(Values_array):
        # print("%s: %s"%(i, thing))    

    # if("Tagged" in selection):
    #     vmax = vmaxAll
    # else:
    #     vmax = None

    if("tagged" in selection):
        vmax = vmaxAll
    else:
        vmax = None
        # plt.clim(0, vmaxAll)

    # plot with colormesh 
    if(isRatio): 
        vmin = 0.00000001
    else: 
        vmin = 1 
    if(doSymLog): 
        norm = norm = SymLogNorm(linthresh=0.03, vmin = vmin)
    else: 
        norm = None 

    if(zmax != -1):
        vmax = zmax 

    pos = ax.pcolormesh(xbins, 
                        ybins, 
                        Values_array.transpose(1,0), 
                        cmap = cmap, 
                        vmin = vmin,
                        vmax = vmax,
                        norm = norm
                        )
    cb = fig.colorbar(pos, 
                    ax=ax,
                )    

    # object_methods = [method_name for method_name in dir(cb)
                #   if callable(getattr(cb, method_name))]

    # print("object_methods:",object_methods)

    # cmin, cmax = cb.get_clim()
    # if("tagged" in selection):
    #     print("Setting clim")
    #     plt.clim(0, vmaxAll)

    #ax.matshow(Values_array, cmap='seismic')

    # # plot with imshow 
    # pos = ax.imshow(Values_array.transpose(1,0),
    #             interpolation='none',
    #             aspect="auto",
    #             extent = [0, 256, 256, 0],
    # #                vmin=0.00000001, vmax=1,
    # #            vmin=0, vmax=1,
    # #            vmin=0.000001, vmax=1,
    # #                 vmin=0,
    #             cmap = cmap,
    # #            norm = LogNorm(vmin = 1, vmax = eval("sev_%s_all_maxValue"%(severity))) ##-- Set vmax to max from total number of TPs
    # #                norm = LogNorm(vmin = 1) ##-- Set vmax to max from total number of TPs
    #             norm = LogNorm(vmin = 1) ##-- Set vmax to max from total number of TPs
    #             )
    # plt.gca().invert_yaxis()

    # cb = fig.colorbar(pos, 
    #                 ax=ax,
    #             )


    xLabel, yLabel = GetPlotLabels(varLabel)

    plt.xlabel(xLabel, fontsize=25)
    plt.ylabel(yLabel, fontsize=25)

    Add_CMS_Header(plt, ax, upperRightText, text_xmin)

    plt.grid()
    plotText, addPlotText = plotText_params
    plotText = plotText.replace("clean_", "")

    if(addPlotText):
        plt.text(
            0.1, 0.75, plotText,
            fontsize=30, fontweight='bold',
            horizontalalignment='left',
            verticalalignment='bottom',
            transform=ax.transAxes
        )

    #ol = "/eos/user/a/atishelm/www/EcalL1Optimization/PilotBeam2021/MinDelta2p5prime_WithOddPF_MultiFitReco/"
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    fig.tight_layout()
    plt.savefig("{ol}/{varLabel}_{selection}.png".format(ol=ol, varLabel=varLabel, selection=selection))
    plt.savefig("{ol}/{varLabel}_{selection}.pdf".format(ol=ol, varLabel=varLabel, selection=selection))
    plt.close()    

"""