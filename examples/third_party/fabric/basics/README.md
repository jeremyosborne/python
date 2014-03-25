Using Fabric for SSH
====================
Fabric is a library and command-line tool for streamlining the use of SSH for application deployment or systems administration tasks.

It provides a basic suite of operations for executing local or remote shell commands (normally or via sudo) and uploading/downloading files, as well as auxiliary functionality such as prompting the running user for input, or aborting execution.

* [fab homepage](http://fabfile.org/)



Requirements
------------
Make sure that fabric is installed. Likely these examples will work with future versions of fabric, but for accuracy, the examples assume the following setup:

    pip install fabric==1.6.1
    # test with
    fab --version



Working with Remote Hosts
-------------------------
These examples assume that you will be using fabric for what it was designed for: working with remote systems. The class examples assume a particular, but easy to replicate setup on an Amazon EC2 instance. This setup should have been done prior to your class.

**You will need to get the hostname of the remote system(s), and you will need to substitute the hostname into the example commands and code.**



SSH Key Setup
-------------
Prior to the class, a set of SSH key files should have been generated for you. These will allow passwordless entry during our scripts, and will help mimic more real life type scenarios.

***(Please note: from here on out the commands are placeholders, and you will likely have to change each and everyone of them to match specifics to your users.)***

Please login to the test host: 

    ssh student1@ec2-54-227-155-203.comfpute-1.amazonaws.com
    (password should be `letmein` without the quotes)

Check that you have a key made for you:

    ls .ssh

Confirm that there is a `student` keyfile there. This is your private key, and your "identity" for the remainder of these examples. Leave the remote login:

    exit

and grab the file, using a secure copy. The command should resemble something like:

    # Assuming scp command is run from your local box,
    # copy the key locally:
    scp student1@ec2-54-227-155-203.compute-1.amazonaws.com:.ssh/student .

Let's test and make sure we can get passwordless entry to our test host. Assuming the student key is kept locally, try:

    ssh -i student student1@ec2-54-227-155-203.compute-1.amazonaws.com

And you should be able to login without having to enter your password. Yay! Exit out of the system, we're good to go. Remember where you put the student file, you'll need it.



### Note about key files
It's a good practice to not leave keyfiles strewn around your system, and in easy to access places. That said, for the convenience of our lab, please keep the keyfile someplace that is easy for you, and for python, to reference. 

The examples will assume that the keyfile is always in the current working directory.
   


`fab` command basic usage
-------------------------
Fabric provides a command line utility `fab`, which (by default) reads configuration and tasks from a file named `fabfile.py` from the directory it is run.  A typical fabfile contains one or more functions to be executed on a group of remote hosts.

Basic usage of the `fab` command looks like:

    fab --fabfile=path_to_file.py -i student [--hosts=user@host[,hosts...]] command

The `examples/fabfile_0.py` provides commands to check free `diskspace` and `host_type`, as well as defining a group of hosts on which to run. Let's run these examples:

    fab --fabfile=examples/fabfile_0.py -i student --hosts=student1@ec2-75-101-223-215.compute-1.amazonaws.com diskspace

Let's run the `host_type` command:

    fab --fabfile=examples/fabfile_0.py -i student --hosts=student1@ec2-75-101-223-215.compute-1.amazonaws.com diskspace
    
Let's run both:

    fab --fabfile=examples/fabfile_0.py -i student --hosts=student1@ec2-75-101-223-215.compute-1.amazonaws.com diskspace host_type

Open `examples/fabfile_0.py` and take a look at the contents. Relatively simple and straightforward.



Basic configuration of fabfiles
-------------------------------
Commandline options are great, but what if you want to run the same script over and over with the same hosts? Fabric has the concept of an environment represented in, you'll never guess, the `env` object.

Open `examples/fabfile_1.py` and change the `env` object settings to our needs. After changing the file, test things out:

    fab --fabfile=examples/fabfile_1.py host_type diskspace

Excellent!

Fabric is Python code. The `env` object acts as a Python object. Open `examples/fabfile_2.py` and take a look at `examples/fabenv.py`. We could organize an environment in an extra file and keep our configuration elsewhere:

    fab --fabfile=examples/fabfile_2.py host_type diskspace

But probably better is to just use a simple `fabricrc` style of file and keep the configuration out of fabric. We can reuse `examples/fabfile_0.py` to demonstrate this:

    fab --fabfile=examples/fabfile_0.py --config=examples/fabricrc host_type diskspace



Task arguments
--------------
It's often useful to pass runtime parameters into your tasks, just as you might during regular Python programming. Fabric has basic support for this using a shell-compatible notation: 

    <task name>:<arg>,<kwarg>=<value>,... 
    
It's contrived, but let's use `examples/fabfile_3.py` as a sample test:

    fab --fabfile=examples/fabfile_3.py hello:name=Me arg_type:name=Me

And of course we can pass a positional argument, too:

    fab --fabfile=examples/fabfile_3.py hello:Me  rg_type:Me

Let's test the input type (I bet you can guess the output):

    fab --fabfile=examples/fabfile_3.py hello:42 arg_type:42

What happens if we encounter an error by passing in an incorrect number of arguments?

    fab --fabfile=examples/fabfile_3.py hello:42,24 arg_type:42

Fabric takes a fail fast approach in general. Passing incorrect arguments, this will cause our task to die.

* see [Fabric Task Arguments](http://docs.fabfile.org/en/1.6/usage/fab.html#per-task-arguments)



Lab - executing commands, handling errors
-----------------------------------------
Build out the `labs/execute.py` fabfile so that it:

* Has a task named `execute` that takes any number of positional and keyword arguments.
* `execute` imports `examples_fabfile_3.py` and passes the arguments to the `hello` and `arg_type` tasks.
* `execute` runs each task: `hello` and `arg_type` no matter what, even if one of them errors.
* If either of these functions throw an error, `execute` prints out the statement `You haz error`.

You should be able to run both of the following commands. 

`execute` will produce "good" results:

    fab --fabfile=labs/execute.py execute:42

`execute` will handle (slightly more gracefully) the errors produced in `hello` and `arg_type`:

    fab --fabfile=labs/execute.py execute:42,24



Handling output in Python
-------------------------
All programming languages can be useful. The main point of fabric is to utilize the strengths of the shell and the strengths of Python at the same time.

`examples/fabfile_4.py` begins the real adventure with fabric:

    fab --fabfile=examples/fabfile_4.py ls

Take a look at the output and the code before jumping into the next lab.



Lab - ls for directories
------------------------
Build out the `labs/ls.py` fabfile so that it:

* Has a task named `ls_num_dirs` that takes a single argument from the commandline.
* Returns a count of the number of directories -- hidden and visible -- at whatever path is passed in.
* Uses "." as the default argument.
* Does not display stdout from the `run` command.

Test commands (all of the following should work without error, although they may give different results):

    fab --config=examples/fabricrc --fabfile=labs/ls.py ls_num_dirs:/
    fab --config=examples/fabricrc --fabfile=labs/ls.py ls_num_dirs:.
    fab --config=examples/fabricrc --fabfile=labs/ls.py ls_num_dirs

* see [Fabric run docs for help](http://docs.fabfile.org/en/1.6/api/core/operations.html#fabric.operations.run)



Batch processing and using fabric as a library
----------------------------------------------
We can run the same task in parallel across multiple hosts if we wish.

Before running the following example, please open `examples/fabfile_5.py` and change the `env` settings. Then open `examples/ssh_config` and replace the `HostName` placeholders. After reviewing the code, run as a regular python command:

    python examples/fabfile_5.py



Lab -- Average Uptime
---------------------
Consider the case where we want to collect average uptime from a group of hosts. Using `examples/fabfile_5.py` as a basis, work with `labs/uptime.py` to get you a script that will return an average uptime across the (contrived) hosts. The command that you should be able to use to invoke the script is:

    python labs/uptime.py

Things todo:

* see [Ways to get uptime](http://en.wikipedia.org/wiki/Uptime)
* Use the `ssh_config` file we just created.
* Run the commands in tasks in parallel.
