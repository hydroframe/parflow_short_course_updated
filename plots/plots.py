# Here we set up some functions for plotting outputs.
import parflow as pf
import numpy as np  # we will use numpy to work with the data
import matplotlib.pyplot as plt  # we will use matplotlib to plot the data
from parflow.tools.fs import get_absolute_path
from parflow.tools.io import write_pfb, read_pfb
from parflow import Run
import parflow.tools.hydrology as hydro
from glob import glob
import math
import os

def plot_domain(run_directory, variable, timestep=0):
    """Function to plot output from a ParFlow run"""

    # Load the run from the file, this is the same as the run defined above
    run = Run.from_definition(os.path.join(run_directory, "domain_example.pfidb"))   

    data = run.data_accessor # get the data accessor, this makes it easier to access the data from the run
    nt = len(data.times)  # get the number of time steps
    nx = data.shape[2]    # get the number of cells in the x direction
    ny = data.shape[1]    # get the number of cells in the y direction
    nz = data.shape[0]    # get the number of cells in the z direction
    dx = data.dx          # get the cell size in the x direction
    dy = data.dy          # get the cell size in the y direction
    dz = data.dz          # get the cell size in the z direction, this is a 1D array of size nz

    # Print a summary of the run data
    print(f"nx = {nx}, ny = {ny}, nz = {nz}, nt = {nt}")
    print(f"dx = {dx}, dy = {dy}, dz = {dz}")

    # Load the data
    data = read_pfb(get_absolute_path(f"domain_example.out.{variable}.{str(timestep).zfill(5)}.pfb")).reshape(nz, nx)
    
    # Set negative saturation values to NaN
    if variable == "satur":
        data[data < 0.0] = np.nan
    
    # Set up x and z to match the shape of the ParFlow grid
    x = np.arange(0.0,(nx+1)*dx,dx)
    z = np.zeros(nz+1)
    z[1:] = np.cumsum(dz)

    # Get limits for plotting
    vmin = np.nanmin(data)
    vmax = np.nanmax(data)
    print(f"vmin: {vmin}, vmax: {vmax}")
    
    # Define labels for plots
    if variable == "satur":
        label = "Saturation [-]"
        title = "Saturation"
    elif variable == "press":
        label = "Pressure Head [m]"
        title = "Pressure Head"

    # Use pcolormesh to plot the data with the x and z coordinates with lines 
    # for the grid mesh from the ParFlow run grid
    fig, ax = plt.subplots()
    im = ax.pcolormesh(x, z, data, vmin=vmin, vmax=vmax, cmap='plasma_r')
    plt.colorbar(im, ax=ax, label=label)
    
    # Include mesh lines
    ax.hlines(z,x[0],x[-1],colors='white',linewidth=0.5)
    ax.vlines(x,z[0],z[-1],colors='white',linewidth=0.5)
    
    ax.set_xlabel('x [m]')
    ax.set_ylabel('z [m]')
    ax.set_title(f"{title} at t={timestep}")
    plt.show()

def plot_domain_overland(run_directory, variable, timestep=0):
    """Function to plot output from a ParFlow run: Overland Flow module"""

    # Load the run from the file, this is the same as the run defined above
    run = Run.from_definition(os.path.join(run_directory, "overland_tiltedV.pfidb"))   

    data = run.data_accessor # get the data accessor, this makes it easier to access the data from the run
    nt = len(data.times)  # get the number of time steps
    nx = data.shape[2]    # get the number of cells in the x direction
    ny = data.shape[1]    # get the number of cells in the y direction
    nz = data.shape[0]    # get the number of cells in the z direction
    dx = data.dx          # get the cell size in the x direction
    dy = data.dy          # get the cell size in the y direction
    dz = data.dz          # get the cell size in the z direction, this is a 1D array of size nz

    # Print a summary of the run data
    print(f"nx = {nx}, ny = {ny}, nz = {nz}, nt = {nt}")
    print(f"dx = {dx}, dy = {dy}, dz = {dz}")

    # Load the data
    data = read_pfb(get_absolute_path(f"overland_tiltedV.out.{variable}.{str(timestep).zfill(5)}.pfb"))[0, :, :]
    
    # Set negative saturation values to NaN
    if variable == "satur":
        data[data < 0.0] = np.nan
    
    # Set up x and z to match the shape of the ParFlow grid
    x = np.arange(0.0,(nx+1)*dx,dx)
    y = np.arange(0.0,(ny+1)*dy,dy)
    z = np.zeros(nz+1)
    z[1:] = np.cumsum(dz)

    # Get limits for plotting
    vmin = np.nanmin(data)
    vmax = np.nanmax(data)
    print(f"vmin: {vmin}, vmax: {vmax}")
    
    # Define labels for plots
    if variable == "satur":
        label = "Saturation [-]"
        title = "Saturation"
    elif variable == "press":
        label = "Pressure Head [m]"
        title = "Pressure Head"

    # Use pcolormesh to plot the data with the x and z coordinates with lines 
    # for the grid mesh from the ParFlow run grid
    fig, ax = plt.subplots()
    im = ax.pcolormesh(x, y, data, vmin=vmin, vmax=vmax, cmap='plasma_r')
    plt.colorbar(im, ax=ax, label=label)
    
    # Include mesh lines
    ax.hlines(z,x[0],x[-1],colors='white',linewidth=0.5)
    ax.vlines(x,z[0],z[-1],colors='white',linewidth=0.5)
    
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_title(f"{title} at t={timestep}")
    plt.show()
    
