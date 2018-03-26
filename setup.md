# Installation
Ubuntu Desktop

```
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get install redis-server git python-pip screen python-yaml
```
OSX

```
installing the above with homebrew/OS utilities should get you going
brew install redis
brew install screen
brew install git

brew install python (if you want to install via homebrew) Metta uses Python 2.7 but a fresh homebrew install with install Python 3. some links below to help you with this. Install python 2.7 with homebrew or use pyenv to install Python 2.7
sudo easy_install pip
```

Set up a virtual python enviroment in the repo folder
ref: http://docs.python-guide.org/en/latest/dev/virtualenvs/
```
pip install --user pipenv

git clone https://github.com/uber-common/metta.git
cd metta

virtualenv metta
source metta/bin/activate
pip install -r requirements.txt

```

* Metta requires Python 2.7 
* If you are getting import errors on workers.vagranttasks or BaseConfig you should declare a different Python environment when creating the virtualenv.
```
virtualenv --python=<path to preferred python> metta
```

Python and Homebrew: http://docs.python-guide.org/en/latest/starting/install/osx/

pyenv and homebrew python3/2.7 https://stackoverflow.com/questions/18671253/how-can-i-use-homebrew-to-install-both-python-2-and-3-on-mac


# VirtualBox setup
Install virtualbox for your OS https://www.virtualbox.org/wiki/Downloads

# Vagrant setup

Download vagrant from the vagrant homepage (the one from the repository doesnt allow the winrm plugin installation)
https://www.vagrantup.com/downloads.html

```
$ sudo dpkg -i vagrant_2.0.0_x86_64.deb 
Selecting previously unselected package vagrant.
(Reading database ... 179795 files and directories currently installed.)
Preparing to unpack vagrant_2.0.0_x86_64.deb ...
Unpacking vagrant (1:2.0.0) ...
Setting up vagrant (1:2.0.0) ...
```

