# Carte locale cursor-ai

## Identite locale retenue

- machine locale : `DESKTOP-1KDQTBH`
- utilisateur courant : `desktop-1kdqtbh\ghost`
- repo courant : `C:\Users\ghost\opt-trading`
- role : poste Windows local d'orchestration multi-agents, de controle Git et d'IDE

## Controles locaux executes

```powershell
git status --short --branch
git branch --list
where.exe git
where.exe gh
where.exe claude
where.exe trae
where.exe node
where.exe npm
where.exe python
where.exe opencode
$PSVersionTable.PSVersion.ToString()
```

## Outils detectes

| Outil | Resultat constate | Statut |
| --- | --- | --- |
| `git` | `C:\Program Files\Git\cmd\git.exe` | `PASS` |
| `gh` | `C:\Program Files\GitHub CLI\gh.exe` | `PASS` |
| `claude` | present dans `C:\Users\ghost\.local\bin\claude.exe` et via package WinGet | `PASS` |
| `trae` | present dans `c:\Users\ghost\AppData\Local\Programs\Trae\bin\trae(.cmd)` | `PASS` |
| `node` | `C:\Program Files\nodejs\node.exe` | `PASS` |
| `npm` | `C:\Program Files\nodejs\npm(.cmd)` | `PASS` |
| `python` | present via `WindowsApps` et `C:\Users\ghost\AppData\Local\Python\bin\python.exe` | `PASS` |
| `opencode` | non detecte localement | `NOT_FOUND` |
| `PowerShell` | `7.5.5` | `PASS` |

## Surfaces repo utiles detectees

| Surface | Etat local | Role retenu |
| --- | --- | --- |
| `workflow_ai/` | present | doctrine d'execution gatee pour missions IDE / agents |
| `workflow_ai/prompts/` | present | prompts locaux utiles au pilotage `cursor-ai` |
| `modules/validated_prompt_factory/` | present | generation de prompts specialises depuis synthese validee |
| `modules/validated_prompt_factory/contextuals/actions.ctx` | present | contextual local imbrique, utile aux prompts |
| `docs/deploy_module_multi_machine_continuity.md` | present | reference de deploiement multi-machine, pas poste runtime principal |
| `docs/ot/trae/trae_pack_texts/README.md` | present | memoire legacy Trae/IDE de lecture seulement |
| `modules/contextuals/` | absent | pas de module top-level confirme sur cette ligne |
| `modules/deploy/` | absent | pas de module top-level confirme sur cette ligne |
| `bundles/` | absent sur cette branche | surface prouvee surtout via branche distante `bundles` |
| `docs/workflow/` | absent | la doctrine active est dans `workflow_ai/`, pas ici |
| `docs/prompts/` | absent | les prompts prouvés sont dans `workflow_ai/prompts/` ou Prompt Factory |

## Branches locales utiles a la posture cursor-ai

- branche de travail courante : `go/GO_OPT_TRADING_MULTI_AGENTS_CURSOR_AI_PARENT_ALIGNMENT_01`
- branche parent multi-agents disponible : `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`
- sauvegarde locale de reference presente : `save/cursor-ai-2026-04-01`

## Limites

- aucun `OpenCode` local n'a ete detecte, donc `cursor-ai` n'est pas documente ici comme hote runtime `OpenCode`
- `OpenClaw` ne doit pas etre relu comme outil local de `cursor-ai` ; il reste borne cote `db-layer`
- cette carte ne configure ni PATH, ni outils, ni IDE

## Conclusion

`cursor-ai` est bien un poste local Windows utile pour :

- cadrage humain
- pilotage agents
- generation / controle de prompts
- gestion des branches et du repo
- lecture de surfaces doctrinales et de continuité

Ce n'est pas, dans ce GO :

- une machine runtime `OpenClaw`
- une machine d'execution `LocalCMS`
- une machine de trading runtime
