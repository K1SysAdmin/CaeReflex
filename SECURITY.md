# Security

Supported version: 1.0.0.

Security reports: <to be configured by project owner>

CaeReflex is localhost-first. Non-localhost REST serving requires an API key. The REST server restricts paths outside localhost, rejects path traversal, and does not expose solver execution, shell execution, or file mutation endpoints.

CrossRef use sends only generated query strings and API parameters, never raw simulation files.
