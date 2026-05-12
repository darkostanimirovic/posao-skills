# posao-skills

Javna kolekcija praktičnih Codex skillova za ljude koji vode `DOO` ili rade kao `preduzetnici` u Srbiji.

Cilj ovog repoa je da na jednom mestu skuplja korisne i ponovo upotrebljive skillove za administrativne, poreske, platne i dokumentacione obaveze koje se često javljaju u vođenju malog biznisa u Srbiji.

Trenutni fokus:

- generisanje `IPS QR` kodova za plaćanje
- obračun godišnjeg poreza na dohodak građana kroz `PP GPDG`

Planirane dopune:

- pravljenje invoice-ova
- dokumenti o promeni plate
- odluke o odmoru i slična HR / administrativna dokumentacija
- druge ponavljajuće obaveze i šabloni za firme i preduzetnike

## Trenutni skillovi

### `ips-qr-kod-generator`

Generiše i validira srpske `NBS IPS QR` kodove za plaćanje na osnovu podataka za uplatu.

Zašto je koristan:

- umesto da ručno kucaš podatke u bankarsku aplikaciju
- ili da kopiraš vrednosti polje po polje
- generišeš IPS QR kod i samo ga skeniraš

Šta sadrži:

- normalizaciju podataka za uplatu
- validaciju preko NBS IPS QR validatora
- generisanje PNG QR koda
- primer ulaznog JSON fajla

Lokacija:

- `skills/ips-qr-kod-generator/`

### `godisnji-porez-na-dohodak-gradjana`

Pomaže u obračunu i proveri prijave za srpski godišnji porez na dohodak građana `PP GPDG` za bilo koju poresku godinu.

Šta sadrži:

- workflow za obračun godišnjeg poreza
- preporuke gde da se nađu zvanični godišnji pragovi i olakšice
- podršku za lični odbitak, izdržavane članove porodice, dodatno umanjenje za mlađe od 40 i poreski kredit
- primer ulaznog JSON fajla sa zaobljenim, ilustrativnim vrednostima

Lokacija:

- `skills/godisnji-porez-na-dohodak-gradjana/`

## Kako se koristi

Ovaj repo ne zahteva instalaciju kao aplikacija ili paket. Ideja korišćenja je jednostavna:

1. Preuzmi ili kloniraj repo.
2. Otvori `skills/` direktorijum.
3. Prekopiraj ceo skill folder koji ti treba na svoju lokalnu lokaciju za Codex skillove.

Mogući načini korišćenja:

- kopiraš samo jedan konkretan skill
- kopiraš sve foldere iz `skills/`
- zadržiš ovaj repo kao izvor i kasnije selektivno preuzimaš izmene

Ako koristiš Codex lokalno, česta ciljna lokacija je `~/.codex/skills/`, ali može i bilo koja druga lokalna lokacija koju koristiš za skillove.

## Opcija 1: kloniranje repoa

```bash
git clone https://github.com/darkostanimirovic/posao-skills.git
cd posao-skills
```

Posle toga iz `./skills/` prekopiraš skill foldere koji ti trebaju.

## Opcija 2: preuzimanje ZIP arhive

1. Otvori `https://github.com/darkostanimirovic/posao-skills`
2. Klikni na `Code`
3. Klikni na `Download ZIP`
4. Raspakuj arhivu
5. Prekopiraj željene foldere iz `skills/` na svoju lokalnu lokaciju za skillove

## Napomene

- Primeri u ovom repou su anonimni i ilustrativni.
- Poreske obračune koji zavise od konkretne godine uvek treba proveriti prema aktuelnim zvaničnim izvorima u Srbiji.
- Uključene skripte su pomoćni alati; odgovarajući `SKILL.md` fajlovi objašnjavaju kada i kako treba da se koriste.
