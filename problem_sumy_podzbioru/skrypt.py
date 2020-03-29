import random

def sprawdz_rozwiazanie(poszukiwana_liczba, zbior, potencjalny_podzbior):
    if all(liczba in zbior for liczba in potencjalny_podzbior):
        return abs(sum(potencjalny_podzbior)-poszukiwana_liczba)
    
    return -1

def sprawdz_poprawnosc(poszukiwana_liczba, zbior, potencjalny_podzbior):
    return sprawdz_rozwiazanie(poszukiwana_liczba, zbior, potencjalny_podzbior) == 0

def test_poprawnosci():
    test_set = [x for x in range(100)]
    test_subset = random.sample(test_set, 5)
    number = sum(test_subset)

    test_subset_1 = [-1,-2]
    test_subset_2 = [1,2]

    subsets = [test_subset, test_subset_1, test_subset_2]

    for subset in subsets:
        print(f"Wynik dla {subset}: {sprawdz_rozwiazanie(number, test_set, subset)}")

test_poprawnosci()