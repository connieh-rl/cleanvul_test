import pandas as pd

class CleanVulInstance():
    def __init__(
        self,
        instance_id: str,
        func_before: str,
        canonical_solution: str,
        language: str,
    ):
        self.instance_id =  instance_id,
        self.func_before = func_before,
        self.canonical_solution = canonical_solution,
        self.language = language
        return
    

class CleanVulBenchmark(PublicBenchmark):
    