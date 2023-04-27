from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Box:
    items_per_box: int
    len: float
    wid: float
    dep: float

    def volume(self) -> float:
        return self.len * self.wid * self.dep


@dataclass(frozen=True)
class Item:
    name: str
    single_price: float
    box: Box
    accessories: List[Tuple["Item", int]] = field(default_factory=list)

    def total_price(self) -> float:
        subprices = [
            accessory.total_price() * amount_needed
            for accessory, amount_needed in self.accessories
        ]
        all_prices = subprices + [self.single_price]
        return sum(all_prices)


@dataclass(frozen=True)
class Pandemic:
    name: str
    duration_in_weeks: float
    infected_per_population: float
    seek_healthcare_per_infected: float
    hospitalised_per_seek_healthcare: float
    icu_case_per_hospitalised: float
    ventilated_per_icu_case: float
    fatality: float
    average_days_in_hospital_not_icu: float
    average_days_in_hospital_icu: float

    def infected_total(self, population: int) -> float:
        return self.infected_per_population * population

    def seek_healthcare_total(self, population: int) -> float:
        return self.seek_healthcare_per_infected * self.infected_total(population)

    def hospitalised_total(self, population: int) -> float:
        return self.hospitalised_per_seek_healthcare * self.seek_healthcare_total(
            population
        )

    def icu_cases_total(self, population: int) -> float:
        return self.icu_case_per_hospitalised * self.hospitalised_total(population)

    def ventilated_total(self, population: int) -> float:
        return self.ventilated_per_icu_case * self.icu_cases_total(population)

    def deaths(self, population: int) -> float:
        return self.fatality * self.infected_total(population)

    def outpatient_visits(self, population: int) -> float:
        return self.seek_healthcare_total(population) - self.hospitalised_total(
            population
        )

    def non_icu_patient_days(self, population: int) -> float:
        return (
            self.hospitalised_total(population) * self.average_days_in_hospital_not_icu
        )

    def non_mv_icu_patient_days(self, population: int) -> float:
        return (
            self.icu_cases_total(population)
            * (1 - self.ventilated_per_icu_case)
            * self.average_days_in_hospital_icu
        )

    def mv_icu_patient_days(self, population: int) -> float:
        return self.ventilated_total(population) * self.average_days_in_hospital_icu

    def dictionary_of_contacts(
        self, professions: List["Profession"], population: int
    ) -> Dict[str, int]:
        return {
            item.name: item.total_contacts(self, population) for item in professions
        }


@dataclass
class Profession:
    name: str
    contacts_per_hospitalised: int = 0
    """0 for Other HCW, only input for Escort"""
    contacts_per_outpatient_visit: int = 0
    """0 for resp tech, radio tech, housekeepers"""
    contacts_per_non_icu_patient_day: int = 0
    """0 for administrative, only input for phlebotomists"""
    contacts_per_icu_patient_day: int = 0
    """0 for administrative"""
    contacts_per_mv_day: int = 0
    """0 for administrative"""
    contacts_per_week: float = 80.0
    """assuming 40 work hours and 2 contacts per hour"""
    attrition_rate: float = 0.4

    def total_contacts(self, pandemic: Pandemic, population: int) -> int:
        return (
            pandemic.hospitalised_total(population) * self.contacts_per_hospitalised
            + pandemic.outpatient_visits(population)
            * self.contacts_per_outpatient_visit
            + pandemic.non_icu_patient_days(population)
            * self.contacts_per_non_icu_patient_day
            + pandemic.non_mv_icu_patient_days(population)
            * self.contacts_per_icu_patient_day
            + pandemic.mv_icu_patient_days(population) * self.contacts_per_mv_day
        )

    def number_of_profession_involved_in_pandemic(
        self, pandemic: Pandemic, population: int
    ) -> float:
        return self.total_contacts(pandemic, population) / (
            self.contacts_per_week
            * pandemic.duration_in_weeks
            * (1 - self.attrition_rate)
        )


@dataclass
class Strategy:
    name: str
    n95_amount: int
    elastomeric_amount: int
    papr_amount: int

    def acquisition_cost_of_respirators(
        self, pandemic: Pandemic, population: int
    ) -> float:
        return


