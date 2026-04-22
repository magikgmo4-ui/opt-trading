# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_DOC_AUDIT_01 - 03_decisions

## Besoin initial

Clore la passe 3 en bornant ce qui est acquis par preuves, sans convertir l'audit comparatif en decision de stack finale.

## ETABLI

- `CrewAI`, `LangGraph`, `AutoGen` et `OpenAI Agents SDK` disposent tous de surfaces publiques suffisantes pour un audit technique documentaire de premier niveau.
- `Marblism` reste utile comme reference produit observee, mais pas comme source de primitives techniques developer-first.
- Les quatre sources techniques couvrent toutes, a des niveaux differents, des besoins pertinents pour une future architecture interne : roles, orchestration, etat/memoire, HITL, outils, observabilite.
- Les differences majeures observees a ce stade portent surtout sur le niveau d'abstraction, le couplage a un ecosysteme, et la profondeur des primitives runtime/persistence.

## HYPOTHESE

- Une passe suivante pourra raisonnablement transformer cette matrice de sources en matrice `besoin interne x pattern retenable x preuve x risque`, sans encore figer une stack unique.

## Decisions bornees

- decision : la passe 3 est consideree complete au niveau `audit technique detaille source par source`.
- decision : aucune stack finale n'est retenue dans ce GO.
- decision : `Marblism` reste dans le dossier comme reference produit observee seulement.
- decision : toute suite doit repartir de la matrice comparative deja consolidee, et non d'une preference implicite pour un framework.

## TODO

- preparer une passe de synthese architecture cible interne par axes : roles, orchestration, memoire, HITL, surfaces, observabilite, securite ;
- distinguer a la prochaine passe ce qui releve de primitives indispensables, d'options confort et de dependances ecosysteme ;
- conserver ce chantier en `doc-only`.

## REPRISE

- reprendre sur `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_DOC_AUDIT_01/02_journal_technique.md`
- relire en priorite la matrice comparative consolidee
- ne pas rouvrir le parent
- ne pas conclure sur une stack finale tant qu'une passe de synthese interne cible n'a pas ete redigee

## Verdict PASS / OPEN / FAIL

PASS
