# 14_REMEDIATION_APPLY_EXECUTION_LOG

## Objectif

Executer uniquement les commandes autorisees par `13_REMEDIATION_EXECUTION_GATE_REQUEST.md` et capturer les preuves.

## Runtime lock

```text
RUNTIME_REMAINS_BLOCKED
NO_OPENCLAW_AGENT_EXECUTION
NO_SSH_CONNECTION
NO_REMOTE_COMMAND
```

## Git precheck
```text
## go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01...origin/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01
?? docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/14_REMEDIATION_APPLY_EXECUTION_LOG.md
4527db13 docs: add AI team remote exec remediation execution gate request
a58583eb docs: add AI team remote exec remediation apply plan
626017b5 docs: record AI team remote exec sandbox config audit and update gates
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
 15 files changed, 4260 insertions(+)
```

## Remediation 1 — identity key resolution (non-connective)
```text
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

## Remediation 2 — sandbox config lecture avant modification
```text
=== agents.json5 (full) ===
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

=== grep cible ===
19:    sandbox: {
22:      scope: "agent",
42:        allow: [
52:        allowAgents: ["builder", "reviewer", "lab"],
64:        deny: [
74:        allowAgents: [],
86:        allow: [
89:        deny: [
98:        allowAgents: [],
110:        deny: [
120:        allowAgents: [],
```

## Remediation 3 — SSH alias confirmation (non-connective)
```text
host fantome
user fantome
hostname 192.168.0.191
port 22
identityfile ~/.ssh/id_ed25519
identityfile ~/.ssh/id_ed25519_fantome
```

## Verdict execution
| Remediation | Executed | Result | Runtime violation |
|:--|:--|:--|:--|
| identity key resolution | YES | A analyser ci-dessus | NO |
| sandbox config lecture | YES | A analyser ci-dessus | NO |
| SSH alias confirmation | YES | A analyser ci-dessus | NO |

```text
RUNTIME_REMAINS_BLOCKED
```


## RISKS

- À qualifier.
