from ehrql import create_dataset
from ehrql.tables.national_sde import patients, artificial_hes_apc_2425

diagnosis_codes = ["I110", "I255", "I420", "I429", "I500", "I501", "I509"]
elective_admission_methods = ["11", "12", "13"]
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

dataset = create_dataset()
admissions = (
    artificial_hes_apc_2425.where(artificial_hes_apc_2425.fde == 1)
    .where(
        artificial_hes_apc_2425.admimeth.isin(
            elective_admission_methods + emergency_admission_methods
        )
    )
    .where(artificial_hes_apc_2425.diag_4_01.isin(diagnosis_codes))
)
dataset.define_population(admissions.exists_for_patient())

