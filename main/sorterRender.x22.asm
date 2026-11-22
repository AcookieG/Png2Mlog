print "By [pink]A[salmon]K[orange]a[gold]y[yellow]oC[]o[]o[]k[]ie[] LINE {Y+1} COLUMN {X+1}"
set n 0
set li 0
set VAR "{INSERTTEXTHERE}"
sensor blockSize VAR @size
set array @links
read pixel VAR n
getlink link li
op add li li 1
op add n n 1
op sub pixel pixel 60
lookup item pixel pixel
control config link pixel 0 0 0
jump 5 lessThan li array
jump 18 equal STOP 1
set li 0
jump 5 lessThan n blockSize
write "STOP" processor1 STOP
