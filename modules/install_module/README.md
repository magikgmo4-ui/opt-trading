\
    # install_module — patch (sync_validate)

    This patch adds a **git push + sync/validate** workflow so you can:
    - commit/push on the current machine
    - pull `--ff-only` on other linux machines (default: `student db-layer`)
    - optional sanity check if available

    ## Commands

    - `menu-install_module`
    - `cmd-install_module sync_validate --hosts "student db-layer"`
    - Auto-commit:
      - `cmd-install_module sync_validate --auto-commit --commit "msg"`

    ## Requirements
    - SSH key-based access already configured (reseau_ssh).
    - Remote machines have repo at `/opt/trading`.
