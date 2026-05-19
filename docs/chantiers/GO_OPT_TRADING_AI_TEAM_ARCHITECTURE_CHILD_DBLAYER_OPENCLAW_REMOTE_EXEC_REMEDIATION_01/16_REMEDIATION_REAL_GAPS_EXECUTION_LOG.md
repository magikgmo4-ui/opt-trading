# 16_REMEDIATION_REAL_GAPS_EXECUTION_LOG

## Objectif

Appliquer uniquement les corrections non-runtime restantes :

1. configurer l'alias SSH `fantome` pour l'utilisateur `openclaw`;
2. auditer le schema `sandbox.mode`;
3. patcher `agents.json5` seulement si une valeur supportee est prouvee.

## Runtime lock

```text
NO_OPENCLAW_RUNTIME
NO_SSH_CONNECTION
NO_REMOTE_COMMAND
NO_SECRET_IN_REPO
```

## Git precheck
```text
## go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01...origin/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01
?? docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/16_REMEDIATION_REAL_GAPS_EXECUTION_LOG.md
4206c937 docs: plan real gap remediation for openclaw ssh and sandbox
518c9c2c docs: record AI team remote exec remediation apply execution
4527db13 docs: add AI team remote exec remediation execution gate request
a58583eb docs: add AI team remote exec remediation apply plan
626017b5 docs: record AI team remote exec sandbox config audit and update gates
7e94bc24 docs: record AI team remote exec remediation clearance execution
b7216b1f docs: add AI team remote exec remediation blocker clearance plan
735ff080 docs: update gate validation and record remediation blockers
7688137f docs: add AI team remote exec remediation gate validation
27b67b36 docs: add AI team remote exec remediation execution plan
5ae2a3dd docs: select AI team remote exec remediation options
7d8db742 docs: add AI team remote exec remediation decision matrix
 .../00_INITIAL_PROJECT_DOC.md                      |  160 ++
 .../01_IDENTITY_AUDIT.md                           |   43 +
 .../02_SANDBOX_AUDIT.md                            |   43 +
 .../03_SSH_ALIAS_AUDIT.md                          |   43 +
 .../04_REMEDIATION_DECISION_MATRIX.md              |   63 +
 .../05_REMEDIATION_SELECTED_OPTIONS.md             |   90 +
 .../06_REMEDIATION_EXECUTION_PLAN.md               |  253 +++
 .../07_GATE_PROOF_LOCAL_OUTPUT.txt                 | 2165 ++++++++++++++++++++
 .../07_REMEDIATION_GATE_VALIDATION.md              |  157 ++
 .../08_REMEDIATION_BLOCKER_REPORT.md               |  126 ++
 .../09_REMEDIATION_BLOCKER_CLEARANCE_PLAN.md       |  206 ++
 ..._REMEDIATION_BLOCKER_CLEARANCE_EXECUTION_LOG.md |  363 ++++
 .../11_REMEDIATION_SANDBOX_CONFIG_AUDIT.md         |  228 +++
 .../12_REMEDIATION_APPLY_PLAN.md                   |  241 +++
 .../13_REMEDIATION_EXECUTION_GATE_REQUEST.md       |   79 +
 .../14_REMEDIATION_APPLY_EXECUTION_LOG.md          |  296 +++
 .../15_REMEDIATION_REAL_GAPS_APPLY_PLAN.md         |  142 ++
 17 files changed, 4698 insertions(+)
```

