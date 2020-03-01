# Problem sumy podzbioru

## Treść problemu

Mamy n-elementowy zbiór liczb całkowitych, czy istnieje jego podzbiór sumujący się do x?

## Przykład
```
Dla zbioru [1,2,3,4] możemy stworzyć podzbiory sumujące się do 3 (np. [1,2])

Dla zbioru [-1,-2,-3,-4] nie możemy stworzyć podzbioru sumującego się do 0
```

## Struktury danych

Zbiory liczb są listami elementów typu `int`.

Na wejściu dostajemy zbiór liczb oraz poszukiwaną liczbę
Na wyjściu dostajemy True, False, wartość typu `bool`