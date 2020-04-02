An edge computing framework

The directory layout explains the code



├── Master

​	  		└── node.py                        *the main controller*     

├── benchmark

​			   ├── benchmark.py             *tasks to run on edge devices*

​			  └── redis_benchmark.py

├── logger.py                                   *for logging*

├── monitor

​	 └── monitor.py                         *analyze data on master*

├── regx.py

├── reporter                                    *run on edge to collect data*

│  └── sar.py

└── utils

  ├── docker.py                              *module for master to interact with docker*

  ├── ssh.py                                   *module for ssh connections*

