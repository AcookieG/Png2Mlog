set n 0
set li 0
set VAR "INSERTTEXTHERE"
sensor blockSize VAR @size
op sub array @links 1
read pixel VAR n
getlink link li
op add li li 1
op add n n 1
op sub pixel pixel 60
lookup item pixel pixel
control config link pixel 0 0 0
jump 5 lessThan li array
jump 36 equal STOP 1
write "STOP" processor1 STOP
set li 0
jump 5 lessThan n blockSize
end
