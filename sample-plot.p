set xdata time
set timefmt "%s"
set format x "%m/%d/%Y %H:%M:%S"
plot "/tmp/ledger_info.dat" using 1:2 with linespoints
