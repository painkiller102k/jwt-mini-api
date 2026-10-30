
# JWT Mini-API

See on lihtne Pythonis loodud REST API, mis kasutab Flaski ja PyJWT teeki. Projekti eesmärk on õppida JWT-põhist autentimist, tokenite kontrollimist ja kasutajaõiguste piiramist.

## Funktsioonid

- `POST /login` kontrollib kasutajanime ja parooli ning tagastab JWT tokeni.
- `GET /profiil` tagastab kehtiva tokeni andmed.
- `GET /admin` lubab ligipääsu ainult administraatori rolliga kasutajale.
- Tokeni algoritm on `HS256` ja token kehtib 5 minutit.
- Salavõti loetakse keskkonnamuutujast `JWT_SECRET`.

## Nõuded

- Python 3.9 või uuem versioon
- pip

## Paigaldamine

Ava terminal projekti kaustas.

Loo virtuaalkeskkond ja aktiveeri see.

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Paigalda vajalikud teegid:

```bash
pip install -r requirements.txt
```

## Seadistamine

Enne rakenduse käivitamist määra keskkonnamuutuja `JWT_SECRET`.

### Windows PowerShell

```powershell
$env:JWT_SECRET = "asenda-oma-salavotmega"
```

### macOS / Linux

```bash
export JWT_SECRET="asenda-oma-salavotmega"
```

Ära lisa päris salavõtit GitHubi repositooriumisse.

## Rakenduse käivitamine

Käivita terminalis käsk:

```bash
python app.py
```

Rakendus töötab tavaliselt aadressil:

`http://127.0.0.1:5000`

Hoia terminal rakenduse töötamise ajal avatuna.

## Testkasutajad

| Kasutajanimi | Parool | Roll |
|---|---|---|
| `student` | `student123` | `student` |
| `admin` | `admin123` | `admin` |

Need kasutajad on mõeldud ainult testimiseks.

## API lõpp-punktid

### POST /login

Kontrollib kasutajanime ja parooli ning tagastab JWT tokeni.

Päringu keha (`application/json`):

```json
{
  "username": "student",
  "password": "student123"
}
```

Eduka sisselogimise korral tagastatakse HTTP `200 OK` ja token. Vale kasutajanime või parooli korral tagastatakse HTTP `401 Unauthorized`.

### GET /profiil

Tagastab kehtiva tokeni andmed.

Päringus peab olema päis:

```text
Authorization: Bearer <sinu-token>
```

Kehtiva tokeni korral tagastatakse HTTP `200 OK`. Puuduva või vigase tokeni korral tagastatakse HTTP `401 Unauthorized`.

### GET /admin

Lubab ligipääsu ainult administraatori rolliga kasutajale.

Kasuta sama päist:

```text
Authorization: Bearer <sinu-token>
```

- Administraatori token: HTTP `200 OK`
- Puuduv või vigane token: HTTP `401 Unauthorized`
- Tavakasutaja token: HTTP `403 Forbidden`

## Aegunud tokeni testimine

Fail `expired_token.py` loob tokeni, mille kehtivusaeg on juba möödunud.

Praeguses failis kasutatakse salavõtit `1982`. Selle testi jaoks peab ka API kasutama sama väärtust, vastasel juhul tokeni allkiri ei ühti.

1. Peata API, kui see töötab.
2. Määra keskkonnamuutuja `JWT_SECRET` väärtuseks `1982`.
3. Käivita API käsuga `python app.py`.
4. Ava teine terminal ja käivita:

   ```bash
   python expired_token.py
   ```

5. Kopeeri terminalis kuvatud token.
6. Saada `GET /profiil` päring päisega `Authorization: Bearer <token>`.

Oodatav tulemus: HTTP `401 Unauthorized`.

Pärast testi kasuta uuesti enda salavõtit. Ära kasuta väärtust `1982` päris rakenduses.

## Turvalisus

- Hoia salavõti saladuses.
- Ära kasuta testkasutajate paroole päris rakenduses.
- Päris rakenduses tuleb paroole turvaliselt räsida.
- Tootmiskeskkonnas tuleb silumisrežiim välja lülitada.
- Projekt on loodud õppimise ja testimise eesmärgil.
