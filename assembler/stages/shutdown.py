# Copyright (c) 2018 by Raytheon BBN Technologies Corp.

from assembler.stages.core.ssh_stage import SSHStage

import subprocess, os

class ShutdownStage(SSHStage):
    ''' This stage will shutdown the vm, so you want it to depend on All SSH stages '''
    NAME = 'ShutdownStage'
    DEPENDS = ['KernelStage']

    def run(self):
        if not self._has_run:
            super(ShutdownStage, self).run()
            try:
                self._exec_cmd('sudo shutdown -h now')
            except subprocess.CalledProcessError as e:
                if e.returncode != 255: # is the system actually shuts down, 255 will be returned, which is expected
                    raise e
