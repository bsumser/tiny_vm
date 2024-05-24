.local x
const 42
const 21
call Int:plus
const 21
call Int:plus
const 17
store x
const 1
const 2
call Int:Equals
jump_ifnot label1
const 21
const 23
call Int:minus
jump label0
label1:
const 1
const 3
call Int:Equals
jump_ifnot label2
const 21
const 23
call Int:divi
jump label0
label2:
const 71
const 87
call Int:plus
jump label0
label0:
const 69
const 69
call Int:plus
