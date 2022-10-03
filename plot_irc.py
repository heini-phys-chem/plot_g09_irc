#!/usr/bin/env python3

import sys
import cclib
import numpy as np


import matplotlib.pyplot as plt
import seaborn as sns

NAMES = {1:'H', 6:'C', 8:'O'}


def read_data(f):
    return cclib.io.ccread(f)

def extract_properties(data):
    energies = data.scfenergies

    energies -= energies[-1] # substract reactant energy from all points
    energies *= 23 # convert from eV to kcal/mol

    coords = data.atomcoords

    labels = data.atomnos
    numAtoms = data.natom
#    print()
#    for i, atom in enumerate(coords[0]):
#        print(labels[i], atom[0], atom[1], atom[2])


    return energies, coords, labels, numAtoms

def plot_irc(y):
    x = np.linspace(0, y.shape[0], y.shape[0])

    fig, ax = plt.subplots(figsize=(6,6))

    ax.set_xlabel("IRC")
    ax.set_ylabel(r'$E$ [kcal/mol]')

    sns.scatterplot(x=x, y=y, color="C0", ax=ax)
    sns.lineplot(x=x, y=y, color="C0", ax=ax)

    plt.tight_layout()

    fig.savefig("tmp.png")


def split_energies(energies):
    e_react = np.array([])
    e_prod  = np.array([])

    for i, e in enumerate(energies):
        if i == 0: continue
        if energies[i] - energies[i-1] > 0:
            j = i
    for i in range(j):
        e_prod = np.append(e_prod, energies[i])
    for i in range(j+1, energies.shape[0]):
        e_react = np.append(e_react, energies[i])

    e_react = np.flip(e_react)

    return e_react, e_prod

def write_coords(coords, labels, numAtoms):
    print(coords.shape)
    coords_prod  = []
    coords_react = []

    for i in range(52):
        coords_prod.append(coords[i])
    for i in range(52, coords.shape[0]):
        coords_react.append(coords[i])


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
    filename = sys.argv[1]

    data = read_data(filename)

    energies, coords, labels, numAtoms = extract_properties(data)
    e_react, e_prod = split_energies(energies)
    energies = np.concatenate((e_react, e_prod), axis=0)

    coords = write_coords(coords, labels, numAtoms)

    plot_irc(energies)
    print(coords.shape)


if __name__ == '__main__':
    main()