def plot_subsurface_storage(run_directory):
    """Function to plot total subsurface storage over time based on a ParFlow run"""
    
    # Load the run from the file, this is the same as the run defined above
    run = Run.from_definition(os.path.join(run_directory, "domain_example.pfidb"))   

    data = run.data_accessor # get the data accessor, this makes it easier to access the data from the run
    nt = len(data.times)  # get the number of time steps
    nx = data.shape[2]    # get the number of cells in the x direction
    ny = data.shape[1]    # get the number of cells in the y direction
    nz = data.shape[0]    # get the number of cells in the z direction
    dx = data.dx          # get the cell size in the x direction
    dy = data.dy          # get the cell size in the y direction
    dz = data.dz          # get the cell size in the z direction, this is a 1D array of size nz
    mask = data.mask
    porosity = data.computed_porosity
    specific_storage = data.specific_storage

    # Initialize empty array
    subsurface_storage = np.zeros(nt)
    
    press_files = sorted(glob(f'{run_directory}/domain_example.out.press*.pfb'))
    satur_files = sorted(glob(f'{run_directory}/domain_example.out.satur*.pfb'))

    # Iteratively calculate overland flow for whole domain
    for hour in range(0, nt):        
        pressure = pf.read_pfb(press_files[hour])
        saturation = pf.read_pfb(satur_files[hour])
            
        subsurface_storage[hour] = np.sum(hydro.calculate_subsurface_storage(porosity, pressure, saturation, specific_storage, dx, dy, dz, mask=mask),
        axis=(0, 1, 2))

    # Plot
    plt.plot(subsurface_storage)
    plt.xlabel("Time")
    plt.ylabel("Subsurface Storage")
    plt.title(f"Subsurface Storage over Time")
    plt.show()

def plot_streamflow(run_directory, grid_cell=None):
    """Function to plot a hydrograph for a single grid cell location based on a ParFlow run"""
    
    # Load the run from the file, this is the same as the run defined above
    run = Run.from_definition(os.path.join(run_directory, "overland_tiltedV.pfidb"))   

    data = run.data_accessor # get the data accessor, this makes it easier to access the data from the run
    nt = len(data.times)  # get the number of time steps
    nx = data.shape[2]    # get the number of cells in the x direction
    ny = data.shape[1]    # get the number of cells in the y direction
    nz = data.shape[0]    # get the number of cells in the z direction
    dx = data.dx          # get the cell size in the x direction
    dy = data.dy          # get the cell size in the y direction
    dz = data.dz          # get the cell size in the z direction, this is a 1D array of size nz
    mask = data.mask
    slopex = (data.slope_x).squeeze()
    slopey = (data.slope_y).squeeze()

    # Initialize empty array
    olf = np.zeros((nt, ny, nx))
    
    press_files = sorted(glob(f'{run_directory}/overland_tiltedV.out.press*.pfb'))
    satur_files = sorted(glob(f'{run_directory}/overland_tiltedV.out.satur*.pfb'))
    mannings = (read_pfb(f"{run_directory}/overland_tiltedV.out.mannings.pfb")).squeeze()

    # Iteratively calculate overland flow for whole domain
    for hour in range(0, nt):        
        pressure = pf.read_pfb(press_files[hour])
        saturation = pf.read_pfb(satur_files[hour])
            
        olf[hour, ...] = hydro.calculate_overland_flow_grid(pressure, slopex, slopey, mannings, dx, dy, mask=mask)  

    # Extract a single location point for plotting. Default to halfway along x-axis and with y=0 unless otherwise noted
    if grid_cell == None:
        grid_cell = (math.floor(nx/2), 0)
        
    output_point = olf[:, grid_cell[0], grid_cell[1]]

    # Plot
    plt.plot(output_point)
    plt.xlabel("Time")
    plt.ylabel("Streamflow")
    plt.title(f"Streamflow at grid cell {grid_cell}")
    plt.show()

