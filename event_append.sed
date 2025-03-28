/.*jk2_init\(\) Found child [0-9]* in scoreboard slot [0-9]*/ s/(.*)/\1,E1,jk2_init\(\) Found child <*> in scoreboard slot <*>/
/.*workerEnv.init\(\) ok .*/ s/(.*)/\1,E2,workerEnv.init() ok <*>/
/.*mod_jk child workerEnv in error state [0-9]*/ s/(.*)/\1,E3,mod_jk child workerEnv in error state <*>/
/.*\[client .*\] Directory index forbidden by rule: .*/ s/(.*)/\1,E4,\[client <*>\] Directory index forbidden by rule: <*>/
/.*jk2_init\(\) Can't find child [0-9]* in scoreboard/ s/(.*)/\1,E5,jk2_init\(\) Can't find child <*> in scoreboard/
/.*mod_jk child init [0-9\-\s]*/ s/(.*)/\1,E6,mod_jk child init <*> <*>/