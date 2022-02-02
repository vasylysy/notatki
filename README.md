# notatki (not finished)

Opis projektu:
Aplikacja pozwala zalogowanemu użytkownikowi na przechowywanie notatek tekstowych. Niektóre notatki mogą być zaznaczone jako zaszyfrowane. Odszyfrowanie powinno wymagać podania tajnego hasła.

Notatki pozwalają na podstawowe ostylowanie.

Moduł uwierzytelniania zakłada:

    walidację danych wejściowych (z negatywnym nastawieniem),
    opóźnienia (żeby utrudnić zdalne zgadywanie i atak brute-force),
    ograniczone informowanie o błędach (np. o tym przyczynie odmowy uwierzytelenia),
    bezpieczne przechowywanie hasła (wykorzystanie kryptograficznych funcji mieszających,i limity prób  wykorzystanie soli, wielokrotne hashowanie),
    kontrola siły hasła, żeby uświadomić użytkownikowi problem,
    zarządzanie uprawnieniami do zasobów.

Wymagania:

    aplikacja posiada bazę danych (SQLite),
    bezpieczne połączenie z aplikacją (szyfrowane połączenie),
    wszystkie dane wejściowe od użytkownika podlegają walidacji z negatywnym nastawieniem,
    zwiększenie opóznienia po nieudanej próbie logowania,
    sprawdzanie jakości hasła.
   
