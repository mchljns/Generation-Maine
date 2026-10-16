#!/bin/bash
# diff a baseline log against mine with timings stripped (the fix4-front difflogs.sh normalization). usage: difflog.sh <baseline> <mine>
norm() { sed -E -- 's/[0-9]+ ?ms//g; s/t=[0-9]+//g; s/load [0-9.]+//g' "$1"; }
diff <(norm "$1") <(norm "$2") | head -${N:-40} | cut -c1-300
