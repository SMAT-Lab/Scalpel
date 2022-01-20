for path_repo in self._conf.get('path_to_repos'):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        jobs = {executor.submit(self.iter_commits, chunk): chunk for chunk in chunks}

        parallel_results = []
        for job in concurrent.futures.as_completed(jobs):
            # Read result from future
            result = job.result()
            # Append to the list of results
            parallel_results.append(result)

        for result in parallel_results:
            return result
