# README - Livrabile proiect licenta

## Date generale

**Titlu proiect:** Platforma educationala de retelistica in GNS3 cu automatizare Python si asistent AI integrat  
**Candidat:** David-Alexandru Mirci  
**Program:** Informatica  
**Universitate:** Universitatea Politehnica Timisoara  
**Sesiune:** Iulie 2026  

## Repository cod sursa

**Repository Git:** https://github.com/davidd234/Licenta

Repository-ul contine codul sursa al componentelor software dezvoltate pentru proiect, fara fisiere binare compilate, fara imagini IOS/FortiGate, fara chei API si fara fisiere temporare generate la rulare.

## Descrierea proiectului

Proiectul reprezinta o platforma educationala de retelistica realizata in GNS3. Topologia este impartita in zone cu rol didactic clar: Site A, Site B, Customer Office, Core/WAN, Admin, DMZ, Security Edge si Site Profesor AI.

Platforma include:

- laboratoare de retelistica pentru VLAN-uri, trunking, STP/RSTP, EtherChannel, RIPv2, rute default si statice, DHCP, SSH/Telnet, securitate Layer 2, SCP backup, ACL-uri, DMZ, FortiGate si Snort/Darkstat;
- o componenta de automatizare Python pentru verificarea conectivitatii, acces SSH/Telnet si extragerea configuratiilor de pe echipamente;
- un asistent educational AI, denumit Profesor AI, care poate raspunde la intrebari despre topologie, concepte Cisco si troubleshooting.

## Livrabile incluse

1. **Documentatia lucrarii**
   - documentatia finala in format `.docx` si/sau `.pdf`;
   - descrierea topologiei, a laboratoarelor si a etapelor de testare.

2. **Proiectul GNS3**
   - topologia exportata din GNS3 sau fisierele necesare pentru recrearea acesteia;
   - configuratiile echipamentelor, acolo unde acestea pot fi exportate;
   - capturile si verificarile relevante pentru laboratoare.

3. **Cod sursa pentru automatizarea retelei**
   - `Yaml & main Automation/main.py` - aplicatia Python pentru automatizare;
   - `Yaml & main Automation/network.yaml` - fisierul de inventar cu echipamentele si datele de conectare.

4. **Cod sursa pentru Profesor AI**
   - `Profesor AI/mainAI.py` - aplicatia Python pentru asistentul educational;
   - `Profesor AI/.env.example` - exemplu de configurare pentru cheia API si model.

5. **README**
   - acest fisier, care descrie livrabilele, pasii de instalare, pasii de compilare si pasii de lansare.

## Structura repository-ului

```text
Licenta/
├── README.md
├── requirements.txt
├── .gitignore
├── Profesor AI/
│   ├── mainAI.py
│   └── .env.example
└── Yaml & main Automation/
    ├── main.py
    └── network.yaml
```

Observatie: imaginile IOS, imaginile FortiGate, fisierele binare mari, cheile API, mediile virtuale Python si fisierele generate automat nu trebuie incluse in repository.

## Cerinte software

Pentru rularea proiectului sunt necesare:

- Python 3.10 sau mai nou;
- GNS3 Client si acces la GNS3 Server;
- imaginile/appliance-urile necesare pentru routere, switch-uri, FortiGate, VPCS si hosturi Linux;
- acces SSH/Telnet catre echipamentele din topologie pentru componenta de automatizare;
- conexiune la Internet pentru componenta Profesor AI, daca se foloseste API-ul OpenAI.

Biblioteci Python folosite:

```text
netmiko
PyYAML
Flask
requests
python-dotenv
```

Acestea sunt trecute in fisierul `requirements.txt`.

## Pasi de instalare

1. Se cloneaza repository-ul:

```bash
git clone https://github.com/davidd234/Licenta.git
cd Licenta
```

2. Se creeaza un mediu virtual Python:

```bash
python -m venv .venv
```

3. Se activeaza mediul virtual.

Pe Linux/macOS:

```bash
source .venv/bin/activate
```

Pe Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Se instaleaza dependentele:

```bash
pip install -r requirements.txt
```

5. Pentru Profesor AI se creeaza fisierul `.env` pe baza fisierului `.env.example`:

```text
OPENAI_API_KEY=cheia_api_personala
OPENAI_MODEL=gpt-4o-mini
```

Atentie: fisierul `.env` nu se publica in repository, deoarece poate contine date sensibile.

## Pasi de compilare

Aplicatiile sunt scrise in Python, deci nu necesita compilare clasica. Codul este interpretat la rulare.

