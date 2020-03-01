def sprawdz_poprawnosc(poszukiwana_liczba, zbior, potencjalny_podzbior):
    if sum(potencjalny_podzbior) == poszukiwana_liczba:
        return all([liczba in zbior for liczba in potencjalny_podzbior])
    return False