## SSH openclaw — before
```text
Pseudo-terminal will not be allocated because stdin is not a terminal.
host fantome
user openclaw
hostname fantome
port 22
addressfamily any
batchmode no
canonicalizefallbacklocal yes
canonicalizehostname false
checkhostip no
compression no
controlmaster false
enablesshkeysign no
clearallforwardings no
exitonforwardfailure no
fingerprinthash SHA256
forwardx11 no
forwardx11trusted yes
gatewayports no
gssapiauthentication yes
gssapikeyexchange no
gssapidelegatecredentials no
gssapitrustdns no
gssapirenewalforcesrekey no
gssapikexalgorithms gss-group14-sha256-,gss-group16-sha512-,gss-nistp256-sha256-,gss-curve25519-sha256-,gss-group14-sha1-,gss-gex-sha1-
hashknownhosts yes
hostbasedauthentication no
identitiesonly no
kbdinteractiveauthentication yes
nohostauthenticationforlocalhost no
passwordauthentication yes
permitlocalcommand no
proxyusefdpass no
pubkeyauthentication true
requesttty auto
sessiontype default
stdinnull no
forkafterauthentication no
streamlocalbindunlink no
stricthostkeychecking ask
tcpkeepalive yes
tunnel false
verifyhostkeydns false
visualhostkey no
updatehostkeys true
enableescapecommandline no
canonicalizemaxdots 1
connectionattempts 1
forwardx11timeout 1200
numberofpasswordprompts 3
serveralivecountmax 3
serveraliveinterval 0
requiredrsasize 1024
obscurekeystroketiming yes
ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com
hostkeyalgorithms ssh-ed25519-cert-v01@openssh.com,ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com,sk-ecdsa-sha2-nistp256-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256
hostbasedacceptedalgorithms ssh-ed25519-cert-v01@openssh.com,ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com,sk-ecdsa-sha2-nistp256-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256
kexalgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,diffie-hellman-group14-sha256
casignaturealgorithms ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256
loglevel INFO
macs umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1-etm@openssh.com,umac-64@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-sha1
securitykeyprovider internal
pubkeyacceptedalgorithms ssh-ed25519-cert-v01@openssh.com,ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com,sk-ecdsa-sha2-nistp256-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256
xauthlocation /usr/bin/xauth
identityfile ~/.ssh/id_rsa
identityfile ~/.ssh/id_ecdsa
identityfile ~/.ssh/id_ecdsa_sk
identityfile ~/.ssh/id_ed25519
identityfile ~/.ssh/id_ed25519_sk
identityfile ~/.ssh/id_xmss
identityfile ~/.ssh/id_dsa
canonicaldomains none
globalknownhostsfile /etc/ssh/ssh_known_hosts /etc/ssh/ssh_known_hosts2
userknownhostsfile /home/openclaw/.ssh/known_hosts /home/openclaw/.ssh/known_hosts2
sendenv LANG
sendenv LC_*
logverbose none
channeltimeout none
permitremoteopen any
addkeystoagent false
forwardagent no
connecttimeout none
tunneldevice any:any
canonicalizePermittedcnames none
controlpersist no
escapechar ~
ipqos lowdelay throughput
rekeylimit 0 0
streamlocalbindmask 0177
syslogfacility USER
```

## SSH openclaw — apply alias config
```text
Host fantome appended to /home/openclaw/.ssh/config
```

## SSH openclaw — after non-connective proof
```text
drwx------ 2 openclaw openclaw 4096 May 12 02:03 /home/openclaw/.ssh
-rw------- 1 openclaw openclaw 121 May 12 02:03 /home/openclaw/.ssh/config
Pseudo-terminal will not be allocated because stdin is not a terminal.
host fantome
user fantome
hostname 192.168.0.191
port 22
addressfamily any
batchmode no
canonicalizefallbacklocal yes
canonicalizehostname false
checkhostip no
compression no
controlmaster false
enablesshkeysign no
clearallforwardings no
exitonforwardfailure no
fingerprinthash SHA256
forwardx11 no
forwardx11trusted yes
gatewayports no
gssapiauthentication yes
gssapikeyexchange no
gssapidelegatecredentials no
gssapitrustdns no
gssapirenewalforcesrekey no
gssapikexalgorithms gss-group14-sha256-,gss-group16-sha512-,gss-nistp256-sha256-,gss-curve25519-sha256-,gss-group14-sha1-,gss-gex-sha1-
hashknownhosts yes
hostbasedauthentication no
identitiesonly yes
kbdinteractiveauthentication yes
nohostauthenticationforlocalhost no
passwordauthentication yes
permitlocalcommand no
proxyusefdpass no
pubkeyauthentication true
requesttty auto
sessiontype default
stdinnull no
forkafterauthentication no
streamlocalbindunlink no
stricthostkeychecking ask
tcpkeepalive yes
tunnel false
verifyhostkeydns false
visualhostkey no
updatehostkeys true
enableescapecommandline no
canonicalizemaxdots 1
connectionattempts 1
forwardx11timeout 1200
numberofpasswordprompts 3
serveralivecountmax 3
serveraliveinterval 0
requiredrsasize 1024
obscurekeystroketiming yes
ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com
hostkeyalgorithms ssh-ed25519-cert-v01@openssh.com,ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com,sk-ecdsa-sha2-nistp256-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256
hostbasedacceptedalgorithms ssh-ed25519-cert-v01@openssh.com,ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com,sk-ecdsa-sha2-nistp256-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256
kexalgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,diffie-hellman-group14-sha256
casignaturealgorithms ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256
loglevel INFO
macs umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1-etm@openssh.com,umac-64@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-sha1
securitykeyprovider internal
pubkeyacceptedalgorithms ssh-ed25519-cert-v01@openssh.com,ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com,sk-ecdsa-sha2-nistp256-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256
xauthlocation /usr/bin/xauth
identityfile /home/openclaw/.ssh/id_ed25519_fantome
canonicaldomains none
globalknownhostsfile /etc/ssh/ssh_known_hosts /etc/ssh/ssh_known_hosts2
userknownhostsfile /home/openclaw/.ssh/known_hosts /home/openclaw/.ssh/known_hosts2
sendenv LANG
sendenv LC_*
logverbose none
channeltimeout none
permitremoteopen any
addkeystoagent false
forwardagent no
connecttimeout none
tunneldevice any:any
canonicalizePermittedcnames none
controlpersist no
escapechar ~
ipqos lowdelay throughput
rekeylimit 0 0
streamlocalbindmask 0177
syslogfacility USER
```

