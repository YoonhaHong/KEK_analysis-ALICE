#!/bin/bash
export CORRY=${HOME}/ITS3/corryvreckan/bin/corry

mkdir -p masks
rm -f masks/*.txt
touch masks/ref-plane0.txt masks/ref-plane1.txt  masks/ref-plane2.txt  masks/dut-plane3.txt  masks/ref-plane4.txt  masks/ref-plane5.txt  masks/ref-plane6.txt

$CORRY -c configs/createmask.conf
$CORRY -c configs/prealign.conf
$CORRY -c configs/align.conf
$CORRY -c configs/analyse.conf
