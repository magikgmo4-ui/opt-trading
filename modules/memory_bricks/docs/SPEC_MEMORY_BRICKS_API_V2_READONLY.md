# SPEC MEMORY_BRICKS API V2 READONLY

## Objectif

- proposer une surface read-only HTTP pour memory_bricks, destinee a un consumer humain/UI comme LocalCMS
- ne rien figer d'implementation premature: la spec decrit les contrats, pas le serveur
- preserver la compatibilite V1: le CLI V1 reste la source de verite operatoire
- separer clairement V1 (local CLI, stable) et V2 (API read-only, a confirmer par consumer)

## Positionnement V1 vs V2

| Dimension | V1 (livre) | V2 (spec, pas implementee) |
|-----------|------------|---------------------------|
| Acces | CLI local (`cmd.sh query ...`) | HTTP/REST (endpoints decrits ci-dessous) |
| Mutation | `new`, `status`, `link`, `index rebuild` | hors perimetre V2 |
| Source d'etat | `_state/memory_bricks` (ou `MEMORY_BRICKS_STATE_ROOT`) | idem, via le meme backend V1 |
| Dependances | Python, bash, filesystem local | theoriquement FastAPI ou equiv. (pas d'impl) |
| Cible | operateur technique | consumer humain/UI (LocalCMS) |
| Garantie | testee, closee, mergee | spec only, a valider par consumer reel |

## Ressources lisibles

### Brick (ressource atomique)

Représente une brique memoire unique.

Champs exposes:
- `id`: identifiant stable (ex: `MB-00001`)
- `title`: titre lisible
- `type`: `resume_point`, `reference`, `decision`, ...
- `status`: `open`, `closed`, `resumed`, `draft`, ...
- `ia`: IA d'origine (ex: `chatgpt`, `claude`)
- `machine`: machine d'origine
- `surface`: surface d'origine
- `project`: projet
- `module`: module
- `summary_short`: resume court
- `resume_point`: point de reprise
- `tags`: liste de tags
- `links`: liste d'IDs liees
- `date`: date ISO 8601
- `decisions`: liste de decisions
- `todo`: liste de taches

### Index (vue d'ensemble)

Deux representations:
- `index_short.md`: resume markdown lisible par humain
- `index_full.json`: index structure (liste d'IDs + meta)

### Source status (etat de la source)

Meme surface que `query status` V1:
- `root`: chemin racine
- `root_exists`: oui/non
- `bricks_dir`: oui/non
- `bricks`: nombre de briques
- `index_full`: oui/non
- `index_short`: oui/non
- `sequence`: oui/non

### Recherche (vue texte)

Recherche texte simple sur: id, title, summary_short, resume_point, tags, contenu markdown.

## Operations read-only proposees

### GET /health

Sanity check rapide de l'API.

```
200 OK
{
  "status": "ok",
  "module": "memory_bricks",
  "version": "v2-readonly-spec"
}
```

### GET /status

Retourne l'etat de la source V1.

```
200 OK
{
  "root": "/home/fantome/opt-trading/_state/memory_bricks",
  "root_exists": true,
  "bricks_dir": true,
  "bricks": 42,
  "index_full": true,
  "index_short": true,
  "sequence": true
}

404 NOT FOUND
{
  "root_exists": false
}
```

### GET /bricks

Liste les briques avec filtres optionnels.

Query params (meme surface que V1 `query list`):
- `status` (optionnel)
- `type` (optionnel)
- `project` (optionnel)
- `module` (optionnel)
- `machine` (optionnel)
- `ia` (optionnel)
- `surface` (optionnel)
- `tag` (optionnel)
- `limit` (optionnel, defaut 50)
- `offset` (optionnel, defaut 0)

```
200 OK
{
  "items": [
    {
      "id": "MB-00001",
      "title": "Sample Brick",
      "status": "open",
      "type": "resume_point",
      "ia": "chatgpt",
      "date": "2026-03-28T20:00:00Z"
    },
    ...
  ],
  "total": 42,
  "limit": 50,
  "offset": 0
}
```

### GET /bricks/{id}

Retourne le contenu complet d'une brique (markdown).

```
200 OK
{
  "id": "MB-00001",
  "title": "Sample Brick",
  "type": "resume_point",
  "status": "open",
  "ia": "chatgpt",
  "machine": "student",
  "surface": "terminal_linux",
  "project": "opt-trading",
  "module": "memory_bricks",
  "date": "2026-03-28T20:00:00-04:00",
  "summary_short": "Short summary.",
  "resume_point": "Continue here.",
  "tags": ["memory", "test"],
  "links": ["MB-00002"],
  "decisions": [],
  "todo": [],
  "content_markdown": "# Sample Brick\n\n..."
}

404 NOT FOUND
{
  "error": "Brick not found"
}
```

### GET /bricks/{id}/links

Retourne les briques liees a la brique ciblee.

```
200 OK
{
  "id": "MB-00001",
  "links": [
    {"id": "MB-00002", "title": "Viewer Contract", "status": "open"},
    ...
  ]
}
```

### GET /find

Recherche texte.

Query params:
- `text` (requis): texte a rechercher
- `limit` (optionnel, defaut 50)
- `offset` (optionnel, defaut 0)

```
200 OK
{
  "items": [
    {"id": "MB-00002", "title": "Viewer Contract", "excerpt": "...needle-decision..."},
    ...
  ],
  "total": 1,
  "query": "needle-decision"
}

400 BAD REQUEST
{
  "error": "Query text cannot be empty"
}
```

### GET /indexes

Retourne les index disponibles.

```
200 OK
{
  "short_available": true,
  "full_available": true,
  "short_url": "/indexes/index_short.md",
  "full_url": "/indexes/index_full.json"
}
```

### GET /indexes/short

Retourne le contenu brut de `index_short.md`.

```
200 OK
Content-Type: text/markdown

(index_short.md brut)
```

### GET /indexes/full

Retourne le contenu brut de `index_full.json`.

```
200 OK
Content-Type: application/json

(index_full.json brut)
```

## Garanties de compatibilite / non-regression V1

- la source d'etat reste `_state/memory_bricks` (ou `MEMORY_BRICKS_STATE_ROOT`)
- l'API V2 ne fait que lire, elle ne cree jamais de directories, jamais de brique, jamais d'index
- les filtres V2 `GET /bricks` correspondent exactement aux filtres V1 `query list`
- les erreurs V2 correspondent aux erreurs V1 (`Brick not found`, `Query text cannot be empty`)
- le CLI V1 `query` reste l'outil operatoire de reference
- l'API V2 est un sous-ensemble read-only du CLI V1

## Points a confirmer par le consumer (LocalCMS)

Les elements suivants sont proposes dans cette spec mais doivent etre valides par un consumer reel:

| Element | Statut | Question ouverte |
|---------|--------|-----------------|
| Format JSON de `GET /bricks` | a confirmer | faut-il un envelope `{"items": [...]}` ou un array plat ? |
| Pagination (`limit`/`offset`) | a confirmer | LocalCMS a-t-il besoin de pagination ou le count est-il faible ? |
| `content_markdown` dans `GET /bricks/{id}` | a confirmer | LocalCMS veut-il le markdown brut ou seulement les champs structures ? |
| `GET /bricks/{id}/links` | a confirmer | local CMS a-t-il besoin d'un endpoint dedie aux liens ? |
| `GET /indexes/*` | a confirmer | LocalCMS a-t-il besoin de lire les index bruts ? |
| `GET /health` | a confirmer | format minimal acceptable pour le health check ? |
| Content-Type negociation | a confirmer | JSON uniquement ou support markdown brut accepte ? |
| Authentification | a confirmer | API locale uniquement (localhost) ou besoin d'auth ? |

## Ce que cette spec ne definit pas

- pas de framework implementatif impose (FastAPI, Flask, quart, etc.)
- pas de port par defaut
- pas de mecanisme d'authentification
- pas de cache
- pas de pagination cursor-based
- pas de WebSocket/SSE pour les changements en temps reel
- pas de mutation (create, update, delete)
- pas de souscription webhooks

## Limites connues

- la source d'etat reste locale: l'API V2 doit tourner sur la meme machine que `_state/memory_bricks`
- la latence depend du filesystem (pas de base de donnees)
- pas de multi-utilisateur garanti
- pas de haute disponibilite
- le markdown brut peut etre volumineux pour de nombreuses briques

## Ordre d'implementation propose (futur)

1. `GET /health` — sanity minimal
2. `GET /status` — etat de la source (fonde sur `_render_query_status` V1)
3. `GET /bricks` — liste avec filtres (fonde sur `list_bricks` V1)
4. `GET /bricks/{id}` — brique unique (fonde sur `show_brick` V1)
5. `GET /find` — recherche (fonde sur `find_bricks` V1)
6. `GET /indexes/*` — index bruts (optionnel, a confirmer)

Chaque endpoint peut etre merge separement apres validation du consumer.
