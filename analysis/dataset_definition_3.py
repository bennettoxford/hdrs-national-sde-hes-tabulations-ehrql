import calendar
from datetime import date
from ehrql import create_dataset, get_parameter
from ehrql.tables.databricks import hospital_admissions

asthma_codes = ["J450", "J451", "J458", "J459", "J46X"]
wheeze_codes = ["R062"]
viral_infection_codes = ["B349"]
emergency_admission_methods = [
    "21",
    "22",
    "23",
    "24",
    "25",
    "28",
    "2A",
    "2B",
    "2C",
    "2D",
]
patient_classification_codes = ["1", "2", "5"]

period_start = get_parameter("period_start", type=str, default="2022-04-01")
period_start = date.fromisoformat(period_start)
end_month = 3 if period_start.year in [2022, 2023] else 9
end_year = period_start.year + 1
period_end = date(end_year, end_month, calendar.monthrange(end_year, end_month)[1])

dataset = create_dataset()


emergency_admissions = hospital_admissions.where(hospital_admissions.fde == 1).where(
    hospital_admissions.disdate.is_on_or_between(period_start, period_end)
    & hospital_admissions.admimeth.is_in(emergency_admission_methods)
    & hospital_admissions.classpat.is_in(patient_classification_codes)
)


age_one_to_five_admissions = hospital_admissions.where(
    (hospital_admissions.startage_calc > 1) & (hospital_admissions.startage_calc <= 5)
)


age_one_to_five_viral_wheeze_asthma_admissions = age_one_to_five_admissions.where(
    age_one_to_five_admissions.diag_4_01.is_in(viral_infection_codes)
    & age_one_to_five_admissions.diag_4_02.is_in(wheeze_codes)
    & age_one_to_five_admissions.diag_4_03.is_in(asthma_codes)
)


age_one_to_five_asthma_admissions = age_one_to_five_admissions.where(
    age_one_to_five_admissions.diag_4_01.is_in(asthma_codes)
    | (
        age_one_to_five_admissions.diag_4_01.is_in(wheeze_codes)
        & age_one_to_five_admissions.diag_4_02.is_in(asthma_codes)
    )
)

age_six_to_sixteen_asthma_admissions = hospital_admissions.where(
    (hospital_admissions.startage_calc > 5) & (hospital_admissions.startage_calc <= 16)
).where(hospital_admissions.diag_4_01.is_in(asthma_codes))


dataset.define_population(
    age_one_to_five_asthma_admissions.exists_for_patient()
    | age_one_to_five_viral_wheeze_asthma_admissions.exists_for_patient()
    | age_six_to_sixteen_asthma_admissions.exists_for_patient()
)

dataset.add_event_table(
    "age_one_to_five_asthma_admissions",
    provider_code=age_one_to_five_asthma_admissions.procodet,
    hospital_code=age_one_to_five_asthma_admissions.sitetret,
)
dataset.add_event_table(
    "age_one_to_five_viral_wheeze_asthma_admissions",
    provider_code=age_one_to_five_viral_wheeze_asthma_admissions.procodet,
    hospital_code=age_one_to_five_viral_wheeze_asthma_admissions.sitetret,
)
dataset.add_event_table(
    "age_six_to_sixteen_asthma_admissions",
    provider_code=age_six_to_sixteen_asthma_admissions.procodet,
    hospital_code=age_six_to_sixteen_asthma_admissions.sitetret,
)
