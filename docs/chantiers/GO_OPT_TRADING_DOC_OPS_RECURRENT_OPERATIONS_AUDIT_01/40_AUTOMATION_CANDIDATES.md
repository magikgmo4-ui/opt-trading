# 40_AUTOMATION_CANDIDATES.md

## Candidates for Automation Based on Recurrent Operations Analysis

### High-Impact, Low-Complexity Automation Targets

#### 1. GO Naming and Directory Creation
- **Pattern**: Consistent naming convention `GO_<SCOPE>_<SURFACE>_<ROLE>_<OBJECT>_<NN>`
- **Frequency**: Every new chantier (566 instances)
- **Automation Opportunity**: 
  - Script to validate GO name format on creation
  - Template generator for standard chantier directory structure
  - Pre-populate with 00_INITIAL_PROJECT_DOC.md template
- **Impact**: Reduce manual errors, ensure consistency

#### 2. Initial Documentation Generation
- **Pattern**: 00_INITIAL_PROJECT_DOC.md with standard sections
- **Frequency**: 152 instances (and growing)
- **Automation Opportunity**:
  - Template with sections: Mission, Contexte, Contraintes, Objectif, Livrables, État de départ
  - Auto-populate with standard contraintes based on chantier type (READ_ONLY, DOC_ONLY, etc.)
  - Generate from GO name parsing (extract scope, surface, role, object)
- **Impact**: Save time, ensure all required sections present

#### 3. Closeout Documentation Generation
- **Pattern**: 90_CLOSEOUT.md or similar with standard sections
- **Frequency**: 415 instances
- **Automation Opportunity**:
  - Template with sections: Résumé, Preuves, Verdict, Contraintes respectées, Gaps, Prochaines étapes
  - Auto-populate from git diff, test results, checklist completion
  - Integrate with validation scripts to auto-determine PASS/FAIL/BLOCKED/PARTIAL
- **Impact**: Standardize closeouts, reduce omissions

#### 4. Inbox Entry Creation
- **Pattern**: Single markdown file in docs/index/inbox/<GO_ID>.md
- **Frequency**: 174 instances
- **Automation Opportunity**:
  - Script to create inbox entry when chantier is created (if parent significant)
  - Auto-populate with GO ID, parent reference, one-line summary
  - Link to chantier directory
- **Impact**: Ensure discoverability without manual effort

#### 5. Keyword and Constraint Validation
- **Pattern**: Frequent use of specific keywords (PASS, FAIL, etc.) and constraints
- **Frequency**: Thousands of occurrences
- **Automation Opportunity**:
  - Pre-commit hook to check for required keywords in closeout documents
  - Validate that constraints mentioned in 00_INITIAL_PROJECT_DOC.md are addressed in 90_CLOSEOUT.md
  - Check for presence of READ_ONLY/DOC_ONLY when appropriate
- **Impact**: Increase compliance, reduce review burden

#### 6. Branch State Tracking
- **Pattern**: BRANCH_STATE.md files (11 instances, but likely undercounted)
- **Automation Opportunity**:
  - Auto-generate BRANCH_STATE.md when chantier branch is created
  - Update with current branch, sync status with sot/mainline, reprise instructions
  - Integrate with git fetch/push operations
- **Impact**: Better branch management, reduce context switching cost

#### 7. Surface-Specific Validation
- **Pattern**: High frequency of surface-specific terms (OpenClaw, tmux, Desk Pro, etc.)
- **Automation Opportunity**:
  - Create validation rules per surface (e.g., for OpenClaw: check specific file patterns, registry updates)
  - Automated checks for Desk Pro UI changes (visual regression tests)
  - Telegram message format validation
- **Impact**: Increase quality, reduce surface-specific errors

### Medium-Impact Automation Targets

#### 8. Repetition Detection and Deduplication
- **Pattern**: Similar chantier names and structures
- **Automation Opportunity**:
  - Analyze existing chantiers to suggest similar existing work
  - Prevent duplicate effort by surfacing related GO_IDs
  - Group chantiers by surface/objective for better overview
- **Impact**: Reduce redundancy, improve knowledge sharing

#### 9. Metrics and Dashboard Generation
- **Pattern**: Need for quantitative understanding of repo activity
- **Automation Opportunity**:
  - Regular reports on chantier open/close rates
  - Surface activity heatmaps
  - Keyword trend analysis over time
  - Blockage reasons analysis (from BLOCKED instances)
- **Impact**: Data-driven process improvement

#### 10. Template Evolution and Versioning
- **Pattern**: Standard templates used across chantiers
- **Automation Opportunity**:
  - Central template repository with versioning
  - Automatic migration of old chantiers to new template standards
  - Template usage analytics
- **Impact**: Keep documentation standards current

### Low-Hanging Fruit (Quick Wins)

#### 11. Git State Verification Automation
- **Pattern**: Every chantier starts with git status, fetch, etc.
- **Automation Opportunity**:
  - Wrapper script or alias that performs standard verification
  - Outputs summary: branch, sync status, uncommitted changes
  - Prevents starting work on outdated branch
- **Impact**: Save seconds per chantier, prevent errors

#### 12. Constraint Checking Lite
- **Pattern**: Frequent mention of READ_ONLY, DOC_ONLY, etc.
- **Automation Opportunity**:
  - Simple script to check if these words appear in appropriate contexts
  - Flag if READ_ONLY chantier attempts to modify runtime files
  - Flag if DOC_ONLY chantier modifies non-documentation files
- **Impact**: Catch obvious mistakes early

### Automation Implementation Approach

1. **Start with Git Hooks**: Pre-commit and prepare-commit-msg for basic validation
2. **Create CLI Tool**: `go-helper` for common operations (create GO, generate docs, validate)
3. **Integrate with CI**: Validate chantier structure and constraints on PR
4. **Build Dashboard**: Periodic reports on chantier health and metrics
5. **Community Templates**: Evolve based on actual usage patterns

### Risks and Considerations

- **Over-automation**: Don't remove necessary human judgment
- **Maintenance overhead**: Automation scripts need maintenance
- **Adoption**: Requires training and buy-in from contributors
- **Flexibility**: Must accommodate edge cases and unique situations

### Recommended First Steps

1. Create a standard 00_INITIAL_PROJECT_DOC.md template
2. Build a script to create a new chantier with standard structure
3. Implement pre-commit checks for GO naming and basic constraint presence
4. Generate a report showing current chantier statistics (like this audit)