# Adding adapters

A new adapter should:

1. Subclass `BaseAdapter`.
2. Return `AdapterResult`.
3. Populate a `ReflexCase` with traceable records.
4. Hash or safely skip source files according to configured limits.
5. Use `InspectionFlag` for partial or uncertain extraction.
6. Avoid writing reports, REST responses, or global state directly.
7. Be registered in `caereflex.services.inspect_with_adapter` and `detect_adapter` when appropriate.
8. Include tests and wiki updates.
