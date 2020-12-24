# MachineLearning with SKLearn (Dynamic Analysis)

Similar to **[MachineLearning-Static](https://github.com/SJash96/MachineLearning-Static)** repository but performed dynamically using pyshark which is a wrapper for tshark (a terminal based wireshark network analyzer) that does IDS (Intrusion Detection System) using SKlearn Machine Learning libraries.
Test is performed from three computers where one (victim) hosts the packet capturing application, one sends malicious packets and attacks (attacker), and last one which performs IDS from the victim machine.

## Preperations

Before starting the dynamic Machine Learning IDS, the program needs a pre-supplied data to work off of. This data can be given initially with identification of each packets (including malicious packets) and the file can later be updated to accomodate new types of attacks.

## What Happens

The victim machine does casual browsing on the internet showing benign data through the IDS until the attacker sends malicious packets. The Machine Learning IDS will run the Decision Tree model and dynamically print out its future predictions on incoming packets which gets printed out to the console (labeled packets that show if the packet is benign or a speicific attack).