if __name__ == "__main__":
    influenza1918 = Pandemic(
        name="Influenza 1918",
        duration_in_weeks=12.0,
        infected_per_population=0.3,
        seek_healthcare_per_infected=0.5,
        hospitalised_per_seek_healthcare=0.22,
        icu_case_per_hospitalised=0.15,
        ventilated_per_icu_case=0.5,
        fatality=0.021,
        average_days_in_hospital_not_icu=5,
        average_days_in_hospital_icu=10,
    )

    md = Profession(
        name="MD",
        contacts_per_hospitalised=3,
        contacts_per_outpatient_visit=1,
        contacts_per_non_icu_patient_day=2,
        contacts_per_icu_patient_day=4,
        contacts_per_mv_day=4,
    )

    rn = Profession(
        name="RN",
        contacts_per_hospitalised=5,
        contacts_per_outpatient_visit=2,
        contacts_per_non_icu_patient_day=6,
        contacts_per_icu_patient_day=24,
        contacts_per_mv_day=24,
    )

    resp_tech = Profession(
        name="Respiratory tech",
        contacts_per_hospitalised=3,
        contacts_per_outpatient_visit=0,
        contacts_per_non_icu_patient_day=6,
        contacts_per_icu_patient_day=12,
        contacts_per_mv_day=6,
    )

    radiology_tech = Profession(
        name="Radiology tech",
        contacts_per_hospitalised=1,
        contacts_per_outpatient_visit=0,
        contacts_per_non_icu_patient_day=1,
        contacts_per_icu_patient_day=2,
        contacts_per_mv_day=2,
    )
    phlebotomists = Profession(name="Phlebotomists", contacts_per_non_icu_patient_day=1)

    housekeepers = Profession(
        name="Housekeepers",
        contacts_per_hospitalised=1,
        contacts_per_outpatient_visit=0,
        contacts_per_non_icu_patient_day=1,
        contacts_per_icu_patient_day=1,
        contacts_per_mv_day=1,
    )

    other_hcw = Profession(
        name="Other HCW",
        contacts_per_hospitalised=0,
        contacts_per_outpatient_visit=1,
        contacts_per_non_icu_patient_day=1,
        contacts_per_icu_patient_day=1,
        contacts_per_mv_day=1,
    )
    administrative = Profession(
        name="Administrative",
        contacts_per_hospitalised=2,
        contacts_per_outpatient_visit=1,
    )

    escort = Profession(name="Escort", contacts_per_hospitalised=1)

    professions = [
        md,
        rn,
        resp_tech,
        radiology_tech,
        phlebotomists,
        housekeepers,
        other_hcw,
        administrative,
        escort,
    ]

    contacts = influenza1918.dictionary_of_contacts(professions, 1000000)
    total_hcw_involved = sum(contacts.values()) / (
        Profession.contacts_per_week
        * influenza1918.duration_in_weeks
        * (1 - Profession.attrition_rate)
    )

    mds_involved = md.number_of_profession_involved_in_pandemic(influenza1918, 1000000)
    rns_involved = rn.number_of_profession_involved_in_pandemic(influenza1918, 1000000)

    papr = Item(
        name="PAPR",
        single_price=500.0,
        box=Box(items_per_box=1, len=20.0, wid=16.0, dep=10.0),
        accessories=[
            (
                Item(
                    name="Filter set",
                    single_price=27.13,
                    box=Box(items_per_box=3, len=9.0, wid=9.0, dep=6.0),
                    accessories=[],
                ),
                3,
            ),
            (
                Item(
                    name="Battery",
                    single_price=286.0,
                    box=Box(1, 10.0, 10.0, 9.0),
                    accessories=[],
                ),
                1,
            ),
            (Item("Hood", 30.87, Box(3, 9.0, 9.0, 9.0)), 3),
            (Item("Tube", 30.89, Box(5, 20.0, 16.0, 10.0)), 3),
        ],
    )
    elastomeric = Item(
        name="Elastomeric",
        single_price=25.0,
        box=Box(items_per_box=10, len=7.0, wid=13.0, dep=18.0),
        accessories=[
            (
                Item(
                    name="E Filter set",
                    single_price=2.5,
                    box=Box(1, 5.3, 5.1, 1.4),
                    accessories=[],
                ),
                3,
            )
        ],
    )
    n95 = Item(
        name="N95",
        single_price=0.25,
        box=Box(items_per_box=20, len=12.0, wid=6.0, dep=6.0),
        accessories=[],
    )


# print(papr.total_price(),elastomeric.total_price(),n95.total_price())
# print(influenza1918.outpatient_visits(1000000))
# print(sum(contacts.values()))
# print(influenza1918.dictionary_of_contacts(professions, 1000000))
print(total_hcw_involved)
print(mds_involved)
print(rns_involved)
