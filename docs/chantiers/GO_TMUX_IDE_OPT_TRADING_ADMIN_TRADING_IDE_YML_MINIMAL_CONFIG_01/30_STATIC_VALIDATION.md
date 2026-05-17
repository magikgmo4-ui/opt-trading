# 30_STATIC_VALIDATION

## 1_MASTER_TARGET

Documenter la validation statique du draft `ide.yml` minimal.

## 7_CANONICAL_STATE

Validation executee hors repo dans un repertoire temporaire, avec suppression du repertoire temporaire apres test.

Commande de validation :

```powershell
npx -y tmux-ide@1.3.1 validate --json
```

Contexte :

- aucun `npm install -g` ;
- aucun `ide.yml` actif ajoute au repo ;
- aucun lancement de session ;
- aucune commande `init`, `detect --write` ou `config set`.

## 8_VALIDATED_DRAFT

```yaml
name: opt-trading-admin-trading
rows:
  - size: 70%
    panes:
      - title: Shell
        command: pwd
        focus: true
      - title: Git
        command: git status --short --branch
  - size: 30%
    panes:
      - title: Docs
        command: ls docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_IDE_YML_MINIMAL_CONFIG_01
```

## 9_VALIDATION_RESULT

Resultat observe :

```json
{
  "valid": true,
  "errors": []
}
```

Verdict statique :

```text
PASS_STATIC_VALIDATE
```

## 10_LIMITS

Cette validation ne prouve pas encore :

- que la session tmux-ide doit etre lancee ;
- que le layout est ergonomique en usage operateur ;
- que le chemin repo distant final est le bon ;
- que les panes doivent devenir persistants ;
- que `tmux-ide` doit etre installe globalement.

## 12_INVARIANTS

- Validation statique seulement.
- Pas de session runtime.
- Pas de fichier actif cree.
- Pas de mutation remote `admin-trading`.

## 17_RESUME_POINT

Le draft passe `tmux-ide@1.3.1 validate --json`. La gate de session reste a lire dans `40_GATE_DECISION.md`.
