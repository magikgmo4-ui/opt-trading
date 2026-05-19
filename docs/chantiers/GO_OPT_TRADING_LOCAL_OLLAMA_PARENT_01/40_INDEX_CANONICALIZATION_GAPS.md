# Gaps de canonisation index

## Gaps constates

- la branche parent locale ne contient pas `docs/index/GO_CLOSED_INDEX.md`
- la branche parent locale ne contient pas `docs/index/GO_PARENT_THREAD_MAP.md`
- `GO_INDEX.md` de cette branche est ancien et ne porte pas la ligne `Local Ollama`
- `ACTIVE_STREAMS.md` de cette branche ne reprend pas le parent `Local Ollama`
- `NEXT_GO_CANDIDATES.md` de cette branche ne reprend pas le parent ni son child
- `BRANCH_STATE.md` de cette branche est un index ancien, trop etroit et non transferable tel quel

## Ce qui doit rester local / inbox dans ce lot

- `docs/index/inbox/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01.md`
- les nouveaux documents de reprise du parent

## Ce qui necessite un batch d'agregation plus tard

- integration de la ligne parent `Local Ollama` dans `GO_INDEX.md`
- integration du flux parent dans `ACTIVE_STREAMS.md`
- integration du `next GO` conditionnel dans `NEXT_GO_CANDIDATES.md`
- classification de branche dans `BRANCH_STATE.md`
- eventuelle mise a jour `REPRISE.md` si le parent redevient flux actif de la ligne canonique recente

## Regle retenue

- ne pas modifier les gros index depuis cette branche vieillie sauf necessite forte
- ne pas importer aveuglement `docs/index/BRANCH_STATE.md`
- preferer un futur patch d'agregation sur une ligne a jour `sot/mainline`
