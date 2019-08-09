"""

Batch executing async commands one by one
from file. Next command starts after previous
command's job's takes "COMPLETED" status

"""
import enmscripting
import time


def read_file(fname):
    try:
        with open(fname, "r") as f:
            lines = f.readlines()
    except IOError as e:
        print "Problem with file: ", e
    except Exception as e:
        print e
    else:
        return lines


def get_output(term, cmd):
    result = term.execute(cmd)
    if result.is_command_result_available():
        output = result.get_output()
        for out_str in output:
            print out_str
        return output


def wait_for_completed_status(term, job, cm_pref):
    cmd = "%s --status --job %s" % (cm_pref, job)
    while True:
        output = get_output(term, cmd)
        if "COMPLETED" in output[2].split("\t") \
                or "Error" in output[1].split():
            break
        else:
            time.sleep(60)


def print_red(str_to_print):
    print "%s%s%s%s%s" % ("\x1B[", "31;40m", str_to_print, "\x1B[", "0m")


def main():
    try:
        session = enmscripting.open()
        terminal = session.terminal()
        for full_cmd in read_file("cfgs.txt"):
            cmd_prefix = " ".join(full_cmd.split()[0:2])
            output = get_output(terminal, full_cmd)
            if "Error" not in " ".join(output).split():
                jobid = output[-1].split()[-1]
                wait_for_completed_status(terminal, jobid, cmd_prefix)
                cfg_str = "Command <%s> has been executed!" % full_cmd
                print_red(cfg_str)
    except Exception as e:
        print e
    finally:
        if session is not None:
            enmscripting.close(session)


if __name__ == "__main__":
    main()
