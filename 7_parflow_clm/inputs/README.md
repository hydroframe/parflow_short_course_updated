The directory contains CLM input.

drv_clmin.dat: Namelist for CLM with variable definitions; many variables are depricated and now handled via ParFlow input. Do not change.

drv_vegm.dat: Spatially distributed land information, which is explained in the header lines of the file. 1 -18 refer to so called plant functional types paramterizing vegetation land cover. Examples include grass, deciduous forest, and crop.

drv_vegp: Look-up table of plany physiological and Monin-Ubukhov parameters for PFT parameterization and approximation of turbulent exchange of water, energy and momentum with the atmosphere.  