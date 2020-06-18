# Problem sumy podzbioru

## Treść problemu

Mamy n-elementowy zbiór liczb całkowitych, podaj dowolny niezerowy podzbiór liczb sumujący się do x (jeżeli istnieje)


## Przykład
```
Dla zbioru [1,2,3,4] możemy stworzyć podzbiory sumujące się do 3 (np. [1,2])

Dla zbioru [-1,-2,-3,-4] nie możemy stworzyć podzbioru sumującego się do 0
```

## Struktury danych

Zbiory liczb są listami elementów typu `int`.

Na wejściu dostajemy zbiór liczb oraz poszukiwaną liczbę.

Na wyjściu dostajemy dowolny podzbiór sumujący się do poszukiwanej liczby lub pusty zbiór `[]`

## Określenie warunków akceptacji

By sprawdzić poprawność rozwiązania problemu wystarczy wykonać dwa kroki:

1. Sprawdzić czy suma liczb podzbioru równa się poszukiwanej liczbie
2. Sprawdzić czy wszystkie liczby z podzbioru należą do zbioru liczb

## Wymagania
Program jest napisany dla Pythona 3.7+.
By zainstalować wymagane zależności należy wykonać:
```bash
pip install -r requirements.txt
```

## Jak uruchomić

Program można uruchomić na dwa sposoby

1. Uruchamiając testy jednostkowe:
```bash
pytest
```
2. Uruchamiając testy manualne:
```bash
python manual.py
```
uruchomienie ich bez dodatkowych parametrów wyświetli ekran pomocy
