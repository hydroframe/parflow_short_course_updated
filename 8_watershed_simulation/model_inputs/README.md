The directory contains the following input files in order to perform a fully coupled, distributed watershed simulation with ParFlow-CLM.

The directory contains CLM input.

drv_clmin.dat: Namelist for CLM with variable definitions; many variables are depricated and now handled via ParFlow input. Do not change.

drv_vegm.dat: Spatially distributed land information, which is explained in the header lines of the file. 1 -18 refer to so called plant functional types paramterizing vegetation land cover. Examples include grass, deciduous forest, and crop.

drv_vegp: Look-up table of plany physiological and Monin-Ubukhov parameters for PFT parameterization and approximation of turbulent exchange of water, energy and momentum with the atmosphere.  

geom_table.csv: List of hydraulic variable values for each geometry defined in the model setup.

Indicator_LW_USGS_Bedrock.pfb: ParFlow binary file of 3D distributed indicator information to depict heterogeneity and bedrock hydrogeology.

LW.mask.pfb: The mask of inactive/active model cells (0: inactive model cells; >0: active model cells) in ParFlow binary format

LW.mask.pfb: The mask of inactive/active model cells (0: inactive model cells; >0: active model cells) in vtk format for plotting.

LW.pfsol: ParFlow ASCII pfsolid file with the node definitions of the triangulated surface to assemble the LW watershed in 3D including the definition of the patches for boundardy conditions.

Mannings_CONUS2.0_LW.pfb: ParFlow binary files of the 2D spatial distribution of Manning's roughness coefficient for overland flow simulations.

slopex_LW.pfb: ParFlow binary of the spatial distributed topographic slopes in x-direction.

slopey_LW.pfb: ParFlow binary of the spatial distributed topographic slopes in y-direction.


