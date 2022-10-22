wyświetl wszystkie obiekty modelu Osoba 
Person.objects.all() 

wyświetl obiekt modelu Osoba z id = 3,
Person.objects.get(id=3) 

wyświetl obiekty modelu Osoba, których nazwa rozpoczyna się na wybraną przez Ciebie literę alfabetu (tak, żeby był co najmniej jeden wynik),
Person.objects.filter(imie__startswith='M') 

wyświetl unikalną listę drużyn przypisanych dla modeli Osoba,


wyświetl nazwy drużyn posortowane alfabetycznie malejąco,
Team.objects.order_by('-name')   

dodaj nową instancję obiektu klasy Osoba
Person.objects.create(imie="Bruce", nazwisko="Springsteen", miesiac=3, team_id='1') 