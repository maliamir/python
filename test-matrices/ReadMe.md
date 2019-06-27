[Demo](https://www.youtube.com/watch?v=JkOnlgDbHhk)

# Introduction
This is a simple flask (a python based micro web-framework) web-application which exposes GET & POST actions against an end-point "/matrices" to SELECT & INSERT test-matrices from & into a Cassandra based keyspace respecitvely.

# Install Python 3.7+
1. Download & install 3.7+ Python from:
   https://www.python.org/downloads/

2. Install pip as:
   Download: https://bootstrap.pypa.io/get-pip.py then
   /usr/local/bin/python3.7 get-pip.py

3. Set Proxy (if necessary):
   export https_proxy="http://www-proxy.host.name.com:80"

4. Install Flask:
   /usr/local/bin/pip3.7 install flask

5. Install Cassandra:
   pip install cassandra-driver


# Installing Cassandra on Mac OS X
1. Install Homebrew (a Simple Package Manager for OS X):
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

2. Install Apache Cassandra:
    brew install cassandra

3.  /usr/local/bin/pip3.7 install cql

4. To have launchd start cassandra now and restart at login:
      brew services start cassandra &
Or, if you don't need a background service you can just run:
     cassandra -f &

5. Run cqlsh -f cassandra_setup.cql. This will create kay space, table and one sample record.


# Download & install IDE: PyCharm and run web-application
1. Download & install PyCharm from:
    https://www.jetbrains.com/pycharm/download

2. Open this python project in PyCharm and then run "test_metrics.py”

Both GET & POST are supported against end-point http://host:5000/matrices 

GET Sample Payload:
`[  
   {  
      "log_stamp":"2019-06-10 22:58:37.551000",
      "matrix":[  
         {  
            "testUnitName":"ApplicationCreation",
            "duration":53523
         },
         {  
            "testUnitName":"ApplicationDeletion",
            "duration":3525235
         }
      ]
   },
   {  
      "log_stamp":"2019-06-10 22:12:51.591000",
      "matrix":[  
         {  
            "testUnitName":"ApplicationCreation",
            "duration":23194
         },
         {  
            "testUnitName":"ApplicationDeletion",
            "duration":5297
         }
      ]
   }
  ]`

POST Sample Payload:
`{
   “matrices”:[  
         {  
            "testUnitName":"ApplicationCreation",
            "duration":53523
         },
         {  
            "testUnitName":"ApplicationDeletion",
            "duration":3525235
         }
      ]
 }`
