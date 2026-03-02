# Apply repo_hygiene in a controlled way

1) Add .gitignore lines (review first):
   cat modules/repo_hygiene/gitignore_additions.txt

2) Append to .gitignore (idempotent):
   while IFS= read -r line; do
     grep -qxF "$line" .gitignore || echo "$line" >> .gitignore
   done < modules/repo_hygiene/gitignore_additions.txt

3) Install shortcuts:
   sudo bash modules/repo_hygiene/install_shortcuts.sh

4) Sanity:
   sanity-repo_hygiene

If you want to de-track journal.md later (ONLY if you decide):
   git rm --cached journal.md
