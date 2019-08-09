"""

Deleting ENM configurations one by one

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
        print output
        return output


def get_job_status(term, job):
    cmd = "config delete --status --job %s" % job
    while True:
        output = get_output(term, cmd)
        if "COMPLETED" in output[2].split("\t"):
            break
        else:
            time.sleep(60)


def main():
    try:
        session = enmscripting.open()
        terminal = session.terminal()
        for cfg_name in read_file("cfgs.txt"):
            cmd = "config delete %s" % cfg_name
            output = get_output(terminal, cmd)
            jobid = output[-1].split()[-1]
            get_job_status(terminal, jobid)
            cfg_str = "Config %s has been deleted!" % cfg_name
            print "%s%s%s%s%s" % ("\x1B[", "31;40m", cfg_str, "\x1B[", "0m")
    except Exception as e:
        print e
    finally:
        if session is not None:
            enmscripting.close(session)


if __name__ == "__main__":
    main()
