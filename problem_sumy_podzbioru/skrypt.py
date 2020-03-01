def sprawdz_poprawnosc(zbior, potencjalny_podzbior, poszukiwana_liczba):
    if sum(potencjalny_zbior) == poszukiwana_liczba:
        return all([liczba in zbior for liczba in potencjalny_zbior])
