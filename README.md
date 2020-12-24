# MachineLearning with SKLearn (Dynamic Analysis)

Similar to **[MachineLearning-Static](https://github.com/SJash96/MachineLearning-Static)** repository but performed dynamically using pyshark which is a wrapper for tshark (a terminal based wireshark network analyzer) that does IDS (Intrusion Detection System) using SKlearn Machine Learning libraries.
Test is performed from three computers where one (victim) hosts the packet capturing application, one sends malicious packets and attacks (attacker), and last one which performs IDS from the victim machine.
The victim computer gets attacked while browsing to show benigin data with attack or malicious data. This data get processed and is run through the Machine Learning IDS tool which can then later predict future attacks or benign data.
