# How to configure this simulator
You can specify relevant parameters in the heqsim/middleware/config.ini

| Parameter name | Type  |              Explanation               |
| :------------: | :---: | :------------------------------------: |
|   qubit_num    |  int  |              # of qubits               |
|      time      | float | Execution time of a local quantum gate |

E.g.

```
[Processor name]
qubit_num = 1
time = 0.1
```