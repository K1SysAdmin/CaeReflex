# Security

Supported version: **1.0.0**

Security reports: [ipcontrol@knowdyn.co.uk](mailto:ipcontrol@knowdyn.co.uk)

CaeReflex is source-available software owned and licensed by **KNOWDYN LTD (UK)**. This file explains the security model, supported version, vulnerability-reporting process, deployment assumptions, privacy boundaries, and known limitations for CaeReflex V1.0.0.

---

## 1. Supported Version

| Version          | Security support |
| ---------------- | ---------------: |
| 1.0.0            |        Supported |
| Earlier versions |    Not supported |

Security reports should refer to the affected version, operating system, Python version, installation method, command used, and whether the issue affects CLI use, REST/API use, CrossRef use, file inspection, exports, packaging, or documentation.

---

## 2. Reporting Security Issues

Report suspected vulnerabilities to:

[ipcontrol@knowdyn.co.uk](mailto:ipcontrol@knowdyn.co.uk)

Please include, where possible:

1. a concise description of the issue;
2. steps to reproduce;
3. affected files, commands, endpoints, or workflows;
4. expected behaviour;
5. observed behaviour;
6. sample input files if safe to share;
7. whether the issue requires optional dependencies;
8. whether the issue affects local CLI use, REST use, or generated outputs;
9. any relevant logs or tracebacks;
10. whether the issue is already public.

Do **not** send proprietary simulation files, confidential engineering cases, credentials, API keys, private tokens, personal data, or controlled technical data unless specifically agreed in writing.

---

## 3. Security Scope

Security issues include, without limitation:

1. path traversal;
2. unrestricted filesystem access;
3. accidental exposure of absolute local paths in `agent_context.json`;
4. unintended shell execution;
5. unintended solver execution;
6. unintended source-file mutation;
7. unsafe REST exposure;
8. missing API-key enforcement outside localhost;
9. leaking API keys or secrets in logs, reports, exceptions, or exported files;
10. hidden CrossRef calls during ordinary inspection;
11. sending raw simulation files to external services;
12. unsafe handling of malformed simulation files;
13. denial-of-service risks from unbounded scanning or large files;
14. dependency-related security concerns;
15. generated outputs that could mislead agents into overclaiming validation, certification, convergence, or design safety.

Security issues do **not** include requests for new features, solver support, commercial licensing, legal interpretation, scientific validation, or engineering review unless they also create a concrete security risk.

---

## 4. Localhost-First Security Model

CaeReflex is **localhost-first**.

The default REST server mode is intended for local development and local agent workflows:

```bash
caereflex serve --host 127.0.0.1 --port 8765
```

In localhost mode, CaeReflex may inspect local paths provided by the user. Even in localhost mode, CaeReflex is designed to use read-only inspection, bounded scanning, file-size limits, and structured error handling.

CaeReflex should not be exposed directly to the public internet without an appropriate deployment review, HTTPS termination, access control, API-key management, logging policy, workspace restriction, and operational security controls.

---

## 5. Non-Localhost REST Serving

Non-localhost REST serving requires an API key.

Example:

```bash
caereflex serve --host 0.0.0.0 --port 8765 --api-key "$CAEREFLEX_API_KEY"
```

When served outside localhost, CaeReflex must:

1. require API-key authentication;
2. restrict case inspection to a configured workspace;
3. reject path traversal;
4. reject arbitrary absolute paths outside the configured workspace;
5. enforce request-size limits;
6. enforce file-size limits;
7. enforce scan-depth limits;
8. enforce scan-file-count limits;
9. avoid logging API keys;
10. avoid exposing absolute local paths in agent-facing outputs.

CaeReflex V1.0.0 does not provide OAuth, user accounts, RBAC, multi-tenant isolation, licence-server enforcement, payment enforcement, or enterprise identity management.

---

## 6. Filesystem and Path Safety

CaeReflex performs read-only inspection of supported engineering artefacts.

CaeReflex must not:

1. execute shell commands;
2. run solvers;
3. run meshing jobs;
4. launch ParaView;
5. mutate source simulation files;
6. write into inspected source directories unless explicitly requested by the user through an output path;
7. follow path traversal outside an allowed workspace in non-localhost mode;
8. expose unrestricted filesystem browsing through REST endpoints.

The following path patterns should be rejected in restricted modes:

```text
../
../../
/etc
/root
~/.ssh
C:\Users\...\Secrets
```

Generated agent-facing outputs must use safe display paths, relative paths, file identifiers, or metadata summaries rather than absolute local paths.

---

## 7. Solver, Shell, and File-Mutation Policy

CaeReflex V1.0.0 does **not** expose endpoints or CLI commands for:

1. OpenFOAM execution;
2. Gmsh meshing execution;
3. ParaView launch or automation;
4. shell command execution;
5. source-file mutation;
6. CAD repair;
7. mesh repair;
8. design optimisation;
9. autonomous engineering decisions.

Any behaviour that enables unintended solver execution, shell execution, or source-file mutation should be reported as a security issue.

