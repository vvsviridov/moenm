'''
Created on 21 nov. 2018

@author: Vyacheslav.Sviridov
'''

import enmscripting


class MoENM(object):
    """
    Use it to step-by-step commands execution i.e.
    when you need to lock object before change parameter
    and unlock after

    Arguments:
        object {[type]} -- I don't know what it means

    Returns:
        [type] -- It isn't return anything
    """
    def __init__(self, server=None, username=None, password=None):
        """
        It requires the connection arguments.

        Keyword Arguments:
            server {[str]} -- server url name (default: {None})
            username {[str]} -- username (default: {None})
            password {[str]} -- password (default: {None})
        """
        self._session = enmscripting.open(server, username, password)
        self._terminal = self._session.terminal()

    def _run(self, cmd, *opts):
        """
        This is the main method to be used in this handler to execute
        ENM CLI commands as "cmedit", "config", etc.

        Arguments:
            cmd {[str]} -- cmedit CLI formatted command
            *opts {[str]} -- cmedit CLI options

        Returns:
            [str] -- cmedit command output as string
        """
        opt = " " + " ".join(opts) if len(opts) > 0 else ""
        out = self._terminal.execute(cmd + opt)
        output_str = '\n'.join(out.get_output())
        return output_str

    def get(self, fdn, param, *opts):
        """
        Uses the command "cmedit get" to get an output.

        Arguments:
            fdn {[type]} -- [description]
            param {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        cmd = "cmedit get %s -attr %s" % (fdn, param)
        out = self._run(cmd, *opts)
        return out

    def delete(self, fdn, *opts):
        """
        Uses the command "cmedit delete" to delete an object.

        Arguments:
            fdn {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        cmd = "cmedit delete %s" % fdn
        out = self._run(cmd, *opts)
        return out

    def create(self, fdn, *opts, **kwargs):
        """
        Uses the command "cmedit create" to create object with given values.

        Arguments:
            fdn {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        val = ";".join("%s=%s" % (k, v) for k, v in kwargs.items())
        cmd = "cmedit create %s %s" % (fdn, val)
        out = self._run(cmd, *opts)
        return out

    def set(self, fdn, *opts, **kwargs):
        """
        Uses the command "cmedit set" to set attribute and values of an MO
        given a FDN and its attributes.

        Arguments:
            fdn {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        val = ";".join("%s:%s" % (k, v) for k, v in kwargs.items())
        cmd = "cmedit set %s %s" % (fdn, val)
        out = self._run(cmd, *opts)
        return out

    def action(self, fdn, act, *opts, **kwargs):
        """
        Uses the command "cmedit action" to execute action of an MO
        given a FDN and its attributes.
        Ex.:
        action(
            "MeContext=ERBS001,ManagedElement=1",
            "manualrestart",
            restartrank="RESTART_WARM",
            restartreason="PLANNED_RECONFIGURATION",
            restartinfo="someInfo"
            )

        Arguments:
            fdn {[type]} -- [description]
            act {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        val = ".(%s)" % (
            ",".join("%s=%s" % (k, v) for k, v in kwargs.items())
            ) if len(kwargs) > 0 else ""
        cmd = "cmedit action %s %s%s" % (fdn, act, val)
        out = self._run(cmd, *opts)
        return out

    def __enter__(self):
        """
        It instantiates object to be used inside the
        "with" statement.

        Returns:
           [type] -- [description]
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        It tries to close the session after exiting the "with" statement.
        In case of failures, the proper exception is raised.

        Arguments:
            exc_type {[type]} -- [description]
            exc_val {[type]} -- [description]
            exc_tb {[type]} -- [description]
        """
        enmscripting.close(self._session)
        if exc_type:
            args = exc_val if isinstance(exc_val, tuple) else \
                 ((exc_val,) if isinstance(exc_val, str) else exc_val.args)
            raise(exc_type(*args), None, exc_tb)
