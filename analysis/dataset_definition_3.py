import calendar
from datetime import date
from ehrql import create_dataset, get_parameter
from ehrql.tables.national_sde import (
    artificial_hes_apc_2425,
    artificial_hes_apc_2223,
)

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


def emergency_admissions(dataset):
    return dataset.where(dataset.fde == 1).where(
        dataset.disdate.is_on_or_between(period_start, period_end)
        & dataset.admimeth.is_in(emergency_admission_methods)
        & dataset.classpat.is_in(patient_classification_codes)
    )


emergency_admissions_2223 = emergency_admissions(artificial_hes_apc_2223)
emergency_admissions_2425 = emergency_admissions(artificial_hes_apc_2425)


def age_one_to_five_admissions(dataset):
    return dataset.where((dataset.startage_calc > 1) & (dataset.startage_calc <= 5))


def age_one_to_five_viral_wheeze_asthma_admissions(dataset):
    return age_one_to_five_admissions(dataset).where(
        dataset.diag_4_01.is_in(viral_infection_codes)
        & dataset.diag_4_02.is_in(wheeze_codes)
        & dataset.diag_4_03.is_in(asthma_codes)
    )


def age_one_to_five_asthma_admissions(dataset):
    return age_one_to_five_admissions(dataset).where(
        dataset.diag_4_01.is_in(asthma_codes)
        | (dataset.diag_4_01.is_in(wheeze_codes) & dataset.diag_4_02.is_in(asthma_codes))
    )


def age_six_to_sixteen_asthma_admissions(dataset):
    return dataset.where((dataset.startage_calc > 5) & (dataset.startage_calc <= 16)).where(
        dataset.diag_4_01.is_in(asthma_codes)
    )


age_one_to_five_asthma_admissions_2223 = age_one_to_five_asthma_admissions(
    emergency_admissions_2223
)
age_one_to_five_viral_wheeze_asthma_admissions_2223 = (
    age_one_to_five_viral_wheeze_asthma_admissions(emergency_admissions_2223)
)
age_six_to_sixteen_asthma_admissions_2223 = age_six_to_sixteen_asthma_admissions(
    emergency_admissions_2223
)
age_one_to_five_asthma_admissions_2425 = age_one_to_five_asthma_admissions(
    emergency_admissions_2425
)
age_one_to_five_viral_wheeze_asthma_admissions_2425 = (
    age_one_to_five_viral_wheeze_asthma_admissions(emergency_admissions_2425)
)
age_six_to_sixteen_asthma_admissions_2425 = age_six_to_sixteen_asthma_admissions(
    emergency_admissions_2425
)


dataset.define_population(
    age_one_to_five_asthma_admissions_2223.exists_for_patient()
    | age_one_to_five_viral_wheeze_asthma_admissions_2223.exists_for_patient()
    | age_six_to_sixteen_asthma_admissions_2223.exists_for_patient()
    | age_one_to_five_asthma_admissions_2425.exists_for_patient()
    | age_one_to_five_viral_wheeze_asthma_admissions_2425.exists_for_patient()
    | age_six_to_sixteen_asthma_admissions_2425.exists_for_patient()
)

dataset.add_event_table(
    "age_one_to_five_asthma_admissions_2223",
    provider_code=age_one_to_five_asthma_admissions_2223.procodet,
    hospital_code=age_one_to_five_asthma_admissions_2223.sitetret,
)
dataset.add_event_table(
    "age_one_to_five_viral_wheeze_asthma_admissions_2223",
    provider_code=age_one_to_five_viral_wheeze_asthma_admissions_2223.procodet,
    hospital_code=age_one_to_five_viral_wheeze_asthma_admissions_2223.sitetret,
)
dataset.add_event_table(
    "age_six_to_sixteen_asthma_admissions_2223",
    provider_code=age_six_to_sixteen_asthma_admissions_2223.procodet,
    hospital_code=age_six_to_sixteen_asthma_admissions_2223.sitetret,
)
dataset.add_event_table(
    "age_one_to_five_asthma_admissions_2425",
    provider_code=age_one_to_five_asthma_admissions_2425.procodet,
    hospital_code=age_one_to_five_asthma_admissions_2425.sitetret,
)
dataset.add_event_table(
    "age_one_to_five_viral_wheeze_asthma_admissions_2425",
    provider_code=age_one_to_five_viral_wheeze_asthma_admissions_2425.procodet,
    hospital_code=age_one_to_five_viral_wheeze_asthma_admissions_2425.sitetret,
)
dataset.add_event_table(
    "age_six_to_sixteen_asthma_admissions_2425",
    provider_code=age_six_to_sixteen_asthma_admissions_2425.procodet,
    hospital_code=age_six_to_sixteen_asthma_admissions_2425.sitetret,
)