---

## 8. CrossRef Privacy and Network Use

CaeReflex may use CrossRef only when explicitly requested through commands or REST actions such as:

```bash
caereflex crossref search CASE_JSON
caereflex crossref attach CASE_JSON
caereflex inspect PATH --attach-crossref
```

CaeReflex must not call CrossRef during ordinary inspection unless explicitly requested.

When CrossRef is used, CaeReflex sends only generated query strings, user-supplied query strings, and API parameters. CaeReflex must not send raw simulation files, full case folders, proprietary engineering artefacts, local file contents, secrets, API keys, or private tokens to CrossRef.

CrossRef-derived outputs are metadata and available-abstract context only. They are not full-paper retrieval, systematic review, validation evidence, certification evidence, or safety approval.

---

## 9. Agent-Facing Output Safety

CaeReflex generates files and responses intended for use by LLM agents, including:

```text
caereflex.json
agent_context.json
agent_context.md
case_report.md
REST JSON responses
CLI JSON summaries
BibTeX exports
```

Agent-facing outputs must preserve distinctions between:

1. extracted facts;
2. inferred facts;
3. generated summaries;
4. user-supplied inputs;
5. external CrossRef metadata.

Agent-facing outputs must not claim that CaeReflex validates, certifies, approves, proves convergence, assesses mesh adequacy, or approves design safety.

Any generated output that exposes absolute paths, secrets, credentials, proprietary data beyond the inspected metadata scope, or misleading safety/validation claims should be treated as a security or safety issue.

---

## 10. Secrets and Credentials

Users should not store secrets, API keys, commercial credentials, private tokens, passwords, SSH keys, or proprietary access credentials inside simulation folders inspected by CaeReflex.

CaeReflex is not a secrets scanner.

If a user points CaeReflex at a folder containing secrets, CaeReflex may record filenames, metadata, hashes, or safe excerpts depending on the adapter. Users are responsible for keeping sensitive files outside inspected workspaces.

API keys used for REST access must be kept private and must not be committed to repositories, examples, notebooks, reports, or generated outputs.

Recommended local secret patterns:

```text
.env
.env.local
*.secret
*.key
*.pem
```

These should be excluded from repositories and inspected workspaces where possible.

---

## 11. Dependency Security

CaeReflex uses optional dependency groups to reduce the security and installation footprint of the core package.

Core use does not require heavyweight optional packages such as Gmsh, PyVista, VTK, or meshio.

Users are responsible for maintaining a secure Python environment and updating third-party dependencies according to their own security policies.

Optional dependency groups include:

```text
server
mesh
vtk
gmsh
dev
all
```

Third-party dependencies are governed by their own licences and security practices. See `THIRD_PARTY_NOTICES.md` where applicable.

---

## 12. Example and Test Data Safety

Bundled examples are intended to be small, local, reproducible, and safe for offline testing.

CaeReflex examples should not require:

1. live CrossRef access;
2. OpenFOAM installation;
3. Gmsh installation;
4. ParaView installation;
5. large downloads;
6. proprietary datasets;
7. unclear-licence external files.

Normal tests should use mocked CrossRef responses and local example files.

---

## 13. Known Limitations

CaeReflex V1.0.0 is not a sandbox, container runtime, secrets scanner, malware scanner, engineering validator, or secure multi-tenant SaaS platform.

Known limitations include:

1. local users may intentionally inspect arbitrary local paths in localhost/CLI mode;
2. parsers are pragmatic and may not cover every grammar feature of engineering file formats;
3. malformed or unusually large files may trigger parsing errors or partial inspection;
4. optional dependencies have their own security posture;
5. generated outputs are only as reliable as the inspected files and available metadata;
6. CrossRef metadata may be incomplete or unavailable;
7. no legal, regulatory, safety, or engineering certification is provided.

Users deploying CaeReflex in commercial, institutional, cloud, enterprise, or internet-facing environments must perform their own security review.

---

## 14. Responsible Disclosure

KNOWDYN LTD (UK) asks security researchers and users to report suspected vulnerabilities privately before public disclosure.

Please allow reasonable time for review and remediation before publishing technical details.

Do not use vulnerability testing to access, modify, delete, exfiltrate, overload, or disrupt data, systems, services, repositories, accounts, or infrastructure that you do not own or have explicit permission to test.

---

## 15. No Warranty and No Liability

CaeReflex is provided “as is” and “as available”, without warranty of any kind.

Any use of CaeReflex is at the user’s sole risk. Users agree to indemnify and hold harmless KNOWDYN LTD (UK), its owners, licensors, officers, employees, contractors, and affiliates from claims, losses, liabilities, damages, costs, and consequences arising from access to or use of CaeReflex, including misuse, unsafe reliance, automated-agent action, engineering decisions, commercial deployment, security failures, or downstream consequences.

---

## 16. Contact

Security reports, permissions, and security-related licensing questions:[research@knowdyn.co.uk](mailto:research@knowdyn.co.uk)
