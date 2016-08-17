#!/bin/bash

N=4
i=0

while [ $i -lt $N ] ; do
    printf "%5d%-5s%5s%5d%8.3f%8.3f%8.3f%8.4f%8.4f%8.4f\n" 1 SOL OW1 1 0.0 0.0 0.0 0.0 0.0 0.0
    printf "%5d%-5s%5s%5d%8.3f%8.3f%8.3f%8.4f%8.4f%8.4f\n" 1 SOL HW2 1 0.0 0.0 0.0 0.0 0.0 0.0
    printf "%5d%-5s%5s%5d%8.3f%8.3f%8.3f%8.4f%8.4f%8.4f\n" 1 SOL HW3 1 0.0 0.0 0.0 0.0 0.0 0.0
    i=$[ $i + 1 ]
done
 