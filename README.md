# __init__.py

In acest fisier s-a definit functia create_app() care creeaza o noua instanta Flask numita app, incarca configurarile aplicatiei dintr-un fisier extern configure.py. Acest fisier poate contine variabile de configurare personalizate cum ar fi secret key, optiuni de debug, sau alte setari specifice.
register_blueprint este utilizat pentru a inregistra modulele functionale (blueprint-uri) in aplicatie:

main_blueprint – functionalitati legate de autentificare, inregistrare si profil (auth.py).

cart_blueprint – gestionarea cosului de cumparaturi (cart.py).

products_blueprint – listarea si vizualizarea produselor (products.py).

checkout_blueprint – procesul de finalizare a comenzilor (checkouts.py).
Linia comentata vrea sa sugereze ca a fost planificata o functionalitate legata de categorii de produse, dar nu este implementata inca. In final, functia da return la instanta configurata a aplicatiei Flask, gata de a fi rulata.

# auth.py

 load_users()
Aceasta functie incarca baza de date cu utilizatori din fisierul users.json.
Daca fisierul nu exista, returneaza un dictionar gol.
Este utilizata pentru autentificare, inregistrare si gestionarea cosului de cumparaturi.

index()
Aceasta este ruta principala a blueprint-ului de autentificare.
Daca utilizatorul este deja autentificat, este redirectionat catre pagna produselor.
In caz contrar, se afiseaza pagina principala (index.html).

login()
Gestioneaza logarea utilizatorilor prin formularul LoginForm.
Verifica daca username-ul, parola si emailul se potrivesc cu cele din users.json.
Daca datele sunt corecte, se seteaza sesiunea si se redirectioneaza utilizatorul.
In caz contrar, se afiseaza un mesaj de eroare.

signup()
Permite utilizatorilor sa isi creeze un cont nou.
Verifica daca numele de utilizator exista deja, iar daca nu, salveaza datele in users.json.
In caz de succes, utilizatorul este redirectionat catre pagina de login.
Daca formularul este invalid, se afiseaza un mesaj de avertizare.

logout()
Aceasta functie elimina utilizatorul curent din sesiune.
Dupa logout, utilizatorul este redirectionat la pagina de login.
Este insotit de un mesaj flash de informare.

compute_order_stats(user_orders)
Calculeaza statistici pentru comenzile unui utilizator : totalul cheltuit, numarul total de produse, pretul mediu pe produs.
Generezaa de asemenea o lista detaliata cu informatii pentru fiecare comanda.
Este folosita in profilul utilizatorului pentru afisarea analitica a istoricului de comenzi.

profile()
Afiseaza pagina cu profilul pentru utilizatorul autentificat.
Incarca comenzile din directorul submitted-orders si le filtreaza dupa utilizator.
Calculeaza statistici si le trimite catre template-ul profile.html.
Include o vizualizare a valorilor per comanda in timp (pret si cantitate).

# cart.py

load_users() – Incarca datele utilizatorilor din fisierul users.json. Daca fisierul nu exista returneaza un dictionary gol.

load_carts() – Incarca cosurile salvate din fisierul carts.json. Creeaza fisierul daca nu exista.

save_carts(carts_data) – Salveaza in fisier cosurile de cumparaturi ale utilizatorilor.

load_products() – Incarca lista de produse din products.json.

get_product_by_id(product_id) – Returneaza produsul corespunzator unui ID dat

get_session_cart() – Returneaza cosul din current session daca utilizatorul nu este logat. Creeaza unul nou daca nu exista.

save_session_cart(cart_data) – Salveaza cosul in sesiune.

get_user_cart(username) – Returneaza cosul unui utilizator logat (din fisier) sau cosul din sesiune daca utilizatorul nu este logat.

save_user_cart(username, cart_data) – Salveaza cosul pentru utilizatorul logat (in fisier) sau in sesiune daca nu este logat.

calculate_total(cart_items) – Calculeaza suma totala a produselor din cos, pe baza cantitatii si preturilor.

#  forms.py

Aici am definit doua formulare folosind Flask-WTF si WTForms pentru autentificarea si inregistrarea utilizatorilor:
LoginForm: Formular pentru autentificare, cu campuri pentru username, parola si email, fiecare avand validatori pentru date
obligatorii, format corect si lungimi minime/modele specifice.
SignUpForm: Formular pentru inregistrare, cu aceleasi campuri si validatori ca LoginForm, asigurand validarea datelor introduse
 de utilizator pentru un username valid, o parola suficient de lunga si un email valid.

# products,py

load_products()
Incarca lista de produse dintr-un fisier JSON. Daca fisierul nu exista, returneaza un dictionar gol. Este functia principala 
pentru accesaea datelor despre produse.

listing_products()
Verifica daca utilizatorul este autentificat (exista in sesiune). Daca nu, il redirectioneaza la pagina de login. Incarca toate
 produsele si le afiseaza in pagina principala a catalogului.

product_detail(product_id)
Cauta un produs specific dupa product_id. Daca produsul nu exista, returneaza o eroare 404 (Not Found). Daca il gaseste, afiseaza 
detaliile produsului in pagina dedicata.

product_discounts()
Creeaza o lista cu produsele care au pret redus (compara pretul original cu pretul actual) si afiseaza doar acestea, intr-o pagina 
speciala pentru produse cu discount.

# Fronte-end
In privinta front-end ului , exista un base.html care va fi extins cu jiinja2 pentru toate acele pagini html.

# Bonus ? 
Puncte potentiale de bonus: automatizare comenzi, pastrare in memorie pentru orice actiune importanta a userului in format json , stoc dinamic, pagina de "statistici" etc.