Optional, se poate verifica sintaxa fisierelor Python cu:

```bash
python -m py_compile "Yaml & main Automation/main.py"
python -m py_compile "Profesor AI/mainAI.py"
```

Daca nu apar erori, fisierele Python sunt valide sintactic.

## Pasi de lansare - proiect GNS3

1. Se porneste GNS3 Client.
2. Se conecteaza clientul la GNS3 Server.
3. Se importa proiectul GNS3 sau se deschide topologia existenta.
4. Se verifica existenta appliance-urilor si imaginilor necesare.
5. Se pornesc echipamentele din topologie.
6. Se verifica adresele IP si conectivitatea de baza prin comenzi precum:

```bash
ping <ip_gateway>
show ip interface brief
show ip route
```

7. Pentru testarea automatizarii, hostul de administrare trebuie sa aiba conectivitate catre echipamentele definite in `network.yaml`.

## Pasi de lansare - Network Automation

Componenta de automatizare foloseste fisierul `network.yaml`, in care sunt definite echipamentele, IP-urile de management, protocolul de acces, utilizatorul, parola si parola de enable.

1. Se intra in folderul componentei de automatizare:

```bash
cd "Yaml & main Automation"
```

2. Se verifica fisierul `network.yaml` si se adapteaza IP-urile daca topologia a fost modificata.

3. Se ruleaza aplicatia:

```bash
python main.py
```

4. Din meniul aplicatiei se pot folosi optiunile:

```text
1. Configure an interface on a device (Interactively)
2. Verify Connectivity
3. Test NetworkAutomation reachability to all YAML devices
4. See the config of a device
5. Delete a test interface
0. Exit
```

5. Pentru verificarea rapida a conectivitatii catre toate echipamentele, se foloseste optiunea 3 din meniu.

## Pasi de lansare - Profesor AI

Componenta Profesor AI ruleaza ca aplicatie Python si poate fi folosita in doua moduri: chat local din terminal sau server API.

1. Se intra in folderul componentei AI:

```bash
cd "Profesor AI"
```

2. Se verifica existenta fisierului `.env`:

```text
OPENAI_API_KEY=cheia_api_personala
OPENAI_MODEL=gpt-4o-mini
```

3. Pentru folosirea meniului local:

```bash
python mainAI.py
```

4. Din meniu se poate alege:

```text
1. Porneste serverul API in background
2. Chat local cu Profesor AI
3. Testeaza conexiunea OpenAI
4. Afiseaza ultimele linii din server.log
5. Opreste serverul API
0. Iesire
```

5. Pentru pornirea directa a serverului API:

```bash
python mainAI.py --server
```

6. Serverul API ruleaza pe portul 5000 si ofera endpoint-ul:

```text
POST http://127.0.0.1:5000/ask
```

Exemplu de test cu `curl`:

```bash
curl -X POST http://127.0.0.1:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Explica-mi pe scurt rolul VLAN-ului 99 in proiect."}'
```

## Observatii de securitate si predare

- Nu se incarca in repository fisiere `.env` care contin chei API.
- Nu se incarca token-uri, parole reale sau date sensibile.
- Nu se incarca imagini IOS, FortiGate sau alte fisiere licentiate.
- Nu se incarca directoare `.venv`, `__pycache__`, fisiere `.pyc`, loguri sau fisiere binare generate automat.
- Fisierul `network.yaml` contine credentiale de laborator; intr-un mediu real acestea trebuie inlocuite cu variabile de mediu sau mecanisme securizate.

## Verificare finala recomandata inainte de predare

Inainte de incarcarea proiectului, se recomanda verificarea urmatoarelor puncte:

- repository-ul contine codul sursa Python;
- README-ul contine adresa repository-ului;
- fisierele binare si mediile virtuale nu sunt incluse;
- proiectul GNS3 sau instructiunile de import sunt prezente;
- `requirements.txt` contine dependentele necesare;
- `network.yaml` este in acelasi folder cu aplicatia de automatizare;
- Profesor AI are un fisier `.env.example`, dar nu contine cheia API reala;
- comenzile `python main.py` si `python mainAI.py` pornesc aplicatiile corespunzatoare.

## Concluzie

Acest README descrie livrabilele proiectului si pasii necesari pentru instalarea, verificarea si lansarea componentelor principale. Proiectul nu necesita compilare clasica, fiind bazat pe Python si GNS3. Rularea completa presupune pornirea topologiei GNS3, verificarea conectivitatii catre echipamente, rularea componentei Network Automation si, optional, pornirea componentei Profesor AI pentru suport educational.
