from caereflex.core.models import ReflexCase, TraceInfo

def test_reflexcase_model():
    c = ReflexCase(case_id='case_test')
    assert c.schema_version == '1.0'

def test_trace_source_kind():
    t = TraceInfo(source_kind='extracted')
    assert t.source_kind == 'extracted'
