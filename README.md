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

   Note: Below step is for MacOS users only, please follow https://computingforgeeks.com/how-to-install-leveldb-on-ubuntu-18-04-ubuntu-16-04/ for linux           installation
   ```
   brew install leveldb
   ```

### Running Application

Below are the steps to run the python application which will connect to Ripple XRP ledger and fetch required information and ingest data into LevelDB. Then, it will pull all the key values from it and add into a flat data file.

1. Run ledger_info.py python script

   ```
   cd ripple-assignment
   python ledger_info.py
   ```
Once we run above command, we will start seeing ledger validation timings i.e. min,max and avg time taken metrics.

   ```
   (base) jyadav-mbp:ripple-assignment jyadav$ python ledger_info.py 
   Ledger Validation Time  => Maximum Value: 3.01 , Minimum Value: 2.02 , Avarage Value: 2.92
   ```
The stdout of this script will keep updating every second and values will be refreshed.

Note: Please run this script for few minutes so that we can get enough dataset for graph plotting. Then we can simply do CTL+C to kill the python program

2. This application will also create a flat data file called "/tmp/ledger_info.dat" which contains ledger sequence number and timestamp. Now we will use this data file to plot the graph, we will use our plot script sample-plot.p file.

   ```
   gnuplot -p sample-plot.p
   ```
This will create a graph UI window like below.


End with an example of getting some data out of the system or using it for a little demo

### Q&A

#### 1.How does your script work?.
#### Answer: 
This script is using ripple python SDK to connect with ripple node. Once connected, we are calling rippled RPC.server_info() method to pull latest information on the current ledger. This result set then converted from dict to json object for further parsing, afterwards we are fetching ledger sequence number from json object and calculating current time along with that. 

We then storing this ledger seq number and corresponding timestamp in a levelDb data store, this leveldb store has seq field as a key and timestamp as an value. By doing this we will make sure that our dataset doesn't contain duplicates sequence number instead will only update the timestamp for the same key if it exist as RPC.server_info() method could return same sequence every time unless next ledger sequence is generated during poll time, these whole steps are happening inside method called get_server_info(). Afterwards, we are pulling all the unique keys/values and loading into a flat file using method flat_file_writer(). 

Method dict_mean() does all the metric calculation for min, max and avg ledger validation time taken, we are using python dictionary to store the last_close.converge_time_s field which has actually value of ledger closer time. We are dynamically storing all these info for each ledger and calculating min, max and avg metrics(using numpy).


### 2.How did you decide on your polling interval?
### Answer: 
While testing the application I found out that the average ledger validation/close time was around 3 seconds, however, there were some variances noticed as well.
Also, reducing poll time to less than 3 seconds was causuing duplicate sequence numbers recorded and if that was more than 3 secs then we were seeing missing sequence number in the output. Therefore, I decided to introduce LevelDB key/value store which helped to tackle these issues, now we can use even small poll time i.e. 1 sec which will make sure that we won't have missing sequence number and leveldb will keep the uniqueness of sequence keys and it will be a low latency output application.


### 3.What do the results tell you?
### Answer: 
Results illustrate that the average ledger validation/closer time is around 3 secs, however, there were instances where network took more time to close the ledger i.e. 4+ secs.


### 4.What might explain the variation in time between new ledgers? (this description of the consensus algorithm may help you: https://developers.ripple.com/consensus-principles-and-rules.html)
### Answer: 
There could be several reasons due to which new ledgers time varies time to time, one of the major cause is Byzantine failures where agreement could not be completed within time between netowork participants. Failures like hardware failures, communication failures, and even dishonest participants are few causes of the delay. Other cause of deplay could be due to network congestion and failure of consensus, though consensus round is much less likely to fail because disagreements are resolved in the consensus process and only remaining disagreements can cause a failure.
