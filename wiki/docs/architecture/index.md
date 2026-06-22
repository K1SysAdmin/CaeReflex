# Architecture overview

CaeReflex has a small service-oriented spine:

```text
CLI / REST / Python API
  -> caereflex.services
  -> adapter selection
  -> adapter.inspect(path)
  -> ReflexCase
  -> exporters / case store / CrossRef attachment
```

The domain model lives in `caereflex.core.models`. Adapters fill the model. Services orchestrate adapter selection, storage, CrossRef, and exports. CLI and REST both call services rather than duplicating business logic.
