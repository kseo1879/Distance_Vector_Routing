# COMP3221 Assignment1 Distance Vector Routing

## How to use
1. Open five different terminals. 
```bash
python3 COMP3221_DiVR.py A 6000 config/Aconfig.txt
```
Then let each terminal have there own command with different node id and port no and different files. 

## Result

These are the result of runnign for each node. 

1. Node A
```bash
python3 COMP3221_DiVR.py A 6000 config/Aconfig.txt
I am node A
Least cost path from A to B: AB: 6.1
Least cost path from A to D: AD: 2.3
Least cost path from A to E: AE: 2.2
Least cost path from A to C: ABC: 12.6

I am node A
Least cost path from A to B: AEB: 2.4000000000000004
Least cost path from A to D: AD: 2.3
Least cost path from A to E: AE: 2.2
Least cost path from A to C: ADC: 5.5
```

2. Node B
```bash
python3 COMP3221_DiVR.py B 6001 config/Bconfig.txt
I am node B
Least cost path from B to A: BA: 6.1
Least cost path from B to C: BC: 6.5
Least cost path from B to E: BE: 0.2
Least cost path from B to D: BAD: 8.399999999999999

I am node B
Least cost path from B to A: BEA: 2.4000000000000004
Least cost path from B to C: BC: 6.5
Least cost path from B to E: BE: 0.2
Least cost path from B to D: BEAD: 4.7
```

3. Node C
```bash
python3 COMP3221_DiVR.py C 6002 config/Cconfig.txt.txt
I am node C
Least cost path from C to B: CB: 6.5
Least cost path from C to D: CD: 3.2
Least cost path from C to A: CBA: 12.6
Least cost path from C to E: CBE: 6.7

I am node C
Least cost path from C to B: CB: 6.5
Least cost path from C to D: CD: 3.2
Least cost path from C to A: CDA: 5.5
Least cost path from C to E: CBE: 6.7
```


4. Node D
```bash
python3 COMP3221_DiVR.py D 6003 config/Dconfig.txt.txt
I am node D
Least cost path from D to A: DA: 2.3
Least cost path from D to C: DC: 3.2
Least cost path from D to B: DAB: 8.399999999999999
Least cost path from D to E: DAE: 4.5

I am node D
Least cost path from D to A: DA: 2.3
Least cost path from D to C: DC: 3.2
Least cost path from D to B: DAEB: 4.7
Least cost path from D to E: DAE: 4.5
```


5. Node E
```bash
python3 COMP3221_DiVR.py E 6004 config/Econfig.txt.txt
I am node E
Least cost path from E to A: EA: 2.2
Least cost path from E to B: EB: 0.2
Least cost path from E to C: EBC: 6.7
Least cost path from E to D: EAD: 4.5
```

