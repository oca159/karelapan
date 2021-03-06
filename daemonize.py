# -*- coding:utf-8 -*-
import fcntl
import os
import sys
import time
from karelapan.settings import LOCKFILE
from signal import SIGTERM

def start(fun_to_start, debug=False):
    try:
        pf = file(LOCKFILE,'r')
        pid = int(pf.read().strip())
        pf.close()
    except IOError:
        pid = None

    if pid:
        message = "pidfile %s already exist. Daemon already running?\n"
        sys.stderr.write(message % LOCKFILE)
        sys.exit(1)
    logger = None
    std_pipes_to_logger = True
    # Used docs by Levent Karakas
    # http://www.enderunix.org/documents/eng/daemon.php
    # as a reference for this section.

    # Fork, creating a new process for the child.
    process_id = os.fork()
    if process_id < 0:
        # Fork error.  Exit badly.
        sys.exit(1)
    elif process_id != 0:
        # This is the parent process.  Exit.
        sys.exit(0)
    # This is the child process.  Continue.

    # Stop listening for signals that the parent process receives.
    # This is done by getting a new process id.
    # setpgrp() is an alternative to setsid().
    # setsid puts the process in a new parent group and detaches its
    # controlling terminal.
    process_id = os.setsid()
    if process_id == -1:
        # Uh oh, there was a problem.
        sys.exit(1)

    # Close file descriptors
    devnull = '/dev/null'
    if hasattr(os, "devnull"):
        # Python has set os.devnull on this system, use it instead
        # as it might be different than /dev/null.
        devnull = os.devnull
    null_descriptor = open(devnull, 'rw')
    if not debug:
        for descriptor in (sys.stdin, sys.stdout, sys.stderr):
            descriptor.close()
            descriptor = null_descriptor

    # Set umask to default to safe file permissions when running
    # as a root daemon. 027 is an octal number.
    os.umask(027)

    # Change to a known directory.  If this isn't done, starting
    # a daemon in a subdirectory that needs to be deleted results
    # in "directory busy" errors.
    # On some systems, running with chdir("/") is not allowed,
    # so this should be settable by the user of this library.
    os.chdir('/')

    # Create a lockfile so that only one instance of this daemon
    # is running at any time.  Again, this should be user settable.
    lockfile = open(LOCKFILE, 'w')
    # Try to get an exclusive lock on the file.  This will fail
    # if another process has the file locked.
    fcntl.lockf(lockfile, fcntl.LOCK_EX|fcntl.LOCK_NB)

    # Record the process id to the lockfile.  This is standard
    # practice for daemons.
    lockfile.write('%s' %(os.getpid()))
    lockfile.flush()

    # Logging.  Current thoughts are:
    # 1. Attempt to use the Python logger (this won't work Python < 2.3)
    # 2. Offer the ability to log to syslog
    # 3. If logging fails, log stdout & stderr to a file
    # 4. If logging to file fails, log stdout & stderr to stdout.

    fun_to_start()

def stop():
    """
    Stop the daemon
    """
    # Get the pid from the pidfile
    try:
        pf = file(LOCKFILE,'r')
        pid = int(pf.read().strip())
        pf.close()
    except IOError:
        pid = None

    if not pid:
        message = "pidfile %s does not exist. Daemon not running?\n"
        sys.stderr.write(message % LOCKFILE)
        return # not an error in a restart

    # Try killing the daemon process
    try:
        while 1:
            os.kill(pid, SIGTERM)
            time.sleep(0.1)
    except OSError, err:
        err = str(err)
        if err.find("No such process") > 0:
            if os.path.exists(LOCKFILE):
                os.remove(LOCKFILE)
        else:
            print str(err)
            sys.exit(1)

def wasap():
    try:
        pf = file(LOCKFILE, 'r')
        pid = int(pf.read().strip())
        pf.close()
    except IOError:
        pid = None

    if not pid:
        print "Kareld no está corriendo"
    else:
        print "Kareld está corriendo con PID %d"%pid
