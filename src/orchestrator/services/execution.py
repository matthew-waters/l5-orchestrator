class ExecutionService:
    def launch_and_submit(self, run):
        raise NotImplementedError

    def poll_and_finalize(self, run):
        raise NotImplementedError