def plot_water_balance(run_directory, run_name):
    """Function to plot total subsurface storage over time based on a ParFlow run"""
    
    # Load the run from the file, this is the same as the run defined above
    run = Run.from_definition(os.path.join(run_directory, f"{run_name}.pfidb"))   

    data = run.data_accessor # get the data accessor, this makes it easier to access the data from the run
    nt = len(data.times)  # get the number of time steps
    nx = data.shape[2]    # get the number of cells in the x direction
    ny = data.shape[1]    # get the number of cells in the y direction
    nz = data.shape[0]    # get the number of cells in the z direction
    dx = data.dx          # get the cell size in the x direction
    dy = data.dy          # get the cell size in the y direction
    dz = data.dz          # get the cell size in the z direction, this is a 1D array of size nz
    mask = data.mask
    surface_mask = mask[-1, :, :].astype(int)
    porosity = data.computed_porosity
    specific_storage = data.specific_storage
    mannings = data.mannings
    slopex = data.slope_x 
    slopey = data.slope_y 

    surface_storage = np.zeros(nt)
    subsurface_storage = np.zeros(nt)
    et = np.zeros(nt)
    precip = np.zeros(nt)
    overland_out = np.zeros(nt)
    swe = np.zeros(nt)
    water_balance_ = np.zeros(nt)
    delta_storage = np.zeros(nt)


    for t in range(0, nt):
    
        data.time = t
        pressure = data.pressure 
        saturation = data.saturation

        subsurface_storage[t] = np.sum(hydro.calculate_subsurface_storage(porosity, pressure, saturation, specific_storage, dx,dy,dz, mask=mask),axis=(0,1,2))
        surface_storage[t] = np.sum(hydro.calculate_surface_storage(pressure, dx, dy, mask=mask), axis=(0,1))
        overland_out[t] = hydro.calculate_overland_flow(pressure, slopex, slopey, mannings, dx, dy, mask=mask)

        #generate array of rainfall from ParFlow keys
        # if (t <= run.Cycle.rainrec.r0.Length):
        #     precip[t]=-(run.Patch.z_upper.BCPressure.r0.Value)*(nx*dx)*(ny*dy)*run.TimeStep.Value  #  m/h over domain
        precip[t] = 0.01 * (nx*dx)*(ny*dy) * run.TimeStep.Value
        
        if t > 0: 
            data.forcing_time = t-1
            # precip[t] = np.sum(data.clm_forcing('APCP')[surface_mask==1])*(3600/1000)*(dx)*(dy)
            et[t]  = np.sum(data.clm_output('qflx_evap_tot')[surface_mask==1])*(3600/1000)*(dx)*(dy)
            swe[t]  = np.sum(data.clm_output('swe_out')[surface_mask==1])*(1/1000)*(dx)*(dy)

        if t > 1:
            delta_storage[t] = (subsurface_storage[t] + surface_storage[t] + swe[t]) - (subsurface_storage[t-1] + surface_storage[t-1] + swe[t-1])
            water_balance_[t] = -delta_storage[t] + precip[t] - et[t] - overland_out[t]
            
    # Plot
    plt.plot(water_balance_)
    plt.xlabel("Time")
    plt.ylabel("Water Balance")
    plt.title("Water Balance over Time")
    plt.show()

    plt.plot(delta_storage)
    plt.xlabel("Time")
    plt.ylabel("Change in Storage")
    plt.title("Change in Storage over Time")
    plt.show()