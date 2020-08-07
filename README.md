# Realtime XRP ledger tracking

Created this project to demostrate how easy it is to connect with XRP ledger and perform some realtime analysis using ripple python SDK.

## Getting Started

Below are the instructions to copy of the project up and running on your local machine for testing purposes.

### Prerequisites

1. Python3+

2. Gnuplot tool for graph plotting.

Note: Below command is for Mac users only, please follow http://www.gnuplot.info/ for linux/Ubuntu installation
   ```
   brew install gnuplot
   ```

3. We must install required python packages, please review requirement.txt file and install all python dependencies via pip.

   ```
   git clone https://github.com/yadavj795/ripple-assignment.git
   cd ripple-assignment
   pip install -r requirements.txt
   ```
4. We are also leveraging LevelDB key-value data store in our application, therefore, please make sure we have leveldb install on the node.

   Note: Below step is for MacOS users only, please follow https://computingforgeeks.com/how-to-install-leveldb-on-ubuntu-18-04-ubuntu-16-04/ for linux         installation
   ```
   brew install leveldb
   ```

### Running Application

Below are the steps to run the python application which will connect to Ripple XRP ledger and fetch required information and ingest data into LevelDB. Then, it will pull all the key values from it and add into a flat data file.

1. Run ledger_info.py

   ```
   cd ripple-assignment
   python ledger_info.py
   ```
Once we run above command, we will start seeing ledger validation timings i.e. min,max and avg time taken metrics.

   ```
   (base) jyadav-mbp:ripple-assignment jyadav$ python ledger_info.py 
   Ledger Validation Time  => Maximum Value: 3.01 , Minimum Value: 2.02 , Avarage Value: 2.92
   ```
This stdout ouptut will keep updating every second and values will be refreshed.

Note: Please run this script for few minutes so that we can get enough dataset for graph plotting. Then we can simply do CTL+C to kill the python program

2. This application will also create a flat data file called "/tmp/ledger_info.dat" which contains ledger sequence number and timestamp. Now we will use this data file to plot the graph, we will use our plot script sample-plot.p file.

   ```
   gnuplot -p sample-plot.p
   ```
This will create a graph UI window like below.


End with an example of getting some data out of the system or using it for a little demo

### Q&A

# 1.How does your script work?.
# Answer: 


# 2.How did you decide on your polling interval?
# Answer: 


# 3.What do the results tell you?
# Answer: 


# 4.What might explain the variation in time between new ledgers? (this description of the consensus algorithm may help you: https://developers.ripple.com/consensus-principles-and-rules.html)
# Answer: 
