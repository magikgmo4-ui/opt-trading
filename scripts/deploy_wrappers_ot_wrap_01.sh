#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading"

echo "Deploying Validated Prompt Factory..."
sudo ln -sf "$BASE/modules/validated_prompt_factory/menu.sh" /usr/local/bin/menu-validated_prompt_factory
sudo ln -sf "$BASE/modules/validated_prompt_factory/cmd.sh" /usr/local/bin/cmd-validated_prompt_factory
sudo ln -sf "$BASE/modules/validated_prompt_factory/sanity.sh" /usr/local/bin/sanity-validated_prompt_factory
sudo chmod +x "$BASE/modules/validated_prompt_factory/menu.sh" "$BASE/modules/validated_prompt_factory/cmd.sh" "$BASE/modules/validated_prompt_factory/sanity.sh"

echo "Deploying Trae Module Validator..."
sudo ln -sf "$BASE/modules/trae_module_validator/menu.sh" /usr/local/bin/menu-trae_module_validator
sudo ln -sf "$BASE/modules/trae_module_validator/cmd.sh" /usr/local/bin/cmd-trae_module_validator
sudo ln -sf "$BASE/modules/trae_module_validator/sanity.sh" /usr/local/bin/sanity-trae_module_validator
sudo chmod +x "$BASE/modules/trae_module_validator/menu.sh" "$BASE/modules/trae_module_validator/cmd.sh" "$BASE/modules/trae_module_validator/sanity.sh"

echo "Done."
ls -l /usr/local/bin/*validated_prompt_factory* /usr/local/bin/*trae_module_validator*