## SSH openclaw — key material presence check
```text
KEY_PATH_ABSENT: /home/openclaw/.ssh/id_ed25519_fantome
No key copied. Secret-safe blocker remains for actual SSH connection.
```

## Sandbox schema audit
```text
{
  defaults: {
    userTimezone: "America/Montreal",
    timeFormat: "24",

    model: {
      primary: "openai/gpt-5.4",
      fallbacks: [],
    },

    models: {
      "openai/gpt-5.4": {
        alias: "gpt-5.4",
      },
    },

    workspace: "/home/openclaw/.openclaw/workspace",

    sandbox: {
      mode: "all",
      workspaceAccess: "rw",
      scope: "agent",
    },

    subagents: {
      maxConcurrent: 1,
      runTimeoutSeconds: 900,
      archiveAfterMinutes: 60,
    },
  },

  list: [
    {
      id: "orchestrateur",
      default: true,
      name: "Orchestrateur Local V1.2.1",
      workspace: "/home/openclaw/.openclaw/workspace-orchestrateur",
      agentDir: "/home/openclaw/.openclaw/agents/orchestrateur/agent",
      model: "openai/gpt-5.4",
      tools: {
        profile: "minimal",
        allow: [
          "sessions_list",
          "sessions_history",
          "sessions_send",
          "sessions_spawn",
          "memory_search",
          "memory_get",
        ],
      },
      subagents: {
        allowAgents: ["builder", "reviewer", "lab"],
      },
    },

    {
      id: "builder",
      name: "Builder Borne V1.2.1",
      workspace: "/home/openclaw/.openclaw/workspace-builder",
      agentDir: "/home/openclaw/.openclaw/agents/builder/agent",
      model: "openai/gpt-5.4",
      tools: {
        profile: "coding",
        deny: [
          "group:runtime",
          "browser",
          "canvas",
          "nodes",
          "cron",
          "gateway",
        ],
      },
      subagents: {
        allowAgents: [],
      },
    },

    {
      id: "reviewer",
      name: "Reviewer Strict V1.2.1",
      workspace: "/home/openclaw/.openclaw/workspace-reviewer",
      agentDir: "/home/openclaw/.openclaw/agents/reviewer/agent",
      model: "openai/gpt-5.4",
      tools: {
        profile: "messaging",
        allow: [
          "sessions_history",
        ],
        deny: [
          "browser",
          "canvas",
          "nodes",
          "cron",
          "gateway",
        ],
      },
      subagents: {
        allowAgents: [],
      },
    },

    {
      id: "lab",
      name: "Lab Sandbox V1.2.1",
      workspace: "/home/openclaw/.openclaw/workspace-lab",
      agentDir: "/home/openclaw/.openclaw/agents/lab/agent",
      model: "openai/gpt-5.4",
      tools: {
        profile: "coding",
        deny: [
          "group:runtime",
          "browser",
          "canvas",
          "nodes",
          "cron",
          "gateway",
        ],
      },
      subagents: {
        allowAgents: [],
      },
    },
  ],
}
--- focused grep ---
modules/openclaw_config_modulaire/app/agents.json5:20:      mode: "all",
modules/openclaw_config_modulaire/app/agents.json5:21:      workspaceAccess: "rw",

=== Modules/doc wider scan ===
modules/openclaw_config_modulaire/app/agents.json5:20:      mode: "all",
```

## Sandbox patch status

```text
Patch not auto-applied in this first pass.
Reason: sandbox.mode target must be proven by schema/code before replacing mode="all".
```

## Runtime status
```text
No OpenClaw runtime executed.
No SSH connection attempted.
No remote command executed.
```
