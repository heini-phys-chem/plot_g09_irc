#!/usr/bin/env python3

import sys
import cclib
import numpy as np


import matplotlib.pyplot as plt
import seaborn as sns

NAMES = {1:'H', 6:'C', 8:'O'}


def read_data(f):
    return cclib.io.ccread(f)

def extract_properties(data, rp_order):
    energies = data.scfenergies

    for i, e in enumerate(energies):
        if i == 0: continue
        if energies[i] - energies[i-1] > 0:
            react_min_idx = i-1

    if rp_order == "prod-react":
        energies -= energies[-1] # substract reactant energy from all points
    elif rp_order == "react-prod":
        energies -= energies[react_min_idx]
    else:
        print("Please choose a reactant and product order ('react-prod' or 'prod-react')")
        exit()

    energies *= 23 # convert from eV to kcal/mol

    coords = data.atomcoords

    labels = data.atomnos
    numAtoms = data.natom


    return energies, coords, labels, numAtoms, react_min_idx

def plot_irc(y):
    x = np.linspace(0, y.shape[0], y.shape[0])

    fig, ax = plt.subplots(figsize=(6,6))

    ax.set_xlabel("IRC")
    ax.set_ylabel(r'$E$ [kcal/mol]')

    sns.scatterplot(x=x, y=y, color="C0", ax=ax)
    sns.lineplot(x=x, y=y, color="C0", ax=ax)

    plt.tight_layout()

    fig.savefig("irc.png")


def split_energies(energies, rp_order, react_min_idx):
    e_react = np.array([])
    e_prod  = np.array([])

    if rp_order == "prod-react":
        for i in range(react_min_idx):
            e_prod = np.append(e_prod, energies[i])
        for i in range(react_min_idx+1, energies.shape[0]):
            e_react = np.append(e_react, energies[i])

        e_react = np.flip(e_react)

    elif rp_order == "react-prod":
        for i in range(react_min_idx):
            e_react = np.append(e_react, energies[i])
        for i in range(react_min_idx+1, energies.shape[0]):
            e_prod = np.append(e_prod, energies[i])

        e_react = np.flip(e_react)


    return e_react, e_prod

def write_coords(coords, labels, numAtoms, rp_order, react_min_idx):
    coords_prod  = []
    coords_react = []

    if rp_order == "prod-react":
        for i in range(react_min_idx):
            coords_prod.append(coords[i])
        for i in range(react_min_idx, coords.shape[0]):
            coords_react.append(coords[i])
    else:
        for i in range(react_min_idx):
            coords_react.append(coords[i])
        for i in range(react_min_idx, coords.shape[0]):
            coords_prod.append(coords[i])


    coords_react.reverse()
    coords_react = np.asarray(coords_react)
    coords_prod  = np.asarray(coords_prod)
#    coords_react = np.flip(coords_react)

    coords_new = np.concatenate((coords_react, coords_prod), axis=0)

    f = open("irc.xyz", 'w')
    for mol in coords_new:
        f.write("{}\n\n".format(numAtoms))
        for i, atom in enumerate(mol):
            f.write("{} {} {} {}\n".format(labels[i], atom[0], atom[1], atom[2]))
    f.close()

    return coords_new


def main():
    filename         = sys.argv[1]
    react_prod_order = sys.argv[2]

    data = read_data(filename)

    energies, coords, labels, numAtoms, react_min_idx = extract_properties(data, react_prod_order)
    e_react, e_prod = split_energies(energies, react_prod_order, react_min_idx)
    energies = np.concatenate((e_react, e_prod), axis=0)

    coords = write_coords(coords, labels, numAtoms, react_prod_order, react_min_idx+1)

    plot_irc(energies)


if __name__ == '__main__':
    main()

