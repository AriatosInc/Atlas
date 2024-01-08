import random

from core.agent import Agent
from utilities.config import read_config


class Patient(Agent):

    def __init__(self, environment, current_bubble, episode_duration, symptom_severity, functional_impairment,
                 treatment_failures, ):
        super().__init__(environment=environment, current_bubble=current_bubble)

        # Set up the decision-making choices
        self.event_slug_dict = {
            "intake": lambda: (random.choices(["ad", "ad_ap", "ap"], weights=[0.33, 0.33, 0.34])[0], 'movement'),
            "ad": lambda: ('esketamine', 'movement'),
            "ad_ap": lambda: ('esketamine', 'movement'),
            "ap": lambda: ('esketamine', 'movement'),
            "esketamine": lambda: ('ect', 'movement'),
            "ect": lambda: ('ad', 'movement'),
            "remission": lambda: ('stay', 'stay'),
            "relapse": lambda: ('intake', 'movement')
        }

        # DM_TRD Parameters
        trd_parameters = ["episode_duration", "symptom_severity", "functional_impairment", "treatment_failures"]
        self.episode_duration = episode_duration
        self.symptom_severity = symptom_severity

        if self.symptom_severity == "severe w/ psychosis":
            self.psychosis = True
            self.symptom_severity = "severe"
        else:
            self.psychosis = False

        self.functional_impairment = functional_impairment # not used, not tracked
        self.treatment_failures = treatment_failures # not used, not tracked

    def __str__(self):
        return f'{self.id} @ {self.current_bubble} | Episode: {self.episode_duration} Symptom Severity: {self.symptom_severity} w/ Psychosis: {self.psychosis}'

    def calculate_madrs_score(self):
        scoring_method = read_config("../../config/dm_trd_scoring.json")
        patient_score = 0

        # Manually coding this right now // todo: automate

        # Determine episode duration score
        if self.episode_duration == "acute":
            patient_score += scoring_method["episode_duration"]["acute"]
        elif self.episode_duration == "subacute":
            patient_score += scoring_method["episode_duration"]["subacute"]
        elif self.episode_duration == "chronic":
            patient_score += scoring_method["episode_duration"]["chronic"]
        else:
            raise ValueError(f"Invalid episode duration: {self.episode_duration}")

        # Determine symptom severity score
        if self.symptom_severity == "mild":
            patient_score += scoring_method["symptom_severity"]["mild"]
        elif self.symptom_severity == "moderate":
            patient_score += scoring_method["symptom_severity"]["moderate"]
        elif self.symptom_severity == "severe":
            if self.psychosis:
                patient_score += scoring_method["symptom_severity"]["severe_with_psychosis"]
            else:
                patient_score += scoring_method["symptom_severity"]["severe_without_psychosis"]
        else:
            raise ValueError(f"Invalid symptom severity: {self.symptom_severity}")

        # Determine score change from functional impairment
        if self.functional_impairment == "mild":
            patient_score += scoring_method["functional_impairment"]["mild"]
        elif self.functional_impairment == "moderate":
            patient_score += scoring_method["functional_impairment"]["moderate"]
        elif self.functional_impairment == "severe":
            patient_score += scoring_method["functional_impairment"]["severe"]

        # Determine score change from treatment failures
        if self.treatment_failures == "0":
            pass
        elif self.treatment_failures == "1-2":
            patient_score += scoring_method["treatment_failures"]["1-2"]
        elif self.treatment_failures == "3-4":
            patient_score += scoring_method["treatment_failures"]["3-4"]
        elif self.treatment_failures == "5-6":
            patient_score += scoring_method["treatment_failures"]["5-6"]

        print(patient_score)
        return patient_score
