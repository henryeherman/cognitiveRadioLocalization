----------------
  Disclaimer
----------------

The materials provided at this Web site are for use solely for research and educational purposes and NOT for operational or
commercial purposes. The publisher of this data disclaim liability of any kind whatsoever, including, without limitation, liability for
quality, performance, merchantability and fitness for a particular purpose arising out of the use, or inability to use the data.

If you use the material (e.g., in scientific publications, talks and so on) you are kindly invited to refer its source.

-----------------------
 About collected data
-----------------------

These measurements were collected in four testbeds, named SIGNET lab, Corridor (or IAS lab), Lecture Hall and Opportunistic testbed.

- SIGNET lab testbed -
These measurements were collected in the SIGNET Researech Lab testbed
at Department of Information Engineering, University of Padova. The testbed consisted in a grid of 48 nodes deployed in the SIGNET laboratory, 50 cm from the ceiling.
In the experiments with EYES-IFXv2 sensor platform (www.infineon.com) every node tried to send packets to each other node on a single channel.
In the experiments with TmoteSKY sensor platform (http://www.sentilla.com/moteiv-transition.html) every node tried to send packets to each other node, over each of the 16 available RF channels.

- Corridor Testbed -
The Corridor (IAS) testbed consists in 10 static sensor nodes and an autonomous mobile robot. The experiment was conducted within the framework of the RAMSES2 University research project that involves the SIGNET Research Group and IAS Research Group at the Department of Information Engineering, University of Padova. The sensor nodes were positioned in a grid (two rows of 4 nodes and a row of 2 nodes). The mobile robot moved along a pre-planned path and periodically broadcasted its position to the static sensors.
No measurements between static nodes were taken.

- Lecture Hall testbed -
These measurements were collected in the Lecture Hall "Antonio Lepschy" of the University of Padova, Department of Information Engineering.
The testbed consisted in 25 nodes deployed on the chairs of the Hall as in the file Lectuyre_Hall_testbed.eps. Every node tried to send packets to each other node over all the 16 available RF channels.


- Opportunistic Testbed
The experiments were conducted in a room measuring approximately 9mx11m with 2 m high ceiling in the lowest zone. The room was empty except for the center support beam. We took into consideration a rectangular area (7.2 m x 9 m) in the room and we drew a grid on the floor where, as shown in figure 1. The sensor nodes were deployed on cones at 30 cm from the floor: the red circles represent the beacon nodes which transmit their known position to the mobile nodes that perform autolocalization (using the well-known Min-Max algorithm [2]). The blue circles represent the mobile nodes and the black line shows the path covered by a mobile node, called opportunistic node, weÕll refer to during the emulation to study the localization algorithm performances. The path is composed of 120 positions at which the opportunistic node transmits a message, after it has performed autolocalization, trying to establish a link with another mobile node that will replay if the RSSI measurement for that message is over a threshold. Similarly the opportunistic node will accept the replay if the RSSI sample is over the same threshold. We then collected, for every opportunistic nodeÕs position, the RSSI samples by the 24 mobile nodes and used them to find out channel parameters and to emulate the opportunistic interactions.

--------------------
References
-------------------

For more informations, please see the papers

ZANCA G., ZANELLA A., ZORZI F. ZORZI M. Experimental comparison of RSSI-based localization algorithms for indoor wireless sensor networks REALWSNÕ08. Glasgow, Scotland, UK. April 1, 2008.

ZANELLA A., MENEGATTI E, LAZZARETTO L. SelfÐlocalization of Wireless Sensor Nodes by means of Autonomous Mobile Robots In: Proceedings of TIWDC Õ07, Ischia Island, Napoli, Italy. 9-12 Sep. 2007.

R.CREPALDI, S.FRISO, ALBERT F.HARRIS III, M.MASTROGIOVANNI, C.PETRIOLI, M.ROSSI, ZANELLA A., M.ZORZI. (2007). The design, deployment, and analysis of SignetLab: a sensor network testbed and interactive management tool. TRIDENTCOM 2007. Orlando, Florida, USA. May 21 - 23. IEEE International Conference on Testbeds and Research Infrastructures for the Development of Networks and Communities.



------------------
 Contents
-----------------

Data are structured in matrixes, available both in Matlab (MAT) and CSV
formats.

EyesIFX nodes allow for two different settings of the receiver amplifier, namely High and Low. In case of SIGNET testbed, we have collected two sets of data, one for each setting. IAS data, conversely, were obtained with the Low setting.

The file name reflects these different cases.

The data matrixes are formatted as follows

ID_tx ID_rx X_tx Y_tx Z_tx X_rx Y_rx Z_rx Pr LQI RSSI SN t P_tx f Hw
(16 fields in all)

where:

ID_tx is the ID of the transmitter node
ID_rx is the ID of the receiver node
X_tx is the X coordinate in the grid of the TX-node (in meters)
Y_tx is the Y coordinate in the grid of the TX-node (in meters)
Z_tx is the Z coordinate in the grid of the TX-node (in meters)
X_rx is the X coordinate in the grid of the RX-node (in meters)
Y_rx is the Y coordinate in the grid of the RX-node (in meters)
Z_rx is the Z coordinate in the grid of the RX-node (in meters)
Pr is the received power in dBm
LQI is the LQI value given by the transceiver (NaN if not supported by the hardware)
RSSI is the raw RSSI value given by the mote (NaN if not supported by the hardware)
SN is the Serial Number of the packet
t is the timestamp of the packet (in millisecond)
P_tx is the transmit power
f is the carrier frequency (in MHz)
Hw is a character representing the hardware platform (e = Eyes)

NaN -> data not available

-----------------------
 Credits
----------------------

Data have been collected by the following persons:

Francesco Zorzi		(zorzifra@dei.unipd.it)
Emanuele Menegatti	(emg@dei.unipd.it)
Andrea Zanella          (zanella@dei.unipd.it)
Michele Zorzi           (zorzi@dei.unipd.it)
Luca Lazzaretto
Giovanni Zanca
Francesco Triolo

SIGNET research group
Department of Information Engineering, University of Padova, Italy

website: http://telecom.dei.unipd.it/signet
