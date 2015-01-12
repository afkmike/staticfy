__author__ = 'mark@afkconcepts.com'
import traceback
import log_manager
import string
from os import walk
import os.path


log = log_manager.log_manager("logs/file_io_log.txt")


def build_traceback(error_trace):
    """
    Strips newline chars, and creates a single string with an entire traceback.
    Used for the logging system.
    :param error_trace: The traceback error
    :return: A string of the entire traceback, with newlines stripped
    """
    s = string.split(error_trace, "\n")
    ns = ""
    for i in range(len(s)):
        t = string.rstrip(s[i])
        ns += t + " "
    return ns


def get_contents(filename, lines=False, full_dir=True):
    """
    Reads the contents of filename and returns either an array (lines=True) of (lines),
    or returns a string (lines=False). (full_dir) is used in later functions.
    :param filename: Name/Directory of the file to be read and returned
    :param lines: Read the file with readlines()
    :param full_dir: Passed on to other functions, does nothing here.
    :return: The (contents) of (filename).
    """
    print "\n"+filename+"\n"
    filename = string.lstrip(filename, "u'")
    filename = string.rstrip(filename, "'")
    log.log.info("Getting %s now..." % filename)
    print "\n"+filename+"\n"
    try:
        if not lines:
            f = open(filename, 'r')
            contents = f.read()
            log.log.info("    ...making backup...")
            make_backup(contents, filename, lines=lines, full_dir=full_dir)  # Make a pristine backup.
            log.log.info("    ...done.")
            return contents
        else:
            f = open(filename, 'r')
            contents = f.readlines()
            log.log.info("    ...making backup...")
            make_backup(contents, filename, lines=lines, full_dir=full_dir)
            log.log.info("    ...done.")
            return contents

    except IOError as e:
        log.log.error("[IO ERROR] %s %s" % (e.errno, e.strerror))
        log.log.error("[TRACEBACK] %s" % build_traceback(traceback.format_exc()))
        filename = input('Please enter a valid file, "skip" to skip this file or "quit" to exit!')  # prompt for file

        if filename == 'quit':
            exit()  # hard exit
        elif filename == 'skip':
            return None
        else:
            return get_contents(filename, full_dir)


def make_backup(contents, filename, lines=False, full_dir=True):
    """
    Makes a back up of (contents), with the name (copyOf(filename))
    If the directory is full, strip out everything but the (filename) for (copy_filename)
    :param contents: Contents to back up, can be a string or array
    :param filename: The file name to back up, can be full dir, or relative
    :param lines: If the content file is from readlines()
    :param full_dir: If the filename has a full dir, or is relative
    :return: Nothing.
    """
    # to get just the name from a full directory name
    if full_dir:
        f = string.split(filename, '\\')
        copy_filename = "copyOf" + f[len(f)-1]
    else:
        copy_filename = "copyOf" + filename
    if make_new_file(contents, copy_filename, backup=True, lines=lines, full_dir=full_dir):
        log.log.info("Made backup copy of " + filename + " named " + copy_filename)
    else:
        log.log.error("Backup of " + filename + " has failed.")



def make_new_file(contents, filename, backup=False, lines=False, full_dir=False):
    """
    Writes (contents) to (filename). If its a (backup=True) and fails, will wait for user input before continuing

    :param contents: The contents to be written to file, can be in readlines() format
    :param filename: The name of the file to write to, can be full dir or relative
    :param backup: Is this a backup file write?
    :param lines: If the format of content is readlines()
    :param full_dir: Does nothing at the moment.
    :return True if successful:
    """
    try:
        if not lines:
            f = open(filename, 'w')  # create/open the file in write mode
            f.write(contents)        # write/overwrite it
            f.close()                # save it
            log.log.info("File saved: " + filename)
        else:
            f = open(filename, 'w')
            for line in contents:
                f.write(line)
            f.close()
            log.log.info("File saved: " + filename)
        return True

    except IOError as e:
        log.log.error("[IO ERROR] %s %s" % (e.errno, e.strerror))
        log.log.error("[TRACEBACK] %s" % build_traceback(traceback.format_exc()))
        if backup:
            input('Back up failed, please manually back up and press any key to continue.')
        else:
            input('Writing to file ' + filename + 'failed, press any key to continue.')
            log.log.error('Writing to file ' + filename + ' failed.')
        return False


def file_or_dir(path, ext=None):
    """
    :param path: user entered path
    :return: (list)filename provided as path OR all files in dir provided as path
    """
    f = []
    if os.path.isdir(path):
        for (dirpath, dirnames, filenames) in walk(path):  # dirpath == path, dirnames = folders inside path
            f.extend(filenames)
            print "file found in folder: ".join(map(str, filenames))  # this could be changed to a log entry
            break  # <-- ???????????????
    elif os.path.isfile(path):
        f.append(path)
        print "single file path: ".join(map(str, path))  # this could be changed to a log entry
    else:
        # TODO show 'you didn't enter a file to modify, moron' dialog and kill the process
        # this is actually a secondary check, it should already be done once in gui.py
        pass
    return f