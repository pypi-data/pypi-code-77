# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 16:03:10 2021

"""

import meteva
import xarray as xr
import numpy as np

def plot_values(look_ff, cmap ="rain_24h"):

    #plot_values(dataset_ob, grd_ob, grd_fo, cmap)
    #data_Xlabeled = grd_ob
    #data_Ylabeled = grd_fo
    
    #整理无坐标信息的格点场的坐标：原始的观测场和预报场的经纬度范围应该是对应的
    #glon = [dataset_ob["lon"].values[0], dataset_ob["lon"].values[-1],
    #        dataset_ob["lon"].values[1]-dataset_ob["lon"].values[0]]    #经度的起点、终点、间隔
    #glat = [dataset_ob["lat"].values[0], dataset_ob["lat"].values[-1],
    #          dataset_ob["lat"].values[1]-dataset_ob["lat"].values[0]]    #纬度的起点、终点、间隔

    #grid1 = meb.grid(glon, glat)
    #data_Xlabeled_tr = meb.grid_data(grid1, data_Xlabeled)
    #data_Ylabeled_tr = meb.grid_data(grid1, data_Ylabeled)
    
    #a = data_Xlabeled_tr
    #b = data_Ylabeled_tr
    #colorbar生成
    #cmap, clev = meb.def_cmap_clevs(meb.cmaps.mode, vmax = np.max((np.max(a), np.max(b))))
    #clev = meb.def_cmap_clevs(meb.cmaps.mode, vmax = np.max((np.max(a), np.max(b))))
    #meb.tool.color_tools.show_cmap_clev(cmap, clev)    #展示colorbar
    #meb.tool.plot_tools.plot_2d_grid_list([a, b], cmap = cmap, clevs = clev)
    grd_ob = look_ff["grd_ob"]
    grd_fo = look_ff["grd_fo"]
    meteva.base.tool.plot_tools.plot_2d_grid_list([grd_ob, grd_fo], cmap = cmap, vmax = np.max((np.max(grd_ob), np.max(grd_fo))),ncol=2)
    
def plot_ids(look_ff,label = None):
    #plot_ids(dataset_ob, grd_ob, grd_fo):
    if label is None:
        data_Xlabeled = look_ff['grd_ob_labeled']
        data_Ylabeled = look_ff['grd_fo_labeled']

        #整理无坐标信息的格点场的坐标：原始的观测场和预报场的经纬度范围应该是对应的
        #glon = [dataset_ob["lon"].values[0], dataset_ob["lon"].values[-1],
        #        dataset_ob["lon"].values[1]-dataset_ob["lon"].values[0]]    #经度的起点、终点、间隔
        #glat = [dataset_ob["lat"].values[0], dataset_ob["lat"].values[-1],
        #         dataset_ob["lat"].values[1]-dataset_ob["lat"].values[0]]    #纬度的起点、终点、间隔

        #grid = look_ff["grid"]
        #grd_ob = meteva.base.grid_data(grid, data_Xlabeled)
        #grd_fo = meteva.base.grid_data(grid, data_Ylabeled)
        #meteva.base.set_griddata_coords(grd_ob,member_list=["OBS"])
        #meteva.base.set_griddata_coords(grd_fo, member_list=["FCT"])
        #a = data_Xlabeled_tr
        #b = data_Ylabeled_tr
        meteva.base.tool.plot_tools.plot_2d_grid_list([data_Xlabeled, data_Ylabeled], cmap = "mode", vmax = np.max((np.max(data_Xlabeled), np.max(data_Ylabeled)))+1,ncol=2)
    else:

        arr = look_ff['grd_ob_features']['labels_'+str(label)]
        arr1 = np.zeros(arr.shape)
        arr1[arr < 100] = arr[arr < 100]
        grid1 = meteva.base.get_grid_of_data(look_ff["grd_ob"])
        data_Xlabeled = meteva.base.grid_data(grid1, arr1)

        arr = look_ff['grd_fo_features']['labels_'+str(label)]
        arr1 = np.zeros(arr.shape)
        arr1[arr < 100] = arr[arr < 100]
        grid1 = meteva.base.get_grid_of_data(look_ff["grd_fo"])
        data_Ylabeled = meteva.base.grid_data(grid1, arr1)
        meteva.base.tool.plot_tools.plot_2d_grid_list([data_Xlabeled, data_Ylabeled], cmap="mode",
                                                      vmax=np.max((np.max(data_Xlabeled), np.max(data_Ylabeled))) + 1,
                                                      ncol=2)
    
'''
if __name__ == '__main__':
    filename_ob = r'F:\\Work\\MODE\\Submit\\mode_data\\ob\\rain03\\20070111.000.nc'    
    dataset_ob = xr.open_dataset(filename_ob)  #通过xarray程序库读取nc文件中的所有内容
    
    #绘图：原始观测和预报场
    A = plot_values(dataset_ob, grd_ob = look_featureFinder['grd_ob'], 
             grd_fo = look_featureFinder['grd_fo'], cmap = "rain_3h")
    
    #绘图：(观测场和预报场中)被标记的目标
    B = plot_ids(dataset_ob, grd_ob = look_featureFinder['grd_ob_labeled'], 
             grd_fo = look_featureFinder['grd_fo_labeled'])
    
    #绘图：(观测场和预报场中)合并后目标标记
    C = plot_ids(dataset_ob, look_mergeforce['grd_ob_labeled'], look_mergeforce['grd_fo_labeled'])
'''