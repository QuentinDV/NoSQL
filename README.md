# Projet NoSQL - RadioStream Analytics

Projet MongoDB complet pour une plateforme de station radio en ligne: base NoSQL, donnees de demonstration, requetes metier, API Flask et page web.

## Lancement avec Docker

```powershell
docker compose up --build
```

L'application est disponible sur:

```text
http://localhost:5000
```

Au demarrage, le conteneur charge automatiquement les donnees de demonstration dans MongoDB.

## Lancement local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:MONGO_URI="mongodb://localhost:27017"
python -m src.seed
flask --app src.app run --debug
```

## Livrables

- Dossier de projet: `docs/projet-nosql-radiostream.md`
- API: `src/app.py`
- Requetes MongoDB: `src/queries.py`
- Donnees de demonstration: `src/seed.py`
- Interface web: `web/index.html`, `web/app.js`, `web/styles.css`

## Endpoints utiles

- `GET /api/health`
- `GET /api/queries`
- `GET /api/queries/<query_id>`

Exemple:

```text
GET /api/queries/top_stations?days=14&limit=5
```