You need to install the vagrant winrm plugin (https://github.com/criteo/vagrant-winrm)
```
vagrant plugin install vagrant-winrm
```

Set up your vagrants
* If you just want to download a Windows vagrant to get going, you can check the documentation here: 
(https://github.com/uber-common/metta/wiki/Vagrants)

* If you want to build your own box. I recommend building the the virtual machine inside virtualbox then converting it to a vagrant "box"
  * ref: (https://www.vagrantup.com/docs/virtualbox/boxes.html)

* Set passwords and enable winrm on the windows host so the winrm-* plugins will work
  * ref: https://www.vagrantup.com/docs/boxes/base.html (windows section)
  * ```vagrant winrm -c whoami ```     -- should work

* Install any instrumentation you need to install (sysmon, EDR products, syslog, etc)

* If you need some backgroun on a vagrant file with multiple machines check here: (https://www.vagrantup.com/docs/multi-machine/)

>>>
** IMPORTANT  update config.ini to point to the virtualbox/vagrant boxes location  (see below)
>>>

# Cloud && Vagrant

rackspace

https://github.com/mitchellh/vagrant-rackspace

AWS

https://github.com/mitchellh/vagrant-aws
see the vagrant folder /aws/ for Vagrantfile and user_data.txt

* needs vagrant plugin install inifile
* needs vagrant plugin install vagrant-aws
* needs vagrant plugin install vagrant-winrm

ref: https://gist.github.com/mkubenka/33b542cbd82614fe7f8b

Linode

https://github.com/displague/vagrant-linode

Others

https://www.vagrantup.com/docs/providers/

## Setup Configuration File 
There are 4 sections to the config.ini file
* [vms]
The items here are the names of the vagrant vms to execute the simulations on
* [reporting]
The items here are for things like the slack integration
* [configuration]
  * The vagrant location variable is the directory where you have the VagrantFile stored for the vms you are using
  * The redis variable is where the hostname/ip address of the redis server you are using 
* [console_log_output] Whether or not you want the information that gets logged to the json log to be displayed to the console (default is false)

```
[vms]
windows=win-vagrant
osx=osx-vagrant
linux=linux-vagrant

[reporting]
slack=https://hooks.slack.com/services/XXXXXX

[configuration]
vagrantlocation=/Users/xxxx/vms/win-vagrant
redis=localhost

[console_log_output]
enabled=false
```

## Confirm redis is running (Run this is its own terminal tab)
```
netstat -pant | grep 6379

user@ubuntu:~/metta$ redis-server 
2867:C 02 Oct 08:20:34.699 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
2867:M 02 Oct 08:20:34.699 * Increased maximum number of open files to 10032 (it was originally set to 1024).
                _._                                                  
           _.-``__ ''-._                                             
      _.-``    `.  `_.  ''-._           Redis 3.0.6 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._                                   
 (    '      ,       .-`  | `,    )     Running in standalone mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
 |    `-._   `._    /     _.-'    |     PID: 2867
  `-._    `-._  `-./  _.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |           http://redis.io        
  `-._    `-._`-.__.-'_.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |                                  
  `-._    `-._`-.__.-'_.-'    _.-'                                   
      `-._    `-.__.-'    _.-'                                       
          `-._        _.-'                                           
              `-.__.-'                                               

2867:M 02 Oct 08:20:34.701 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
2867:M 02 Oct 08:20:34.701 # Server started, Redis version 3.0.6
2867:M 02 Oct 08:20:34.701 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
2867:M 02 Oct 08:20:34.701 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
2867:M 02 Oct 08:20:34.701 * The server is now ready to accept connections on port 6379

```

## Start the celery shell script (Run this is its own terminal tab)

```
(metta) user@ubuntu:~/metta$ ./start_vagrant_celery.sh 
[2017-10-02 08:43:30,368: DEBUG/MainProcess] | Worker: Preparing bootsteps.
[2017-10-02 08:43:30,369: DEBUG/MainProcess] | Worker: Building graph...
[2017-10-02 08:43:30,369: DEBUG/MainProcess] | Worker: New boot order: {StateDB, Beat, Timer, Hub, Pool, Autoscaler, Consumer}
[2017-10-02 08:43:30,375: DEBUG/MainProcess] | Consumer: Preparing bootsteps.
[2017-10-02 08:43:30,375: DEBUG/MainProcess] | Consumer: Building graph...
[2017-10-02 08:43:30,385: DEBUG/MainProcess] | Consumer: New boot order: {Connection, Events, Heart, Mingle, Gossip, Tasks, Control, Agent, event loop}
 
 -------------- vagrant@ubuntu v4.1.0 (latentcall)
---- **** ----- 
--- * ***  * -- Linux-4.10.0-28-generic-x86_64-with-Ubuntu-16.04-xenial 2017-10-02 08:43:30
-- * - **** --- 
- ** ---------- [config]
- ** ---------- .> app:         tasks:0x7fab5854cd90
- ** ---------- .> transport:   redis://127.0.0.1:6379/1
- ** ---------- .> results:     redis://localhost/0
- *** --- * --- .> concurrency: 3 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . celery.accumulate
  . celery.backend_cleanup
  . celery.chain
  . celery.chord
  . celery.chord_unlock
  . celery.chunks
  . celery.group
  . celery.map
  . celery.starmap
  . workers.vagranttasks.alive_vagrant
  . workers.vagranttasks.runcmd_nodb_osx
  . workers.vagranttasks.runcmd_nodb_win
  . workers.vagranttasks.runcmd_osx
  . workers.vagranttasks.runcmd_win

[2017-10-02 08:43:30,393: DEBUG/MainProcess] | Worker: Starting Hub
[2017-10-02 08:43:30,393: DEBUG/MainProcess] ^-- substep ok
[2017-10-02 08:43:30,393: DEBUG/MainProcess] | Worker: Starting Pool
[2017-10-02 08:43:30,444: DEBUG/MainProcess] ^-- substep ok
[2017-10-02 08:43:30,445: DEBUG/MainProcess] | Worker: Starting Consumer
[2017-10-02 08:43:30,445: DEBUG/MainProcess] | Consumer: Starting Connection
[2017-10-02 08:43:30,486: INFO/MainProcess] Connected to redis://127.0.0.1:6379/1
[2017-10-02 08:43:30,486: DEBUG/MainProcess] ^-- substep ok
[2017-10-02 08:43:30,486: DEBUG/MainProcess] | Consumer: Starting Events
[2017-10-02 08:43:30,491: DEBUG/MainProcess] ^-- substep ok
[2017-10-02 08:43:30,491: DEBUG/MainProcess] | Consumer: Starting Heart
[2017-10-02 08:43:30,493: DEBUG/MainProcess] ^-- substep ok
[2017-10-02 08:43:30,493: DEBUG/MainProcess] | Consumer: Starting Mingle
[2017-10-02 08:43:30,493: INFO/MainProcess] mingle: searching for neighbors
[2017-10-02 08:43:31,505: INFO/MainProcess] mingle: all alone
[2017-10-02 08:43:31,505: DEBUG/MainProcess] ^-- substep ok
[2017-10-02 08:43:31,505: DEBUG/MainProcess] | Consumer: Starting Gossip
[2017-10-02 08:43:31,507: DEBUG/MainProcess] ^-- substep ok
[2017-10-02 08:43:31,507: DEBUG/MainProcess] | Consumer: Starting Tasks
[2017-10-02 08:43:31,509: DEBUG/MainProcess] ^-- substep ok
[2017-10-02 08:43:31,509: DEBUG/MainProcess] | Consumer: Starting Control
[2017-10-02 08:43:31,510: DEBUG/MainProcess] ^-- substep ok
[2017-10-02 08:43:31,511: DEBUG/MainProcess] | Consumer: Starting event loop
[2017-10-02 08:43:31,511: DEBUG/MainProcess] | Worker: Hub.register Pool...
[2017-10-02 08:43:31,511: INFO/MainProcess] vagrant@ubuntu ready.
[2017-10-02 08:43:31,511: DEBUG/MainProcess] basic.qos: prefetch_count->12


```

## "vagrant up" your vagrants if you havent

## In a new tab run  run_simulation_yaml.py

```

$ python run_simulation_yaml.py -f MITRE/Adversarial_Simulation/ontarget_recon.yml
YAML FILE: MITRE/Adversarial_Simulation/ontarget_recon.yml
OS matched windows...sending to the windows vagrant
Running: net user
Running: net user /domain
...

```

##  You should be able to view how things are going in the vagranttasks tab

```
[2017-10-02 13:54:54,282: INFO/MainProcess] Received task: workers.vagranttasks.runcmd_nodb_win[dad594b6-d12f-4f3c-a42e-a33051225b66]
[2017-10-02 13:54:54,284: DEBUG/MainProcess] TaskPool: Apply <function _fast_trace_task at 0x10b5da848> (args:('workers.vagranttasks.runcmd_nodb_win', 'dad594b6-d12f-4f3c-a42e-a33051225b66', {'origin': 'gen57319@XXXXXXXXXXXXXXX', 'lang': 'py', 'task': 'workers.vagranttasks.runcmd_nodb_win', 'group': None, 'root_id': 'dad594b6-d12f-4f3c-a42e-a33051225b66', u'delivery_info': {u'priority': 0, u'redelivered': None, u'routing_key': 'celery', u'exchange': u''}, 'expires': None, u'correlation_id': 'dad594b6-d12f-4f3c-a42e-a33051225b66', 'retries': 0, 'timelimit': [None, None], 'argsrepr': "('net user', 'On-target Recon Simulation', '017df153-470e-43d6-8e91-24c6b7cf62c4', None, 'windows-cb')", 'eta': None, 'parent_id': None, u'reply_to': '43579bfb-7243-3853-8858-2345326476dd', 'id': 'dad594b6-d12f-4f3c-a42e-a33051225b66', 'kwargsrepr': '{}'}, '[["net user", "On-target Recon Simulation", "017df153-470e-43d6-8e91-24c6b7cf62c4", null, "windows-cb"], {}, {"chord": null, "callbacks": null, "errbacks": null, "chain": null}]', 'application/json', 'utf-8') kwargs:{})
[2017-10-02 13:54:54,294: DEBUG/MainProcess] Task accepted: workers.vagranttasks.runcmd_nodb_win[dad594b6-d12f-4f3c-a42e-a33051225b66] pid:54830
[2017-10-02 13:54:54,296: WARNING/PoolWorker-3] changing locations
[2017-10-02 13:54:54,297: WARNING/PoolWorker-3] ##### DEBUG -- We made it to the vagrant function  -- DEBUG ######
[2017-10-02 13:54:54,297: WARNING/PoolWorker-3] 'Running: net user with Rule GUID: None against vagrant windows-cb

User accounts for \\

-------------------------------------------------------------------------------
Administrator            automation               DefaultAccount
defaultuser0             Guest                    
The command completed with one or more errors.

The following WinRM command responded with a non-zero exit status.
Vagrant assumes that this means the command failed!

```
