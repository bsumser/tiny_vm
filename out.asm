const 25
const 17
call Int:plus
store x
const 0
store y
load x
const 25
call Int:Equals
jump_ifnot label0
const 25
load x
call Int:plus
store y
jump label0
label0:
load y
return 1
