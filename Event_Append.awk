BEGIN {
    FS = ",";
    OFS = ",";
}

/jk2_init\(\) Found child [0-9]* in scoreboard slot [0-9]*/ {
    #An E1 event.
    print $0, "E1,jk2_init() Found child <*> in scoreboard slot <*>";
}