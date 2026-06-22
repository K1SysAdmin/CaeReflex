# CrossRef

`caereflex.evidence.crossref` adds DOI metadata and available abstracts only when explicitly requested.

It can use a mock response for offline tests. Live requests call the CrossRef works API, parse metadata items, clean abstracts when present, deduplicate records, compute a simple query-term relevance score, and attach a `LiteratureContext`.

CrossRef records are literature context only. They do not validate a simulation or prove that full papers were read.
