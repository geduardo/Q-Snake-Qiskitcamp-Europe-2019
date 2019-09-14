# Qiskitcamp hackathon: Q-Snake

## Introduction
In this project we have created a very simple game based in the memorable classical game [Snake](https://en.wikipedia.org/wiki/Snake_(video_game_genre)). Our work is written on python and qiskit (together with its reduced version "aether") and we use a programmable console called "Pew Pew". The game has different modes and is meant to be a very simple introduction to quantum programming with Qiskit and programming in general. Due to its simplicity its ideal to introduce Quantum Computing to High School students with zero background of programming or quantum mechanics, for example in the form of workshops.
The game has different modes:
+ Q-Python
+ Q-Python Plus
+ Q-Python Circuit

## Q-Python 
It is the simplest version of Q-Python and the only one that runs in the Pew Pew console (due to memory constraints). The game is similar to the classic game of Snake with the difference being the method by which the apples spawn. In the classic version, these apples are spawned randomly via a classical random generator. In the quantum version, this spawning is facilitated via a quantum random generator. This quantum random generator is implemented by performing measurement a qubit on a superposition. There is also a simple barrier mechanic that the snake can penetrate through quantum tunneling with some probability.
## Q-Python Plus
This mode is simliar to Q-Python but runs on a PewPew emulator due to the stated memory constraints. Again, the spawning of the apples are via quantum random generator. This mode, however, implementing more reastically through the actual equations and measurements made on qubits. This introduces concepts such as quantum tunneling and the bloch sphere. 

## Q-Python Circuit
This mode involves creating a simple circuit. The goal of the game is to reach a final state of ket 1 starting from an initial state of ket 0 given the limitation that one can only use H, Z, or a measurement operation As the snake eats apples, one is tasked to select either of the options. If the user is unable to do so, then he loses. The user must also avoid randomly generated noise that also lead to a game over upon collision. 

## Licences
The original snake game and the original pew simulator are taken from
https://github.com/pewpew-game
Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) License
author: 2019 by Radomir Dopieralski

The compressed version of qiskit (aether) is taken from
https://github.com/quantumJim/aether
(Apache 2.0 licence)
author: quantumJim
