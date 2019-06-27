'''
Created on 21 nov. 2018

@author: Vyacheslav.Sviridov
'''

import enmscripting


class MoENM(object):
    '''
    Use it to step-by-step commands execution i.e.
    when you need to lock object before change parameter
    and unlock after her
    '''

    def __init__(self, server=None, username=None, password=None):
        """ It requires the connection arguments.
        """
        self._session = enmscripting.open(server, username, password)
        self._terminal = self._session.terminal()

    def _run(self, cmd, *opts):
        """ This is the main method to be used in this handler to execute
        ENM CLI commands as "cmedit", "config", etc.
        """
        opt = " " + " ".join(opts) if len(opts) > 0 else ""
        out = self._terminal.execute(cmd + opt)
        output_str = '\n'.join(out.get_output())
        return output_str

    def get(self, fdn, param, *opts):
        """ Uses the command "cmedit get" to get an output.
        """
        cmd = "cmedit get %s -attr %s" % (fdn, param)
        out = self._run(cmd, *opts)
        return out

    def delete(self, fdn, *opts):
        """ Uses the command "cmedit delete" to delete an object.
        """
        cmd = "cmedit delete %s" % fdn
        out = self._run(cmd, *opts)
        return out

    def create(self, fdn, *opts, **kwargs):
        """ Uses the command "cmedit create" to create object with given values.
        """
        val = ";".join("%s=%s" % (k, v) for k, v in kwargs.items())
        cmd = "cmedit create %s %s" % (fdn, val)
        out = self._run(cmd, *opts)
        return out

    def set(self, fdn, *opts, **kwargs):
        """ Uses the command "cmedit set" to set attribute and values of an MO
        given a FDN and its attributes.
        """
        val = ";".join("%s:%s" % (k, v) for k, v in kwargs.items())
        cmd = "cmedit set %s %s" % (fdn, val)
        out = self._run(cmd, *opts)
        return out

    def action(self, fdn, act, *opts, **kwargs):
        """ Uses the command "cmedit action" to execute action of an MO
        given a FDN and its attributes.
        Ex.:
        action("MeContext=ERBS001,ManagedElement=1", "manualrestart",
        restartrank="RESTART_WARM", restartreason="PLANNED_RECONFIGURATION",
        restartinfo="someInfo")
        """
        val = ".(%s)" % (
            ",".join(
                "%s=%s" % (k, v) for k, v in kwargs.items())) if len(
                    kwargs) > 0 else ""
        cmd = "cmedit action %s %s%s" % (fdn, act, val)
        out = self._run(cmd, *opts)
        return out

    def __enter__(self):
        """ It instantiates object to be used inside the
        "with" statement.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ It tries to close the session after exiting the "with" statement.
        In case of failures, the proper exception is raised.
        """
        enmscripting.close(self._session)
        if exc_type:
            args = exc_val if isinstance(exc_val, tuple) else \
                 ((exc_val,) if isinstance(exc_val, str) else exc_val.args)
            raise(exc_type(*args), None, exc_tb)
