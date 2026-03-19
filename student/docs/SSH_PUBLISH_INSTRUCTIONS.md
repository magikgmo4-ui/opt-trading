# SSH Publish Instructions

## Source Of Truth

- base branch: `sot/mainline`
- working branch: `student`

## Verify GitHub SSH Authentication

```bash
ssh -T git@github.com
```

## Push The `student` Branch Manually

```bash
cd /opt/trading
git push -u git@github.com:magikgmo4-ui/opt-trading.git student
```

## Run The Publish Helper Locally On The Machine

```bash
/opt/trading/student/bin/publish_student_pr_safe.sh
```

## Run The Publish Helper Over SSH

Using the SSH alias already configured on your machines:

```bash
ssh student 'bash /opt/trading/student/bin/publish_student_pr_safe.sh'
```

Or with an explicit user and host:

```bash
ssh student@192.168.16.103 'bash /opt/trading/student/bin/publish_student_pr_safe.sh'
```

## Pull Request

- base: `sot/mainline`
- head: `student`
- body file: `/opt/trading/student/docs/PR_STUDENT_CONSOLIDATION.md`
