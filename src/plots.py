import numpy as np
import matplotlib.pyplot as plt

import atmos as atm


def add_labels(grp, labels, pos, fontsize, fontweight='bold'):
    """Add labels to subplots in a figure
    
    Parameters
    ----------
    grp : atm.FigGroup object
        Instance of atm.FigGroup class for the subplots to annotate
    labels : list
        Labels to annotate, e.g. ['a', 'b', 'c']
    pos : list of tuples
        Positions for each label
    fontsize, fontweight
        Text parameters for labels
    """
    try:
        n = len(pos[0])
    except TypeError:
        pos = [pos] * len(labels)
    row, col = 0, 0
    for i in range(len(labels)):
        grp.subplot(row, col)
        atm.text(labels[i], pos[i], fontsize=fontsize,
                 fontweight=fontweight)
        col += 1
        if col == grp.ncol:
            col = 0
            row += 1
    return None


def contourf_latday(var, is_precip=False, clev=None, cticks=None, climits=None,
                    nc_pref=40, grp=None,
                    xlims=(-120, 200), xticks=np.arange(-120, 201, 30),
                    ylims=(-60, 60), yticks=np.arange(-60, 61, 20),
                    dlist=None, grid=False, ind_nm='onset', xlabels=True):
    """Create a filled contour plot of data on latitude-day grid.
    """
    var = atm.subset(var, {'lat' : ylims})
    vals = var.values.T
    lat = atm.get_coord(var, 'lat')
    days = atm.get_coord(var, 'dayrel')
    if var.min() < 0:
        symmetric = True
    else:
        symmetric = False
    if is_precip:
        cmap = 'PuBuGn'
        extend = 'max'
    else:
        cmap = 'RdBu_r'
        extend = 'both'
        
    if clev == None:
        cint = atm.cinterval(vals, n_pref=nc_pref, symmetric=symmetric)
        clev = atm.clevels(vals, cint, symmetric=symmetric)
    elif len(atm.makelist(clev)) == 1:
        if is_precip:
            clev = np.arange(0, 10 + clev/2.0, clev)
        else:
            clev = atm.clevels(vals, clev, symmetric=symmetric)

    plt.contourf(days, lat, vals, clev, cmap=cmap, extend=extend)
    plt.colorbar(ticks=cticks)
    plt.clim(climits)
    atm.ax_lims_ticks(xlims, xticks, ylims, yticks)
    plt.grid(grid)

    if dlist is not None:
        for d0 in dlist:
            plt.axvline(d0, color='k')
    if xlabels:
        plt.gca().set_xticklabels(xticks)
        plt.xlabel('Days Since ' + ind_nm.capitalize())
    else:
        plt.gca().set_xticklabels([])
    if grp is not None and grp.col == 0:
        plt.ylabel('Latitude')
        
    return None


def contourf_londay(var, clev=None, grp=None,n_pref=40,
                   yticks=np.arange(-120, 201, 30)):
    """Create a filled contour plot of data on longitude-day grid.
    """
    lon = atm.get_coord(var, 'lon')
    days = atm.get_coord(var, 'dayrel')
    if clev is None:
        cint = atm.cinterval(var, n_pref=n_pref, symmetric=True)
        clev = atm.clevels(var, cint, symmetric=True)
        
    plt.contourf(lon, days, var, clev, cmap='RdBu_r', extend='both')
    plt.colorbar()
    plt.yticks(yticks)
    plt.axhline(0, color='0.5', linestyle='--', dashes=[6, 1])
    if grp is not None and grp.row == grp.nrow - 1:
        plt.xlabel('Longitude')
    if grp is not None and grp.col == 0:
        plt.ylabel('Days Since Onset')